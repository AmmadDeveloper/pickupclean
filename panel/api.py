from django.contrib.auth import authenticate
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from models.models import Category, Files, Service, Order, Cart, PostCode, TimeSlot, ScheduleConfig, EmailConfig, \
    PhoneConfig, Promo, HomeBackground, PaymentIntent, Notification, NotificationRead, PromoUsage, ServiceType, \
    EmailRecord, MessageRecord
from rest_framework.authtoken.models import Token
from .schema import CategorySchema,AuthenticationSchema,ServiceSchema,PostCodeSchema,SettingSchema,PromoSchema,EmailSendSchema,PhoneSendSchema,ServiceTypeSchema
from ninja.files import UploadedFile
from twilio.rest import Client
from models.models import Message
from models.utils.Constants import OrderType
from django.conf import settings
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractYear
from django.db.models import Q
import datetime
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        user = Token.objects.get(key=token).user
        if user and user.is_superuser:
            return token
        else:
            return "invalid creds"

api = NinjaAPI(auth=GlobalAuth(),version='1.0.0')

@api.post("/token", auth=None)  # < overriding global auth
def get_token(request, user:AuthenticationSchema):
    user=authenticate(email=user.email,password=user.password)
    if user and user.is_superuser:
        token=Token.objects.filter(user_id=user.id).first()
        return {"token": token.key,"message":"Success","statuscode":200}
    else:
        return {"message":"Invalid Email or Password","statuscode":404}


@api.post("/upload",auth=None)
def upload(request, file: UploadedFile):
    f=Files()
    f.File=file
    f.save()
    return {'name': f.File.url,'statuscode':200,'message':'success'}


@api.post("/bgupload",auth=None)
def upload(request, file: UploadedFile):
    f=HomeBackground()
    f.File=file
    f.save()
    return {'name': f.File.url,'statuscode':200,'message':'success'}

from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

@api.get('/dashboard')
def getData(request):
    total_users=User.objects.filter(is_superuser=False,is_staff=False).count()
    total_month_sales=(Order.objects.filter(paid=True,order_status__in=['delivered','confirmed','processing','completed','in-progress'],order_date__gte=now()-timedelta(days=30)).aggregate(Sum('order_amount'))).get('order_amount__sum')
    if total_month_sales:
        total_month_sales=round(float(total_month_sales),2)
    else:
        total_month_sales=0
    total_year_sales = (Order.objects.filter(paid=True,order_status__in=['delivered','confirmed','processing','completed','in-progress'], order_date__gte=now() - timedelta(days=365)).aggregate(
        Sum('order_amount'))).get('order_amount__sum')
    if total_year_sales:
        total_year_sales=round(float(total_year_sales),2)
    else:
        total_year_sales=0
    total_pending_orders=Order.objects.filter(order_status__in=['in-progress']).count()
    return {"data":{"total_users":total_users,"total_month_sales":total_month_sales,"total_year_sales":total_year_sales,"total_pending_orders":total_pending_orders},'statuscode':200,'message':'success'}


from django.db.models import Count
@api.get('/orderstatus')
def getOrderStatus(request):
    vals=Order.objects.all().values('order_status').annotate(total=Count('order_status')).order_by('order_status')
    resp=[]
    for item in vals:
        resp.append({"type":item.get('order_status'),"value":item.get('total')})
    return {"data":resp,'statuscode':200,'message':'success'}

