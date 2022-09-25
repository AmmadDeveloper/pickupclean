import functools
import json
from django.contrib.auth.models import User
import requests
from django.contrib.auth import authenticate
from django.db.models import Q
from ninja import NinjaAPI
from ninja.responses import codes_4xx
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token
from datetime import timedelta
import datetime
from models.models import PostCode, ScheduleConfig, Electronic_Address, Order, Cart, Category, Service, PaymentIntent, \
    ServiceType, Address
from mobile.schema import AuthenticationSchema, SignUpSchema, CreateOrderSchema, cartSchema
from models.utils.Constants import OrderType
from .schema import addressSchema
api = NinjaAPI(version='3.0.0')

class AuthClass(HttpBearer):
    def authenticate(self, request, token):
        user = Token.objects.get(key=token).user
        if user and user.is_active:
            return token
        else:
            return "invalid creds"


@api.post("/signup",auth=None)
def signup(request,fields:SignUpSchema):
    try:
        user = User.objects.create_user(password=fields.password, email=fields.email,
                                        username=fields.email)
        user.is_active = True
        user.first_name = fields.fullname.split(' ')[0]
        user.last_name = fields.fullname.split(' ')[1] if len(fields.fullname.split(' '))==2 else ''
        user.save()
        eadd = Electronic_Address()
        eadd.user = user
        eadd.phone = fields.phone
        eadd.save()
        token=Token.objects.filter(user_id=user.id).first()
        return {"token": token.key,"userinfo":{"firstname":user.first_name,"lastname":user.last_name,"phone":eadd.phone}, "message": "Success", "statuscode": 200}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}



@api.post("/login", auth=None)  # < overriding global auth
def get_token(request, user:AuthenticationSchema):
    user=authenticate(email=user.email,password=user.password)
    if user and user.is_active:
        token=Token.objects.filter(user_id=user.id).first()
        return {"token": token.key,"userinfo":{"firstname":user.first_name,"lastname":user.last_name},"message":"Success","statuscode":200}
    else:
        return {"message":"Invalid Email or Password","statuscode":404}


@api.get('time-slots',response={200: dict, codes_4xx: dict},auth=None)
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


@api.post('create_order',auth=AuthClass())
def create_order(request,order:CreateOrderSchema):
    try:
        user = Token.objects.get(key=request.auth).user
        ord = Order.objects.filter(user_id=user.id, order_status=OrderType.OPEN).first()
        eaddress = Electronic_Address.objects.filter(user_id=user.id).first()
        if not ord:
            ord = Order()
            ord.fullname = user.first_name + user.last_name
            ord.email = user.email
            if eaddress != None:
                ord.phone = eaddress.phone

        ord.ship_address1 = order.address_line1
        ord.ship_address2 = order.address_line2
        ord.ship_address3 = order.address_line3
        ord.ship_address4 = order.address_line4
        ord.ship_postal_code = order.postcode
        ord.ship_country = order.country
        ord.ship_city = order.city
        ord.pickup_date = order.pickup_date
        ord.dropoff_date = order.dropoff_date
        ord.pickup_time_slot = order.pickup_time_slot
        ord.dropoff_time_slot = order.dropoff_time_slot
        ord.user_id = user.id
        ord.save()
        return {"orderid": ord.id,"message":"Success","statuscode":200}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}
#102e77d8a7657a9b6ef896d39071e96c7acdf3b1


@api.post('cart',auth=AuthClass())
def add_cart(request,item:cartSchema):
    user = Token.objects.get(key=request.auth).user
    ord=Order.objects.filter(user_id=user.id,order_status=OrderType.OPEN).first()
    if ord:
        cart=Cart()
        cart.price=item.price
        cart.user=user
        cart.qty=item.qty
        cart.category_id=item.catid
        cart.service_id=item.id
        cart.total=item.total
        cart.order_id=ord.id
        cart.save()
        return {'cartitem': {"cartid":cart.id,"catid":item.catid,"id":item.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.name,"catname":item.catname}, 'statuscode': 200, 'message': 'success'}
    else:
        return {'statuscode': 400, 'message': 'error'}

