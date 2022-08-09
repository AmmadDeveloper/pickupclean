#/api/time-slots/?country=GB&postcode=TW11%208UF
import json

from django.contrib.auth import authenticate
from ninja import NinjaAPI,Form
from ninja.security import HttpBearer
from models.models import Category,Files,ScheduleConfig,PostCode,PostCodeRequests,Service,Cart,Order
from rest_framework.authtoken.models import Token
from datetime import timedelta
import datetime
import requests
from ninja.responses import codes_4xx
from .schema import districtSchema,cartSchema,AuthenticationSchema
from models.utils.Constants import OrderType

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        user = Token.objects.get(key=token).user
        if user:
            return token
        else:
            return "invalid creds"


user_api = NinjaAPI(version='2.0.0')


@user_api.post("/login", auth=None)  # < overriding global auth
def get_token(request, user:AuthenticationSchema):
    user=authenticate(email=user.email,password=user.password)
    if user:
        token=Token.objects.filter(user_id=user.id).first()
        return {"token": token.key,"message":"Success","statuscode":200}
    else:
        return {"message":"Invalid Email or Password","statuscode":404}


@user_api.post('cart',auth=AuthBearer())
def add_cart(request,data:cartSchema):
    user = Token.objects.get(key=request.auth).user
    ord=Order.objects.filter(user_id=request.user.id,order_status=OrderType.OPEN).first()
    if ord:
        cart=Cart()
        cart.price=data.price
        cart.user=user
        cart.qty=data.qty
        cart.category_id=data.catid
        cart.service_id=data.id
        cart.total=data.total
        cart.order_id=ord.id
        cart.save()
        item=data
        return {'cartitem': {"cartid":cart.id,"catid":item.catid,"id":item.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.name,"catname":item.catname}, 'statuscode': 200, 'message': 'success'}
    else:
        return {'statuscode': 400, 'message': 'error'}

@user_api.patch('cart',auth=AuthBearer())
def update_cart(request,data:cartSchema):
    cart=Cart.objects.filter(id=data.cartid).first()
    cart.price=data.price
    cart.qty=data.qty
    cart.category_id=data.catid
    cart.service_id=data.id
    cart.total=data.total
    cart.save()
    item=data
    return {'cartitem': {"cartid":cart.id,"catid":item.catid,"id":item.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.name,"catname":item.catname}, 'statuscode': 200, 'message': 'success'}



@user_api.get('cart',auth=AuthBearer())
def get_cart(request):
    user = Token.objects.get(key=request.auth).user
    order=Order.objects.filter(user_id=request.user.id,order_status=OrderType.OPEN).first()
    cats=[{"cartid":item.id,"catid":item.category.id,"id":item.service.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.service.name,"catname":item.category.name} for item in Cart.objects.filter(active=True,purchased=False,user=user,order_id=order.id)]
    return cats

@user_api.delete('cart',auth=AuthBearer())
def delete_cart(request,cartid:int):
    obj=Cart.objects.filter(id=cartid).first()
    obj.active=False
    obj.save()
    return {'statuscode':200,'message':'success'}


@user_api.get('categories/',auth=None)
def get_categories(request):
    cats=[{"id":item.id,"name":item.name} for item in Category.objects.filter(active=True)]
    return cats

@user_api.get('services/',auth=None)
def get_services(request,id:int):
    servs=[{"id":item.id,"name":item.name,"price":item.price} for item in Service.objects.filter(category_id=id)]
    return servs


@user_api.get('time-slots/',response={200: dict, codes_4xx: dict},auth=None)
def time_slot(request,country:str,postcode:str,pickup_start:datetime.datetime=None):
    codes=PostCode.objects.filter(code__exact=postcode.split(" ")[0]).count()
    if codes>0:
        if pickup_start!=None:
            print((pickup_start+ timedelta(days=1)).date())
            days=[(pickup_start + timedelta(days=i)).date() for i in range(15)[2:] if
                (pickup_start + timedelta(days=i)).isoweekday() != 7]
        else:
            days = [(datetime.datetime.today() + timedelta(days=i)).date() for i in range(15) if
                (datetime.datetime.today() + timedelta(days=i)).isoweekday() != 7]
        res = {"country": country, "postcode": postcode, "availability": []}
        api_resp=requests.get("https://www.googleapis.com/calendar/v3/calendars/en.uk%23holiday@group.v.calendar.google.com/events?key=AIzaSyBjr42RKZeifwt7Za0P09BJGD8YXTPudLI")
        response=json.loads(api_resp.content)
        holidays = [item['start']['date'] for item in response["items"]]
        days = [day for day in days if str(day) not in holidays]
        x=days[0].isoweekday()
        sch = ScheduleConfig.objects.all()
        time_schedules = eval(sch[0].value)
        for day in days:
            timeslot_arr=[]
            start=int(time_schedules[str(day.isoweekday())]['start'].strftime("%H"))
            end = int(time_schedules[str(day.isoweekday())]['end'].strftime("%H"))
            today=datetime.datetime.now()
            if day==today.date():
                c_hr=today.strftime('%H')
                if start<int(c_hr) and int(c_hr)<end-2:
                    start=int(c_hr)+2

            while(start!=end):
                timeslot_arr.append({
                    "cleaners": [308, 160],
                    "full_label": day.strftime("%d %B %Y")+", "+str(start)+":00 - "+str(start+1)+":00",
                    "value": day.strftime("%Y-%m-%d")+"T"+str(start)+":00:00",
                    "tags": [],
                    "id":str(start)+"-"+str(start+1),
                    "label": str(start)+":00 - "+str(start+1)+":00"
                })
                start+=1
            if datetime.date.today() ==day:
                label="Today"
            elif datetime.date.today() + datetime.timedelta(days=1)==day:
                label="Tomorrow"
            else:
                label=time_schedules[str(day.isoweekday())]['day']
            data={
                "date":day.strftime("%Y-%m-%d"),
                "date_label":day.strftime("%d %B %Y"),
                "weekday_label":label[0].upper()+label[1:],
                "time_slots":timeslot_arr
            }
            res['availability'].append(data)

        return 200,res
    else:
        return 400,{"errors": [{"code": "address_not_served"}]}