@api.get('/sales')
def getSales(request,span:str):
    resp=[]
    if span=="weekly":
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        week = Order.objects.filter(order_date__gte=now()-timedelta(days=7)).annotate(weekday=ExtractWeekDay('order_date')).values('weekday').annotate(count=Sum('order_amount'),total=Sum('order_amount')).values('weekday','total', 'count')
        for vals in week:
            resp.append({"day":vals.get("weekday"),"label":weekdays[vals.get("weekday")-1],"amount":float(round(vals.get("total"),1))})
            resp = sorted(resp, key=lambda d: d['day'])
        resp = [{k: v for k, v in d.items() if k != 'day'} for d in resp]
    elif span=="monthly":
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = Order.objects.filter(order_date__gte=now()-timedelta(days=30)).annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id'),total=Sum('order_amount')).values('month', 'count', 'total')
        for vals in month:
            resp.append({"month":vals.get("month"),"label":months[vals.get("month")-1],"amount":float(round(vals.get("total"),1))})
            resp = sorted(resp, key=lambda d: d['month'])
        resp = [{k: v for k, v in d.items() if k != 'month'} for d in resp]
    elif span=="yearly":
        years = Order.objects.filter(order_date__gte=now()-timedelta(days=365)).annotate(year=ExtractYear('order_date')).values('year').annotate(count=Count('id'),total=Sum('order_amount')).values('year', 'count', 'total')
        for vals in years:
            resp.append({"year":vals.get("year"),"label":str(vals.get('year')),"amount":float(round(vals.get("total"),1))})
            resp = sorted(resp, key=lambda d: d['year'])
        resp = [{k: v for k, v in d.items() if k != 'year'} for d in resp]

    return {"data":resp,'statuscode':200,'message':'success'}

@api.get('/orderarea')
def getOrderArea(request):
    items=Order.objects.all().values('ship_postal_code').annotate(total=Count('ship_postal_code'))
    dic={}
    resp=[]
    for item in items:
        code=item.get('ship_postal_code').split(' ')[0]
        if code in dic.keys():
            dic[code]+=item.get('total')
        else:
            dic[code]=item.get('total')
    for key,val in dic.items():
        resp.append({"name":key,"value":val})
    return {"data":{"name":"root","children":resp},'statuscode':200,'message':'success'}

@api.delete('/block')
def BlockCustomer(request,id:int):
    customer=User.objects.filter(id=id).first()
    customer.is_active=False
    customer.save()
    return {'statuscode':200,'message':'success'}


@api.get('/contact')
def getContacts(request,name:str):
    query = Q()
    query.add(Q(first_name__icontains=name), Q.OR)
    query.add(Q(last_name__icontains=name), Q.OR)
    users=[{"firstname":user.first_name,"lastname":user.last_name,"id":user.id,"email":user.email,"phone":[x.phone for x in user.electronic_address.all()]} for user in User.objects.filter(query).prefetch_related('electronic_address')][0:5]
    return {'users':users,'statuscode':200,'message':'success'}
@api.get('/order/')
def getOrder(request,status:str=None,fromdate:str=None,todate:str=None,search:str=None):
    query = Q()
    query.add(~Q(order_status=OrderType.OPEN),Q.AND)
    if status and status!='all':
        query.add(Q(order_status=status), Q.AND)
    if fromdate:
        query.add(Q(order_place_date__gte=fromdate), Q.AND)
    if todate:
        query.add(Q(order_place_date__lte=todate), Q.AND)
    if search:
        query.add((Q(id=search)), Q.AND)

    orders=[
        {
            'key':order.id,
            'id':order.id,
            'fullname':order.fullname,
            'email':order.email,
            'phone':order.phone,
            'status':order.order_status,
            'total':"£ "+str(round(order.order_amount,2)) if order.order_amount else '',
            'postcode':order.ship_postal_code,
            'order_date':order.order_place_date.strftime('%d-%B-%Y') if order.order_place_date else ''
        }
            for order in Order.objects.filter(query).order_by('-order_place_date')]
    return {'orders':orders,'statuscode':200,'message':'success'}

@api.get('/notifications/')
def getNotifications(request,id:int=None):
    user = Token.objects.get(key=request.auth).user
    if id:
        read = NotificationRead()
        read.notification_id = id
        read.user = user
        read.save()
    notificationread=[n.notification.id for n in NotificationRead.objects.filter()]
    notifications=[{"heading":n.heading,"message":n.message,"created_on":n.created_on,"id":n.id,"key":n.id} for n in Notification.objects.filter().order_by('-created_on') if n.id not in notificationread]
    return {'notifications':notifications,'nums':len(notifications),'statuscode':200,'message':'success'}



@api.get('/marknotifications/')
def markasread(request):
    user = Token.objects.get(key=request.auth).user
    notifications = [n.id for n in
                     Notification.objects.filter().order_by('-created_on')]
    reads=[NotificationRead(notification_id=id,user = user) for id in notifications if len(NotificationRead.objects.filter(notification_id=id).all())==0]
    objs=NotificationRead.objects.bulk_create(reads)
    return {'statuscode':200,'message':'success'}