@api.patch('cart',auth=AuthClass())
def update_cart(request,item:cartSchema):
    try:
        cart=Cart.objects.filter(id=item.cartid).first()
        cart.price=item.price
        cart.qty=item.qty
        cart.category_id=item.catid
        cart.service_id=item.id
        cart.total=item.total
        cart.save()
        return {'cartitem': {"cartid":cart.id,"catid":item.catid,"id":item.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.name,"catname":item.catname}, 'statuscode': 200, 'message': 'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}


@api.get('cart',auth=AuthClass())
def get_cart(request):
    user = Token.objects.get(key=request.auth).user
    order=Order.objects.filter(user_id=user.id,order_status=OrderType.OPEN).first()
    cats=[{"cartid":item.id,"catid":item.category.id,"id":item.service.id,"price":item.price,"total":item.total,"qty":item.qty,"name":item.service.name,"catname":item.category.name} for item in Cart.objects.filter(active=True,purchased=False,user=user,order_id=order.id)]
    return cats

@api.delete('cart',auth=AuthClass())
def delete_cart(request,cartid:int):
    try:
        obj=Cart.objects.filter(id=cartid).first()
        obj.active=False
        obj.save()
        return {'statuscode':200,'message':'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}

@api.get('categories/',auth=None)
def get_categories(request):
    cats=[{"id":item.id,"name":item.name,"icon":item.icon.url[6:] if item.icon.url else ''} for item in Category.objects.filter(active=True)]
    return cats

@api.get('types/',auth=None)
def get_types(request):
    types=[{"id":item.id,"name":item.name,"icon":item.picture.url[6:] if item.picture.url else ''} for item in ServiceType.objects.filter(active=True)]
    return types


@api.get('services/',auth=None)
def get_services(request,cat_id:int,type_id:int=None):
    servs=[{"id":item.id,"name":item.name,"price":item.price} for item in Service.objects.filter(category_id=cat_id,servicetype_id=type_id)]
    return servs


from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

@api.get('getfinalorder/',auth=AuthClass())
def finalize_order(request):
    try:
        user = Token.objects.get(key=request.auth).user
        order = Order.objects.filter(user_id=user.id, order_status=OrderType.OPEN).first()
        cart_total = [x.total for x in Cart.objects.filter(order_id=order.id, active=True)]
        cart = [{"cartid": item.id,
                 "catid": item.category.id,
                 "id": item.service.id,
                 "price": item.price,
                 "total": item.total,
                 "qty": item.qty,
                 "name": item.service.name,
                 "catname": item.category.name
                 } for item in Cart.objects.filter(active=True, purchased=False, user=user, order_id=order.id)]
        total_amount = functools.reduce(lambda a, b: a + b, cart_total, )
        order.order_amount = total_amount
        order.save()
        intent = PaymentIntent.objects.filter(order_id=order.id).first()
        if not intent:
            res = stripe.PaymentIntent.create(
                amount=int(order.order_amount * 100),
                currency="gbp",
                payment_method_types=["card"],
                metadata={
                    "order_id": order.id,
                    "user_id": user.id
                }
            )
            intent = PaymentIntent()
            intent.order = order
            intent.user = user
            intent.intentid = res.id
            intent.client_secret = res.client_secret
            intent.amount = res.amount
            intent.save()
        else:
            id = intent.intentid
            stripe_intent = stripe.PaymentIntent.retrieve(id)
            if int(total_amount * 100) != stripe_intent.amount:
                res = stripe.PaymentIntent.modify(
                    stripe_intent.id,
                    amount=int(total_amount * 100),
                )
                intent.amount = res.amount
                intent.save()
            # intent.intenti

        address = order.ship_address1 + ", " + order.ship_address2 + ", " + order.ship_address3 + ", " + order.ship_address4
        city = order.ship_city
        country = order.ship_country
        postcode = order.ship_postal_code
        pickup = {
            "timeslot": order.pickup_time_slot,
            "date": order.pickup_date.strftime("%A, %B %d")
        }
        dropoff = {
            "timeslot": order.dropoff_time_slot,
            "date": order.dropoff_date.strftime("%A, %B %d")
        }
        return {'addressdetail':order.addressdetail,'detail':order.detail,'name':order.fullname,'email':order.email,'phone':order.phone,'cart':cart,'total':total_amount,'address':address,'city':city,'country':country,'postcode':postcode,'pickup':pickup,'dropoff':dropoff,"message":"Success","statuscode":200}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}


@api.get('paymentdata',auth=AuthClass())
def getPaymentIntent(request):
    try:
        user = Token.objects.get(key=request.auth).user
        order=Order.objects.filter(user_id=user.id, order_status=OrderType.OPEN).first()
        intent=PaymentIntent.objects.filter(order_id=order.id).first()
        return {'secret': intent.client_secret,'public_key':'pk_test_51JlhHTAIj4VUJPcDeLGSFO23zCFWywO8QCsU6jwKzYBtgAeUzC3USVd28e9q71Msxcc5ZMPQRBGO5h0V2xbHefhQ00xEanG3at',"webhookurl":settings.SERVER_URL+'order/webhook/', 'statuscode': 200, 'message': 'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}

@api.get('getorderhistory',auth=AuthClass())
def order_history(request,fromdate:str=None,todate:str=None,limit:int=10,offset:int=0):
    try:
        user = Token.objects.get(key=request.auth).user
        query = Q()
        # query.add(Q(email__iexact=user.email), Q.OR)
        query.add(Q(user_id=user.pk), Q.OR)
        if fromdate:
            query.add(Q(order_place_date__gte=fromdate), Q.AND)
        if todate:
            query.add(Q(order_place_date__lte=todate), Q.AND)


        query.add(~Q(order_status=OrderType.OPEN), Q.AND)
        orders = [{"orderid": item.id,
                   "orderstatus": item.order_status,
                   "orderdate": item.order_date.strftime("%B %d, %Y") if item.order_date else '',
                   "pickuptime": item.pickup_time_slot,
                   "pickupdate": item.pickup_date.strftime("%B %d, %Y") if item.pickup_date else '',
                   "dropofftime": item.dropoff_time_slot,
                   "dropoffdate": item.dropoff_date.strftime("%B %d, %Y") if item.dropoff_date else '',
                   "orderamount": float(item.order_amount),
                   "orderaddress": item.__fulladdress__(),
                   'lines': [
                       {
                           "categoryname": line.category.name,
                           "quantity": line.qty,
                           "totalprice": line.total,
                           "price": line.price,
                           "productid": line.service.id,
                           "productname": line.service.name,
                           "image": line.category.icon.url[6:]

                       } for line in item.ordercart.all()]
                   }
                  for item in Order.objects.prefetch_related('ordercart').filter(query).order_by('-order_date')][offset:limit]
        return {"orders":orders,'statuscode': 200, 'message': 'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}


@api.get('updateorderfield/',auth=AuthClass())
def placeorder(request,name:str,value:str,):
    user = Token.objects.get(key=request.auth).user
    order = Order.objects.filter(user_id=user.id, order_status=OrderType.OPEN).first()
    if order:
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
    else:
        return {'statuscode': 400, 'message': 'not found'}


@api.get('address',auth=AuthClass())
def getaddress(request):
    try:
        user = Token.objects.get(key=request.auth).user
        item = Address.objects.filter(user_id=user.id).first()
        if item:
            return {'address': {"id":item.id,"line1":item.line1,"line2":item.line2,"city":item.city,"province":item.province,"country":item.country,"postcode":item.postcode}, 'statuscode': 200, 'message': 'success'}
        else:
            return {'address': {}, 'statuscode': 200, 'message': 'success'}

    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}


@api.post('address',auth=AuthClass())
def createaddress(request,addr:addressSchema):
    try:
        user = Token.objects.get(key=request.auth).user
        address=Address.objects.filter(user_id=user.id).first()
        if not address:
            address=Address()
        address.line1=addr.line1
        address.line2=addr.line2
        address.city=addr.city
        address.province=addr.province
        address.country=addr.country
        address.postcode=addr.postcode
        address.user=user
        address.save()
        return {'address': {"id":address.id,"line1":address.line1,"line2":address.line2,"city":address.city,"province":address.province,"country":address.country,"postcode":address.postcode}, 'statuscode': 200, 'message': 'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}



@api.patch('address',auth=AuthClass())
def updateaddress(request,addr:addressSchema):
    try:
        address=Address.objects.filter(id=addr.id).first()
        address.line1 = addr.line1
        address.line2 = addr.line2
        address.city = addr.city
        address.province = addr.province
        address.country = addr.country
        address.postcode = addr.postcode
        address.save()
        return {'address': {"id": address.id, "line1": address.line1, "line2": address.line2, "city": address.city,
                            "province": address.province, "country": address.country, "postcode": address.postcode},
                'statuscode': 200, 'message': 'success'}
    except Exception as exc:
        return {"message":exc.args[1],'statuscode':400}

#pk_test_51JlhHTAIj4VUJPcDeLGSFO23zCFWywO8QCsU6jwKzYBtgAeUzC3USVd28e9q71Msxcc5ZMPQRBGO5h0V2xbHefhQ00xEanG3at

# {
#   "catid": "1",
#   "catname": "Dry Cleaning",
#   "name": "Cashmere Knitwear",
#   "id": "2",
#   "price": 7.5,
#   "qty": 1,
#   "total": 7.5
# }