@user_api.post('district-request/',auth=None)
def districtrequest(request,Items:districtSchema=Form('')):
    postCodeRequests=PostCodeRequests()
    postCodeRequests.email=Items.email
    postCodeRequests.postcode=Items.postcode
    postCodeRequests.name=Items.name
    postCodeRequests.country=Items.country
    postCodeRequests.save()
    return {'settings': Items, 'statuscode': 200, 'message': 'success'}


@user_api.get('updateorderfield/',auth=AuthBearer())
def placeorder(request,name:str,value:str,):
    user = Token.objects.get(key=request.auth).user
    order = Order.objects.filter(user_id=user.id, order_status=OrderType.OPEN).first()
    if name=='fullname':
        order.fullname=value
        order.save()
    elif name=='email':
        order.email = value
        order.save()
    elif name=='phone':
        order.phone = value
        order.save()
    elif name=='addressdetail':
        order.addressdetail = value
        order.detail=True
        order.save()
    return {'statuscode': 200, 'message': 'success'}


# weekdays pickup 8am-9pm
# sunday pickup 11am-4pm
# public and national holidays flag
# inshAllah dont worry about the quality

# scalable too
# you can add features in it later

#working days

# @user_api.post('intent/')
# def createIntent(request):
#     import stripe
#
#     from django.conf import settings
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#
#     res=stripe.PaymentIntent.create(
#         amount=1099,
#         currency="eur",
#         automatic_payment_methods={"enabled": True},
#     )
#     return {"success":"success"}

from models.models import PaymentIntent

@user_api.get('paymentdata',auth=AuthBearer())
def getPaymentIntent(request):
    user = Token.objects.get(key=request.auth).user
    order=Order.objects.filter(user_id=request.user.id, order_status=OrderType.OPEN).first()
    intent=PaymentIntent.objects.filter(order_id=order.id).first()
    return {'secret': intent.client_secret, 'statuscode': 200, 'message': 'success'}













#{
#   "amount": 1099,
#   "amount_capturable": 0,
#   "amount_details": {
#     "tip": {}
#   },
#   "amount_received": 0,
#   "application": null,
#   "application_fee_amount": null,
#   "automatic_payment_methods": {
#     "enabled": true
#   },
#   "canceled_at": null,
#   "cancellation_reason": null,
#   "capture_method": "automatic",
#   "charges": {
#     "data": [],
#     "has_more": false,
#     "object": "list",
#     "total_count": 0,
#     "url": "/v1/charges?payment_intent=pi_3LHE6tAIj4VUJPcD0zObiKgv"
#   },
#   "client_secret": "pi_3LHE6tAIj4VUJPcD0zObiKgv_secret_eWUF4WgLrmFTuH2BQpvVTIozh",
#   "confirmation_method": "automatic",
#   "created": 1656798255,
#   "currency": "eur",
#   "customer": null,
#   "description": null,
#   "id": "pi_3LHE6tAIj4VUJPcD0zObiKgv",
#   "invoice": null,
#   "last_payment_error": null,
#   "livemode": false,
#   "metadata": {},
#   "next_action": null,
#   "object": "payment_intent",
#   "on_behalf_of": null,
#   "payment_method": null,
#   "payment_method_options": {
#     "bancontact": {
#       "preferred_language": "en"
#     },
#     "card": {
#       "installments": null,
#       "mandate_options": null,
#       "network": null,
#       "request_three_d_secure": "automatic"
#     },
#     "eps": {},
#     "giropay": {},
#     "ideal": {},
#     "p24": {}
#   },
#   "payment_method_types": [
#     "card",
#     "bancontact",
#     "eps",
#     "giropay",
#     "ideal",
#     "p24"
#   ],
#   "processing": null,
#   "receipt_email": null,
#   "review": null,
#   "setup_future_usage": null,
#   "shipping": null,
#   "source": null,
#   "statement_descriptor": null,
#   "statement_descriptor_suffix": null,
#   "status": "requires_payment_method",
#   "transfer_data": null,
#   "transfer_group": null
# }