@api.patch('/orderstatus/')
def updateOrderStatus(request,id:int,status:str):
    order = Order.objects.filter(id=id).prefetch_related('ordercart', 'order_intent').first()
    order.order_status=status
    order.save()
    cartdata = [{
        "id": item.id,
        "serviceid": item.service.id,
        "servicename": item.service.name,
        "categoryid": item.category.id,
        "categoryname": item.category.name,
        "categoryimage": item.category.icon.url[6:],
        "price": item.price,
        "quantity": item.qty,
        "total": item.total
    } for item in order.ordercart.all()]

    paymentdata = [
        {"id": item.id, "amount": item.amount, "refund": item.refund,
         "refund_date": item.refund_date.strftime("%B %d,%y") if item.refund_date else ''} for item in
        order.order_intent.all()
    ][0]

    res = {
        "item_count": len(cartdata),
        "id": order.id,
        "order_date": order.order_place_date.strftime("%B %d,%y") if order.order_place_date else '',
        "fullname": order.fullname,
        "email": order.email,
        "phone": order.phone,
        "paymentdata": paymentdata,
        "cartdata": cartdata,
        "status": order.order_status,
        "totalamount": "£" + str(round(order.order_amount, 2)),
        "paid": order.paid,
        "pickup_date": order.pickup_date.strftime("%B %d,%y"),
        "dropoff_date": order.dropoff_date.strftime("%B %d,%y"),
        "pickup_time": order.pickup_time_slot,
        "dropoff_time": order.dropoff_time_slot,
        "address": order.__fulladdress__()
    }

    return {'order': res, 'statuscode': 200, 'message': 'success'}


@api.get('/orderdetail/')
def getOrderDetailById(request,id:int):
    order=Order.objects.filter(id=id).prefetch_related('ordercart','order_intent').first()

    cartdata=[{
        "id":item.id,
        "serviceid":item.service.id,
        "servicename": item.service.name,
        "categoryid": item.category.id,
        "categoryname": item.category.name,
        "categoryimage":item.category.icon.url[6:],
        "price":item.price,
        "quantity":item.qty,
        "total":item.total
    } for item in order.ordercart.all()]

    paymentdata=[
        {"id":item.id,"amount":item.amount,"refund":item.refund,"refund_date":item.refund_date.strftime("%B %d,%y") if item.refund_date else ''} for item in order.order_intent.all()
    ][0]

    res={
        "item_count":len(cartdata),
        "id":order.id,
        "order_date":order.order_place_date.strftime("%B %d,%y") if order.order_place_date else '',
        "fullname":order.fullname,
        "email":order.email,
        "phone":order.phone,
        "paymentdata":paymentdata,
        "cartdata":cartdata,
        "status":order.order_status,
        "totalamount":"£"+str(round(order.order_amount,2)),
        "paid":order.paid,
        "pickup_date":order.pickup_date.strftime("%B %d,%y"),
        "dropoff_date":order.dropoff_date.strftime("%B %d,%y"),
        "pickup_time":order.pickup_time_slot,
        "dropoff_time":order.dropoff_time_slot,
        "address":order.__fulladdress__()
    }

    return {'order':res,'statuscode': 200, 'message': 'success'}

@api.get('/payment/')
def getPayments(request,status:str=None,fromdate:str=None,todate:str=None,search:str=None):
    query = Q()
    query.add(Q(order__paid=True),Q.AND)
    if status and status!='all':
        query.add(Q(refund=True), Q.AND)
    if fromdate:
        query.add(Q(order__order_place_date__gte=fromdate), Q.AND)
    if todate:
        query.add(Q(order__order_place_date__lte=todate), Q.AND)
    if search:
        query.add((Q(order_id=search)), Q.AND)

    payments=[{
        "refund":"Yes" if payment.refund else "No",
        'key': payment.id,
        "order_id":payment.order.id,
        "fullname":payment.order.fullname,
        "email":payment.order.email,
        "id":payment.id,
        "amount":"£ "+str(round(float(payment.amount)/100,2)),"date":payment.order.order_place_date.strftime('%d-%B-%Y') if payment.order.order_place_date else ''
    } for payment in PaymentIntent.objects.filter(query).order_by('-created_on')]
    return {'payments': payments, 'statuscode': 200, 'message': 'success'}


@api.delete('/payment')
def refundPayment(request,id:int):
    intent=PaymentIntent.objects.filter(id=id).first()
    res=stripe.Refund.create(
        payment_intent=intent.intentid,
    )
    if res.status=='succeeded':
        intent.refund=True
        intent.refund_date=datetime.datetime.now()
        intent.order.order_status=OrderType.REFUND
        intent.save()
        intent.order.save()
        return {'statuscode': 200, 'message': 'success'}
    else:
        return {'statuscode': 400, 'message': 'error'}


@api.get('listEmail/')
def getEmailRecord(request):
    recs=[{"id":rec.id,"recipient_type":rec.recipient_type,"subject":rec.subject,"created_on":rec.created_on.strftime("%d %B %Y"),"status":rec.status,"key":rec.id} for rec in EmailRecord.objects.filter().order_by('-created_on')]
    return {"records":recs,'statuscode': 200, 'message': 'success'}

@api.get('listMessages/')
def getSmsRecord(request):
    recs = [{"id": rec.id, "recipient_type": rec.recipient_type,
             "created_on": rec.created_on.strftime("%d %B %Y"), "status": rec.status, "key": rec.id} for rec in
            MessageRecord.objects.filter().order_by('-created_on')]
    return {"records": recs, 'statuscode': 200, 'message': 'success'}


@api.post('sendEmail/')
def sendMail(request,emailSchema:EmailSendSchema):
    user = Token.objects.get(key=request.auth).user
    record=EmailRecord()
    record.body=emailSchema.body
    record.subject=emailSchema.subject
    record.created_by=user
    record.recipient_type=emailSchema.to
    record.recipients=str(emailSchema.emails) if emailSchema.to!='all' else "['all']"

    c = {
        'body':emailSchema.body
    }
    subject = emailSchema.subject
    template = get_template("email/MarketingEmail.html")
    email = template.render(c)
    # email = loader.render_to_string(email_template_name, c)
    #send_mail(subject,message="Hello world", from_email='suitclosset@gmail.com', to=["ammadhassanqureshi@gmail.com","ammad.development@gmail.com"], fail_silently=False,html_message=email)
    if emailSchema.to=='all':
        emails=[x.email for x in User.objects.filter()]
    else:
        emails=emailSchema.emails
    msg=EmailMultiAlternatives(subject,body=email, from_email='suitclosset@gmail.com', bcc=emails)
    msg.attach_alternative(email, "text/html")
    try:
        s=msg.send(fail_silently=False)
        if s == 1:
            record.status = "sent"
            record.status_message = "email sent"
            record.save()
    except Exception as exe:
        record.status = "error"
        record.status_message = str(exe.args[1])
        record.save()
        return {'statuscode': 200,'statusmessge':'Your email was not sent', 'message': 'error'}
    recs = [{"id": rec.id, "recipient_type": rec.recipient_type, "subject": rec.subject,
             "created_on": rec.created_on.strftime("%d %B %Y"), "status": rec.status, "key": rec.id} for rec in
            EmailRecord.objects.filter().order_by('-created_on')]
    return {"records": recs, 'statuscode': 200,'statusmessge':'Your email was sent', 'message': 'success'}

@api.post('sendSms/')
def sendMessages(request,data:PhoneSendSchema):
    record = MessageRecord()
    try:
        user = Token.objects.get(key=request.auth).user
        record = MessageRecord()
        record.body = data.body
        record.created_by = user
        record.recipient_type = data.to
        record.recipients = str(data.phones) if data.to != 'all' else "['all']"
        if data.to == 'all':
            phones=[]
            rec = [x.electronic_address.first() for x in User.objects.filter().prefetch_related('electronic_address')]
            for i in rec:
                if i!=None:
                    phones.append(i.phone)
        else:
            phones = data.phones
        bindings = list(map(lambda number: json.dumps({'binding_type': 'sms', 'address': number}), phones))
        response = client.notify.services(settings.NOTIFY_SID).notifications.create(
            to_binding=bindings,
            body=data.body
        )

        # response = client.messages \
        #     .create(
        #     body='Hello tabtab this is a new message',
        #     from_=settings.PHONE_NUMBER,
        #     status_callback='https://992b-182-185-167-180.ap.ngrok.io/sms/status',
        #     to='+923130452101'
        # )
        message = Message()
        message.sid = response.sid
        message.body = response.body
        message.accountsid = response.account_sid
        message.status = "sent"
        message.error_message = ""
        message.error_code = ""
        message.sent_to = "marketing"
        message.uri = ""
        message.sent_from = settings.PHONE_NUMBER
        message.save()
        record.sid=response.sid
        record.status = "sent"
        record.status_message = "message sent"
        record.save()
        recs = [{"id": rec.id, "recipient_type": rec.recipient_type,
                 "created_on": rec.created_on.strftime("%d %B %Y"), "status": rec.status, "key": rec.id} for rec in
                MessageRecord.objects.filter().order_by('-created_on')]
        return {"records": recs, 'statuscode': 200, 'statusmessge': 'Your messages has been sent','message': 'success'}
    except Exception as exe:
        record.status = "error"
        record.status_message = str(exe.args[1])
        record.save()
        return {'statuscode': 200, 'statusmessge': 'Your message was not sent', 'message': 'error'}






@api.get('/customer/')
def getCustomer(request):
    customers=[
        {
            'key': user.id,
            'id':user.id,
            'fullname':user.first_name+" "+user.last_name,
            'lastlogin':user.last_login.strftime('%d-%B-%Y ') if user.last_login else '',
            'email':user.email,
            'active':'True' if user.is_active else 'False',
            'total_orders':Order.objects.filter(user_id=user.id).count()
        }
            for user in User.objects.filter(is_staff=False,is_superuser=False).order_by('-date_joined')]
    return {'users':customers,'statuscode':200,'message':'success'}


@api.get('/homeimages')
def homeimages(request):
    imgs=[{"uid":img.id,"name":img.File.name,"status":'done',"url":img.File.url} for img in HomeBackground.objects.all().order_by('-created_on')[0:5]]
    return {'images':imgs,'statuscode':200,'message':'success'}


@api.get('/settings')
def get_settings(request):
    setting={}
    sch = ScheduleConfig.objects.all()
    emailConf = EmailConfig.objects.all()
    phoneConf = PhoneConfig.objects.all()
    if len(sch) == 0:
        setting['schedule']={'monday':[],'tuesday':[],'wednesday':[],'thursday':[],'friday':[],'saturday':[]}
    else:
        vals=eval(sch[0].value)
        setting['schedule']={}
        for k,v in vals.items():
            setting['schedule'][v.get('day')]=[v.get('start').strftime('%Y-%m-%d %H:%M:%S'),v.get('end').strftime('%Y-%m-%d %H:%M:%S')]
    if len(emailConf) == 0:
        setting['emailConfig']={'email':'','password':''}
    else:
        setting['emailConfig']={
            'email':emailConf[0].email,
            'password':emailConf[0].password
        }
    if len(sch) == 0:
        setting['phoneConfig']={'phone':''}
    else:
        setting['phoneConfig']={
            'phone':phoneConf[0].phone
        }
    setting['paymentConfig']={}
    setting['paymentConfig']['publishablekey']=settings.STRIPE_PUBLISHABLE_KEY
    setting['paymentConfig']['secretkey'] = settings.STRIPE_SECRET_KEY

    return {'settings': setting, 'statuscode': 200, 'message': 'success'}




@api.post('/settings')
def update_settings(request,settings:SettingSchema):
    schedule={}
    response={}
    weekdays=['monday','tuesday','wednesday','thursday','friday','saturday']
    for k,v in settings.schedule.items():
        schedule[str(weekdays.index(k)+1)]={}
        schedule[str(weekdays.index(k)+1)]['start']=datetime.datetime.strptime(v[0], '%Y-%m-%d %H:%M:%S')
        schedule[str(weekdays.index(k)+1)]['end'] = datetime.datetime.strptime(v[1], '%Y-%m-%d %H:%M:%S')
        schedule[str(weekdays.index(k)+1)]['day']=k
    sch=ScheduleConfig.objects.all()
    emailConf=EmailConfig.objects.all()
    phoneConf=PhoneConfig.objects.all()
    if len(sch)==0:
        sch=ScheduleConfig()
        sch.value=str(schedule)
        # di=eval(sch.value)
        sch.save()
        response['schedule']=schedule
    else:
        sch[0].value=str(schedule)
        sch[0].updated_on=datetime.datetime.now()
        sch[0].save()
        response['schedule'] = schedule

    if len(emailConf)==0:
        emailConf=EmailConfig()
        emailConf.email=settings.emailConfig.get("email")
        emailConf.password=settings.emailConfig.get("password")
        emailConf.updated_on=datetime.datetime.now()
        emailConf.save()
        response['emailConfig'] = emailConf
    else:
        emailConf[0].email = settings.emailConfig.get("email")
        emailConf[0].password = settings.emailConfig.get("password")
        emailConf[0].updated_on = datetime.datetime.now()
        emailConf[0].save()
        response['emailConfig'] = emailConf[0]
    if len(phoneConf)==0:
        phoneConf=PhoneConfig()
        phoneConf.phone=settings.phoneConfig.get("phone")
        phoneConf.updated_on=datetime.datetime.now()
        phoneConf.save()
        response['phoneConfig']=phoneConf
    else:
        phoneConf[0].phone = settings.phoneConfig.get("phone")
        phoneConf[0].updated_on = datetime.datetime.now()
        phoneConf[0].save()
        response['phoneConfig'] = phoneConf[0]

    return {'settings':settings,'statuscode':200,'message':'Your settings has been successfully updated!'}


# Category APIS
@api.post('/category')
def create_category(request,category:CategorySchema):
    Cat=Category()
    Cat.name=category.name
    Cat.icon=category.icon
    Cat.description=category.description
    Cat.short_description = category.short_description
    Cat.picture=category.picture
    user = Token.objects.get(key=request.auth).user
    Cat.created_by=user
    Cat.save()
    return {'category':{"id":Cat.id,"name":Cat.name,"description":Cat.description,"key":Cat.id},'statuscode':200,'message':'success'}

@api.patch('/category')
def update_category(request,category:CategorySchema):
    Cat=Category.objects.filter(id=category.id).first()
    Cat.name=category.name
    Cat.icon=category.icon
    Cat.description=category.description
    Cat.short_description=category.short_description
    Cat.picture=category.picture
    user = Token.objects.get(key=request.auth).user
    Cat.created_by=user
    Cat.save()
    Cat = [{"id": cat.id, "name": cat.name, "description": cat.description, "key": cat.id} for cat in
           Category.objects.filter(active=True)]
    return {'categories': Cat, 'statuscode': 200, 'message': 'success'}


@api.get('/types')
def get_types(request,id:int=None):
    if not id:
        Types=[{"id":t.id,"name":t.name,"description":t.description,"key":t.id} for t in ServiceType.objects.filter(active=True)]
        return {'types':Types,'statuscode':200,'message':'success'}
    else:
        type=[{"id": t.id, "name": t.name, "description": t.description,"picture_path":t.picture.url[6:],"picture":t.picture.url[6:], "key": t.id} for t in ServiceType.objects.filter(id=id,active=True)][0]
        type['picture'] = [{
            'uid': type.get('id'),
            'name': type.get('picture').split('/')[-1],
            'status': 'done',
            'url': type.get('picture'),
            'thumbUrl': type.get('picture'),
        }]
        return {'type': type, 'statuscode': 200, 'message': 'success'}

@api.post('/types')
def save_type(request,type:ServiceTypeSchema):
    st=ServiceType()
    st.name=type.name
    st.description = type.description
    st.picture = type.picture
    user = Token.objects.get(key=request.auth).user
    st.created_by = user
    st.save()
    return {'type': {"id": st.id, "name": st.name,"description":st.description, "key": st.id}, 'statuscode': 200, 'message': 'success'}

@api.patch('/types')
def update_type(request,type:ServiceTypeSchema):
    st=ServiceType.objects.filter(id=type.id).first()
    st.name=type.name
    st.description = type.description
    st.picture = type.picture
    user = Token.objects.get(key=request.auth).user
    st.created_by = user
    st.save()
    Types = [{"id": t.id, "name": t.name, "description": t.description, "key": t.id} for t in
             ServiceType.objects.filter(active=True)]
    return {'types': Types, 'statuscode': 200, 'message': 'success'}

@api.delete('/types')
def delete_type(request,id:int):
    type=ServiceType.objects.get(id=id)
    type.active=False
    type.save()
    return {'statuscode':200,'message':'success'}


@api.get('/category')
def get_category(request,id:int=None):
    if not id:
        Cat=[{"id":cat.id,"name":cat.name,"description":cat.description,"key":cat.id} for cat in Category.objects.filter(active=True)]
        return {'categories':Cat,'statuscode':200,'message':'success'}
    else:
        category=[{"id": cat.id, "name": cat.name, "description": cat.description,"short_description":cat.short_description,"icon_path":cat.icon.url[6:],"picture_path":cat.picture.url[6:],"icon":cat.icon.url[6:],"picture":cat.picture.url[6:], "key": cat.id} for cat in Category.objects.filter(id=id,active=True)][0]
        category['icon']=[{
            'uid': category.get('id'),
            'name': category.get('icon').split('/')[-1],
            'status': 'done',
            'url': category.get('icon'),
            'thumbUrl': category.get('icon'),
          }]
        category['picture'] = [{
            'uid': category.get('id'),
            'name': category.get('picture').split('/')[-1],
            'status': 'done',
            'url': category.get('picture'),
            'thumbUrl': category.get('picture'),
        }]
        return {'category': category, 'statuscode': 200, 'message': 'success'}


@api.delete('/category')
def delete_category(request,id:int):
    Cat=Category.objects.get(id=id)
    Cat.active=False
    Cat.save()
    return {'statuscode':200,'message':'success'}


# Services APIS
@api.post('/service')
def create_service(request,service:ServiceSchema):
    Ser=Service()
    Ser.name=service.name
    Ser.servicetype_id=service.type_id
    Ser.description=service.description
    Ser.price=service.price
    Ser.category_id=service.category_id
    Ser.delivery_time=service.delivery_time
    user = Token.objects.get(key=request.auth).user
    Ser.created_by=user
    Ser.save()
    return {'service':{"id":Ser.id,"name":Ser.name,"delivery_time":Ser.delivery_time,"price":Ser.price,"key":Ser.id},'statuscode':200,'message':'Your service has been successfully created'}

@api.get('/service')
def get_service(request,id:int=None):
    if not id:
        Ser=[{"id":Ser.id,"name":Ser.name,"delivery_time":Ser.delivery_time,"price":Ser.price,"key":Ser.id} for Ser in Service.objects.filter(is_available=True)]
        return {'services':Ser,'statuscode':200,'message':'success'}
    else:
        Serv = [{"id": Ser.id, "name": Ser.name, "delivery_time": Ser.delivery_time,"description":Ser.description, "price": Ser.price,"cat":Ser.category.id,"type_id":Ser.servicetype.id,"category_id":Ser.category.id, "key": Ser.id}
               for Ser in Service.objects.filter(is_available=True,id=id)][0]
        return {'service': Serv, 'statuscode': 200, 'message': 'success'}

@api.patch('/service')
def update_service(request,service:ServiceSchema):
    Ser = Service.objects.filter(id=service.id).first()
    Ser.name = service.name
    Ser.servicetype_id=service.type_id
    Ser.description = service.description
    Ser.price = service.price
    Ser.category_id = service.category_id
    Ser.delivery_time = service.delivery_time
    user = Token.objects.get(key=request.auth).user
    Ser.created_by = user
    Ser.save()
    Ser = [{"id": Ser.id, "name": Ser.name, "delivery_time": Ser.delivery_time, "price": Ser.price, "key": Ser.id} for
           Ser in Service.objects.filter(is_available=True)]
    return {'services': Ser, 'statuscode': 200, 'message': 'updated successfully'}


@api.delete('/service')
def delete_service(request,id:int):
    Ser=Service.objects.get(id=id)
    Ser.is_available=False
    Ser.save()
    return {'statuscode':200,'message':'success'}


#PostCode APIS
@api.post('/postcode')
def create_postcode(request,postcode:PostCodeSchema):
    post=PostCode()
    post.name=postcode.name
    post.description=postcode.description
    post.code=postcode.code
    post.country=postcode.country
    user = Token.objects.get(key=request.auth).user
    post.created_by = user
    post.save()
    return {'postcode':{"id":post.id,"name":post.name,"description":post.description,"code":post.code,"country":post.country,"key":post.id},'statuscode':200,'message':'success'}

@api.get('/postcode')
def get_postcode(request,id:int=None):
    if not id:
        Pcode=[{"id":post.id,"name":post.name,"description":post.description,"code":post.code,"country":post.country,"key":post.id} for post in PostCode.objects.filter(active=True)]
        return {'postcodes':Pcode,'statuscode':200,'message':'success'}
    else:
        res=[{"id": post.id, "name": post.name, "description": post.description, "code": post.code, "country": post.country,"key": post.id} for post in PostCode.objects.filter(active=True,id=id)][0]
        return {"postcode":res,'statuscode':200,'message':'success'}

@api.patch('/postcode')
def edit_postcode(request,postcode:PostCodeSchema):
    pcode=PostCode.objects.filter(id=postcode.id).first()
    pcode.name=postcode.name
    pcode.country=postcode.country
    pcode.code=postcode.code
    pcode.description=postcode.description
    pcode.save()
    Pcodes = [
        {"id": post.id, "name": post.name, "description": post.description, "code": post.code, "country": post.country,
         "key": post.id} for post in PostCode.objects.filter(active=True)]
    return {'postcodes':Pcodes,'statuscode':200,'message':'success'}

@api.delete('/postcode')
def delete_postcode(request,id:int):
    post=PostCode.objects.get(id=id)
    post.active=False
    post.save()
    return {'statuscode':200,'message':'success'}


#PROMOS APIS
@api.post('/promo')
def create_promo(request,promo:PromoSchema):
    promoCode=Promo()
    promoCode.title=promo.title
    promoCode.until=promo.until
    promoCode.type=promo.type
    promoCode.value=promo.value
    user = Token.objects.get(key=request.auth).user
    promoCode.user = user
    promoCode.code=get_random_string(6)
    promoCode.save()
    return {'promo':{"id":promoCode.id,"title":promoCode.title,"until":promoCode.until,"value":promoCode.value,"code":promoCode.code,"type":promoCode.type,"key":promoCode.id},'statuscode':200,'message':'success'}

@api.get('/promo')
def get_promo(request):
    Promos=[{"id":promoCode.id,"title":promoCode.title,"until":promoCode.until.strftime("%B %d,%Y") if promoCode.until else '',"value":promoCode.value,"code":promoCode.code,"type":promoCode.type,"key":promoCode.id} for promoCode in Promo.objects.filter(active=True)]
    return {'promo':Promos,'statuscode':200,'message':'success'}


@api.delete('/promo')
def delete_promo(request,id:int):
    promo=Promo.objects.get(id=id)
    promo.active=False
    promo.save()
    return {'statuscode':200,'message':'success'}


import json

@api.get('/sendsms',auth=None)
def sendsms(request):
    bindings = list(map(lambda number: json.dumps({'binding_type': 'sms', 'address': number}), ['+923130452101','+923045171619']))
    print("=====> To Bindings :>", bindings, "<: =====")
    response = client.notify.services(settings.NOTIFY_SID).notifications.create(
        to_binding=bindings,
        body="Hello this is broadcast"
    )


    # response = client.messages \
    #     .create(
    #     body='Hello tabtab this is a new message',
    #     from_=settings.PHONE_NUMBER,
    #     status_callback='https://992b-182-185-167-180.ap.ngrok.io/sms/status',
    #     to='+923130452101'
    # )
    message=Message()
    message.sid=response.sid
    message.body=response.body
    message.accountsid=response.account_sid
    message.status=response.status
    message.error_message=response.error_message
    message.error_code=response.error_code
    message.sent_to=response.to
    message.uri=response.uri
    message.sent_from=settings.PHONE_NUMBER
    message.save()
    return {'statuscode':200,'message':'success'}


#SMe4c93b75288c4bdcada0adbea5827b2f


