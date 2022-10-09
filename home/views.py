import datetime
import functools
import json
import random
import string

import requests
from django.db.models import Min
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from twilio.rest import Client
from models.models import Category, Message, PostCode, Electronic_Address, Order, Cart, PaymentIntent, UserVerification, \
    PromoUsage, ServiceType, EmailCode, PhoneCode, ScheduleConfig, HomeBackground
from models.utils.Constants import OrderType
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as lout, authenticate,login as lin
from .forms import loginform,signupform
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.db.models.query_utils import Q
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

# Create your views here.
def home(request):
    if request.method=="GET":
        cats=[{"name":cat.name,"icon":cat.icon,"short_desc":cat.short_description,"price":cat.category_products.aggregate(price=Min('price'))} for cat in Category.objects.filter(active=True).prefetch_related('category_products')[0:4]]
        imgs=[{
        "src": img.File.url,
        "theme": 'light',
        "title": 'Laundary Mess?',
        "description": 'Dont worry we are here for you'
      } for img in HomeBackground.objects.filter().order_by('-created_on')[0:5]]
        return render(request,'index.html',{"categories":cats,"background":imgs})
    elif request.method=="POST":
        if request.user.is_authenticated:
            if request.POST.get('pickup_date') !='' and request.POST.get('dropoff_date')!='':
                ord = Order.objects.filter(user_id=request.user.id, order_status=OrderType.OPEN).first()
                eaddress=Electronic_Address.objects.filter(user_id=request.user.id).first()
                if not ord:
                    ord=Order()
                    ord.fullname=request.user.first_name+" "+request.user.last_name
                    ord.email=request.user.email
                    if eaddress!=None:
                        ord.phone=eaddress.phone
                    ord.ship_address1=request.POST.get('address_line1')
                    ord.ship_address2 = request.POST.get('address_line2')
                    ord.ship_address3 = request.POST.get('address_line3')
                    ord.ship_address4 = request.POST.get('address_line4')
                    ord.ship_postal_code=request.POST.get('postcode')
                    ord.ship_country = request.POST.get('country')
                    ord.ship_city = request.POST.get('city')
                    ord.pickup_date = request.POST.get('pickup_date')
                    ord.dropoff_date = request.POST.get('dropoff_date')
                    ord.pickup_time_slot = request.POST.get('pickup_time_slot')
                    ord.dropoff_time_slot=request.POST.get('dropoff_time_slot')
                    ord.user_id=request.user.id
                    ord.save()
                else:
                    ord.ship_address1 = request.POST.get('address_line1')
                    ord.ship_address2 = request.POST.get('address_line2')
                    ord.ship_address3 = request.POST.get('address_line3')
                    ord.ship_address4 = request.POST.get('address_line4')
                    ord.ship_postal_code = request.POST.get('postcode')
                    ord.ship_country = request.POST.get('country')
                    ord.ship_city = request.POST.get('city')
                    ord.pickup_date = request.POST.get('pickup_date')
                    ord.dropoff_date = request.POST.get('dropoff_date')
                    ord.pickup_time_slot = request.POST.get('pickup_time_slot')
                    ord.dropoff_time_slot = request.POST.get('dropoff_time_slot')
                    ord.save()
                return redirect('/orderdetail')
            else:
                return redirect('/')
        else:
            return redirect('/login')

@login_required()
def orderdetail(request):
    promo=request.session.get('promo')
    if promo is not None:
        del request.session['promo']
    return render(request,'orderdetail.html')

def login(request):
    if request.method=="GET":
        site_key=settings.GOOGLE_CAPTCHA_SITE_KEY
        return render(request, 'account/login.html',{'sitekey':site_key})
    if request.method == "POST":
        lform = loginform(request.POST or None)
        userinput = request.POST.get('g-recaptcha-response')
        res = requests.post('https://www.google.com/recaptcha/api/siteverify',
                            data={'secret': settings.GOOGLE_CAPTCHA_SECRET_KEY, 'response': userinput})
        resdict = json.loads(res.content)
        if resdict.get('success'):
            if (lform.is_valid()):
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user == None:
                    messages.error(request,'Email or password provided is incorrect!')
                    return redirect('login')
                else:
                    lin(request, user,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('homepage')
            else:
                messages.error(request, 'Please enter valid information!')
                return render(request, 'account/login.html')
    return render(request,'account/login.html')


def signup(request):
    if request.method=="GET":
        site_key = settings.GOOGLE_CAPTCHA_SITE_KEY
        return render(request, 'account/signup.html', {'sitekey': site_key})
    elif request.method=="POST":
        sform=signupform(request.POST or None)
        userinput = request.POST.get('g-recaptcha-response')
        res = requests.post('https://www.google.com/recaptcha/api/siteverify',
                            data={'secret': settings.GOOGLE_CAPTCHA_SECRET_KEY, 'response': userinput})
        resdict = json.loads(res.content)
        if resdict.get('success'):
            if(sform.is_valid()):
                try:
                    user=User.objects.create_user(password=request.POST['password'],email=request.POST['email'],username=request.POST['email'])
                    user.is_active=True
                    user.first_name=request.POST['first_name']
                    user.last_name=request.POST['last_name']
                    user.save()
                    eadd=Electronic_Address()
                    eadd.user=user
                    eadd.phone=request.POST['phone']
                    eadd.save()
                    UserVerification.objects.get_or_create(user_id=user.id, phone_verified=False, email_verified=False)
                    data = {"name": user.first_name + ' ' + user.last_name}
                    template = get_template("../../home/templates/email/signupemail.html")
                    html = template.render(data)
                    res = send_mail(subject="Welcome to Pick up clean", message="this is a message",
                                    from_email="suitclosset@gmail.com",
                                    recipient_list=[user.email]
                                    , fail_silently=False, html_message=html)
                    lin(request,user,backend='django.contrib.auth.backends.ModelBackend')
                except Exception as exc:
                    messages.error(request,message="User already exists")
                    return redirect('signup')
            else:
                return redirect('signup')
        return redirect('homepage')

def logout(request):
    lout(request)
    return redirect('homepage')

def privacy(request):
    return render(request,'privacy.html')

def instruction(request):
    return render(request,'instructions.html')

def price(request):
    types=[]
    services=[]
    query=ServiceType.objects.filter(active=True).prefetch_related('services')
    for q in query:
        types.append({"name":q.name,"desc":q.description})
        ser=[x for x in q.services.filter(is_available=True)]
        length=len(ser)
        if length>0:
            if length!=1:
                temp=[]
                temp2=[]
                for s in ser[0:round(length/2)]:
                    temp.append({"name":s.name+" - "+s.category.name,"price":s.price})
                for s in ser[round(length/2):]:
                    temp2.append({"name":s.name+" - "+s.category.name,"price":s.price})
                services.append([temp,temp2])
            else:
                services.append([[{"name":ser[0].name+" - "+ser[0].category.name,"price":ser[0].price}]])
        types[0]['active']="active"
    return render(request,'price.html',{"services":services,"types":types})



def setpassword(request, **kwargs):
    if request.method=='GET':
       return render(request,'setpassword.html',kwargs)
    elif request.method=="POST":
        uidb64 = request.POST.get('uidb64') or None
        token = request.POST.get('token') or None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST.get('confirmnewpassword')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset has been successful.')
        else:
            messages.error(request, 'Password reset has not been unsuccessful.')
        return redirect('login')




def resetpass(request):
    if request.method=="GET":
        return render(request,'reset-pass.html')
    elif request.method=="POST":
        data= request.POST.get('email')
        user= User.objects.filter(Q(email=data)).first()
        if user:
            c = {
                'email': user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'Picupclean',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': request.scheme,
            }
            subject = "Reset Your Password"
            template = get_template("email/password_reset_email.html")
            email = template.render(c)
            # email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, 'suitclosset@gmail.com' , [user.email], fail_silently=False)
        messages.success(request, 'An email has been sent to ' + data +" if it is a valid user.")
        return render(request,'reset-pass.html')


def services(request):
    data=[{"id":cat.id,"name":cat.name,"description":cat.description,"short_description":cat.short_description,"icon":cat.icon.url[6:]} for cat in Category.objects.filter(active=True)]
    return render(request,'services.html',{"Services":data})

def servicedetail(request,id):
    category=Category.objects.filter(id=id).prefetch_related('category_products')
    cats=[
        {
            "id":cat.id,
            "name":cat.name,
            "description":cat.description,
            "short_description":cat.short_description,
            "icon":cat.icon.url[6:],
            "picture":cat.picture.url[6:],
            "services":[{"name":ser.name,"price":ser.price,} for ser in cat.category_products.all()]
        } for cat in category]


    return render(request, 'services/servicedetail.html', {"category":cats[0]})


def getCancel(item):
    if timezone.now()>(item.order_date+datetime.timedelta(hours=24)) and item.order_status==OrderType.CANCELLED:
        return False
    elif timezone.now()>(item.order_date+datetime.timedelta(hours=24)) and item.order_status!=OrderType.CANCELLED :
        return False
    elif item.order_status==OrderType.CANCELLED:
        return False
    else:
        return True

def orderhistory(request):
    if request.user.is_authenticated:
        query=Q()
        query.add(Q(user_id=request.user.pk),Q.OR)
        query.add(~Q(order_status=OrderType.OPEN), Q.AND)

        orders=[{"orderid":item.id,
                 "orderstatus":item.order_status,
                 "orderdate":item.order_date.strftime("%B %d, %Y") if item.order_date else '',
                 "pickuptime": item.pickup_time_slot,
                 "pickupdate": item.pickup_date.strftime("%B %d, %Y") if item.pickup_date else '',
                 "dropofftime": item.dropoff_time_slot,
                 "dropoffdate": item.dropoff_date.strftime("%B %d, %Y") if item.dropoff_date else '',
                 "orderamount":float(item.order_amount),
                 "orderaddress":item.__fulladdress__(),
                 "cancel":getCancel(item),
                 'lines':[
                     {
                         "categoryname":line.category.name,
                         "quantity":line.qty,
                         "totalprice":line.total,
                         "price": line.price,
                         "productid": line.service.id,
                         "productname": line.service.name,
                         "image": line.category.icon.url[6:]

                     } for line in item.ordercart.all()]
                 }
                for item in Order.objects.prefetch_related('ordercart').filter(query).order_by('-order_date')]
        # for item in orders:
        #     item['lines']=[]
        #     for line in item.get('orderline'):
        #         cover = ProductImage.objects.filter(product_id=line.product.id, title="cover")
        #         image = [i.picture.url for i in cover][0]
        #         item['lines'].append({
        #                       "productid":line.product.id,
        #                       "productname":line.product.name,
        #                       "quantity":line.quantity,
        #                       "size":line.size,
        #                       "productprice":line.product.unit_price,
        #                       "totalprice":float(line.total),
        #                        "image":image
        #                       })
        return render(request,'orderhistory.html',{'orders':orders})
    else:
        return render(request,'orderhistory.html')



def get_random_string(length):
    # choose from all lowercase letter
    if length==80:
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    else:
        letters = string.digits
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

def callback(request):
    code=request.GET.get('code')
    ecode=EmailCode.objects.filter(code__iexact=code).first()
    if ecode:
        verification=UserVerification.objects.filter(user_id=ecode.user.id,email_verified=False).first()
        if verification:
            verification.email_verified=True
            verification.save()
        else:
            return render(request,'index.html')
    return render(request,'verified.html',{'address':'email'})

@login_required()
def verify_email(request):
    if request.method=="GET":
        user=request.user
        code=get_random_string(80)
        emailcode,created=EmailCode.objects.get_or_create(user_id=user.id)
        if emailcode:
            emailcode.code=code
            emailcode.user=request.user
            emailcode.save()
        data = {"name": user.first_name + ' ' + user.last_name,"url":f'{settings.BASE_URL}email/callback/?code={code}'}
        template = get_template("../../home/templates/email/emailverification.html")
        html = template.render(data)
        res = send_mail(subject="Email Verification", message="",
                        from_email="suitclosset@gmail.com",
                        recipient_list=[user.email]
                        , fail_silently=False, html_message=html)
        return render(request,'verifyemail.html')

@login_required()
def verify_phone(request,phone:str):
    if request.method=="GET":
        uphone=Electronic_Address.objects.filter(user_id=request.user.id).first()
        uphone.phone=phone
        uphone.save()
        code = get_random_string(6)
        phonecode, created = PhoneCode.objects.get_or_create(user_id=request.user.id)
        if phonecode:
            phonecode.code = code
            phonecode.user = request.user
            phonecode.save()
            response = client.messages \
                .create(
                body=f'Thanks for using picupclean your one time system generated code for phone verification is: {code}',
                from_=settings.PHONE_NUMBER,
                status_callback=f'{settings.SERVER_URL}sms/status',
                to=phone
            )
            message = Message()
            message.sid = response.sid
            message.body = response.body
            message.accountsid = response.account_sid
            message.status = response.status
            message.error_message = response.error_message
            message.error_code = response.error_code
            message.sent_to = response.to
            message.uri = response.uri
            message.sent_from = settings.PHONE_NUMBER
            message.save()
        return render(request,'verifyphone.html',{'phone':phone})
    elif request.method=="POST":
        data=request.POST.get('code') or None
        if data:
            pcode = PhoneCode.objects.filter(code__iexact=data).first()
            if pcode:
                verification = UserVerification.objects.filter(user_id=pcode.user.id, phone_verified=False).first()
                if verification:
                    verification.phone_verified = True
                    verification.save()
                else:
                    return render(request, 'index.html')
        return render(request,'verified.html',{'address':'phone'})


@login_required()
def profile(request):
    if request.method=="GET":
        eadd=Electronic_Address.objects.filter(user_id=request.user.id).first()
        phone=eadd.phone if eadd else ''
        # email_verified=
        verified=UserVerification.objects.get_or_create(user_id=request.user.id)[0]
        return  render(request,'profile.html',{"phone":phone,"phone_verified":verified.phone_verified,"email_verified":verified.email_verified})
    elif request.method=="POST":
        oldpass=request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        cnewpass = request.POST.get('cnewpass')
        user=authenticate(request,email=request.user.email,password=oldpass)
        if user and newpass==cnewpass:
            user.set_password(newpass)
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, "Your password didn't match.")

        eadd = Electronic_Address.objects.filter(user_id=request.user.id).first()
        phone = eadd.phone if eadd else ''
        # email_verified=
        verified = UserVerification.objects.get_or_create(user_id=request.user.id)[0]
        return render(request, 'profile.html', {"phone": phone, "phone_verified": verified.phone_verified,
                                                "email_verified": verified.email_verified})

def areas(request):
    areas=PostCode.objects.all()
    lockey={}
    letters=[]
    resp=[]
    for area in areas:
        fletter=area.name[0].lower()
        if fletter not in letters:
            letters.append(fletter)
        if fletter in lockey.keys():
            lockey[fletter]['areas'].append(area.name)

        else:
            lockey[fletter]={}
            lockey[fletter]['areas']=[area.name]
    data=OrderedDict(sorted(lockey.items()))
    for k,v in data.items():
        d={
            "name":k,
            "area":v['areas']
        }
        resp.append(d)
    # for i in range(3):
    da=chunks(resp,3)
    response=[]
    letters=sorted(letters)
    for i in da:
        response.append(i)
    return render(request,'areas.html',{"data":response,"letters":letters})


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def orderwebhook(request):
    intent_id=request.GET.get('payment_intent')
    stripe_intent = stripe.PaymentIntent.retrieve(intent_id)
    if stripe_intent.status=='succeeded':
        order_id=stripe_intent.metadata.get('order_id')
        user_id = stripe_intent.metadata.get('user_id')
        promo_id = stripe_intent.metadata.get('promo_id') or None
        order = Order.objects.filter(id=order_id, user_id=user_id).first()
        if promo_id:
            promo=PromoUsage()
            promo.order_id=order_id
            promo.promo_id=promo_id
            promo.used_by_id=user_id
            promo.save()
            order.promo_applied=True
        order=Order.objects.filter(id=order_id,user_id=user_id).first()
        order.order_place_date=datetime.datetime.now()
        order.order_status=OrderType.CONFIRMED
        order.paid=True
        order.save()
        return render(request,'placed.html',{'order_id':order.id})


@csrf_exempt
def smswebhook(request):
    if request.method=="POST":
        message_sid = request.POST.get('MessageSid', None)
        message_status = request.POST.get('MessageStatus', None)
        message=Message.objects.filter(sid=message_sid).first()
        if message:
            message.updated_on=datetime.datetime.now()
            message.status=message_status
            message.save()
        else:
            message=Message()
            message.sid=request.POST.get('SmsSid')
            message.sent_to=request.POST.get('To')
            message.sent_from = request.POST.get('From')
            message.updated_on = datetime.datetime.now()
            message.created_on = datetime.datetime.now()
            message.status = message_status
            message.accountsid=request.POST.get('AccountSid')
            message.save()
        return JsonResponse({"status":"ok"})
    return JsonResponse({'status':'not found'})




#Response for marketing webhook

#<QueryDict: {'ErrorCode': ['21608'], 'SmsSid': ['SM31ec2fecaeff1a1bedd7253f954d1672'], 'SmsStatus': ['failed'], 'MessageStatus': ['failed'], 'To': ['+923045171619'], 'MessagingServiceSid': ['MG0f508964da61e66634828eb44a2b27a9'], 'MessageSid': ['SM31ec2fecaeff1a1bedd7253f954d1672'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>
#<QueryDict: {'SmsSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'SmsStatus': ['sent'], 'MessageStatus': ['sent'], 'To': ['+923130452101'], 'MessagingServiceSid': ['MG0f508964da61e66634828eb44a2b27a9'], 'MessageSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>
#<QueryDict: {'SmsSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'SmsStatus': ['queued'], 'MessageStatus': ['queued'], 'To': ['+923130452101'], 'MessagingServiceSid': ['MG0f508964da61e66634828eb44a2b27a9'], 'MessageSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>
#<QueryDict: {'SmsSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'SmsStatus': ['delivered'], 'MessageStatus': ['delivered'], 'To': ['+923130452101'], 'MessagingServiceSid': ['MG0f508964da61e66634828eb44a2b27a9'], 'MessageSid': ['SM7242eb432726a38b21b9c2442eb4dba5'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>

@csrf_exempt
def smsmarketinhwebhook(request):
    print(request.POST)
    if request.method=="POST":
        message_sid = request.POST.get('MessageSid', None)
        message_status = request.POST.get('MessageStatus', None)
        message=Message.objects.filter(sid=message_sid).first()
        message.updated_on=datetime.datetime.now()
        message.status=message_status
        message.save()
        return JsonResponse({"status":"ok"})
    return JsonResponse({'status':'not found'})


def order(request):
    user=request.user
    order = Order.objects.filter(user_id=request.user.id, order_status=OrderType.OPEN).first()

    cart_total=[x.total for x in Cart.objects.filter(order_id=order.id,active=True)]
    cart=[{"cartid":item.id,
           "catid":item.category.id,
           "id":item.service.id,
           "price":item.price,
           "total":item.total,
           "qty":item.qty,
           "name":item.service.name,
           "catname":item.category.name
           } for item in Cart.objects.filter(active=True,purchased=False,user=user,order_id=order.id)]
    total_amount=functools.reduce(lambda a, b: a + b, cart_total,)
    promo=request.session.get('promo')
    promo_amount=None
    promo_res=None
    if promo:
        if promo.get('type')=='amount':
            promo_amount = promo.get('value')
            total_amount=total_amount-promo.get('value')
        elif promo.get('type')=='percentage':
            promo_amount = total_amount * (promo.get('value') / 100)
            total_amount=total_amount-promo_amount

        promo_res={
            "title":promo.get('title'),
            "code":promo.get('code'),
            "total":promo_amount
        }

    order.order_amount=total_amount
    order.save()
    intent=PaymentIntent.objects.filter(order_id=order.id).first()
    if not intent:
        if promo is not None:
            res = stripe.PaymentIntent.create(
                amount=int(order.order_amount * 100),
                currency="gbp",
                payment_method_types=["card"],
                metadata={
                    "order_id": order.id,
                    "user_id": user.id,
                    "promo_id": promo.get('id')
                }
            )
        else:
            res = stripe.PaymentIntent.create(
                amount=int(order.order_amount * 100),
                currency="gbp",
                payment_method_types=["card"],
                metadata={
                    "order_id": order.id,
                    "user_id": user.id
                }
            )
        intent=PaymentIntent()
        intent.order=order
        intent.user=request.user
        intent.intentid=res.id
        intent.client_secret = res.client_secret
        intent.amount=res.amount
        intent.save()
    else:
        id=intent.intentid
        stripe_intent=stripe.PaymentIntent.retrieve(id)
        if int(total_amount * 100)!=stripe_intent.amount:
            if promo is not None:
                res=stripe.PaymentIntent.modify(
                    stripe_intent.id,
                    amount=int(total_amount*100),
                    metadata={
                        "order_id": order.id,
                        "user_id": user.id,
                        "promo_id":promo.get('id')
                    }
                )
            else:
                res = stripe.PaymentIntent.modify(
                    stripe_intent.id,
                    amount=int(total_amount * 100),
                )
            intent.amount=res.amount
            intent.save()
        # intent.intenti

    address=order.ship_address1+", "+order.ship_address2+", "+order.ship_address3+", "+order.ship_address4
    city=order.ship_city
    country=order.ship_country
    postcode=order.ship_postal_code
    pickup={
        "timeslot":order.pickup_time_slot,
        "date":order.pickup_date.strftime("%A, %B %d")
    }
    dropoff = {
        "timeslot": order.dropoff_time_slot,
        "date": order.dropoff_date.strftime("%A, %B %d")
    }
    return render(request,'order.html',{'promo':promo_res,'addressdetail':order.addressdetail,'detail':order.detail,'name':order.fullname,'email':order.email,'phone':order.phone,'cart':cart,'total':total_amount,'address':address,'city':city,'country':country,'postcode':postcode,'pickup':pickup,'dropoff':dropoff})


def loginsuccess(request):
    return render(request,'account/success.html')


def loggedIn(request):
    if request.user.is_authenticated:
        token = Token.objects.filter(user_id=request.user.id).first()
        return JsonResponse({"login":True,"token":token.key})
    else:
        return JsonResponse({"login":False})


def status(request):
    return render(request,'success.html')






from google.oauth2 import id_token
from google.auth.transport import requests as reqs
from django.contrib.auth import login as lin
def create_google_user(request):
    token=request.POST.get('token')
    # (Receive token by HTTPS POST)
    # ...

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, reqs.Request(), settings.GOOGLE_CLIENT_ID)
        # {
        # 'iss': 'https://accounts.google.com',
        # 'nbf': 1664825478,
        #  'aud': '342462780848-k79mrcrbfm2n0inkj8im53rvnbdrblm8.apps.googleusercontent.com',
        #  'sub': '104693037795907723835',
        #  'email': 'asad.tornado99@gmail.com',
        #  'email_verified': True,
        #  'azp': '342462780848-k79mrcrbfm2n0inkj8im53rvnbdrblm8.apps.googleusercontent.com',
        #  'name': 'Asad Saleem',
        #  'picture': 'https://lh3.googleusercontent.com/a/ALm5wu0QoYt5uHim37FCPlg1v_bYdozKGw0BwIubD_HL=s96-c',
        #  'given_name': 'Asad',
        #  'family_name': 'Saleem',
        #  'iat': 1664825778,
        #  'exp': 1664829378,
        #  'jti': 'e5fba2af851a98567251c011db953d9ea9f7e481'}
        try:
            user = User.objects.create_user(password=idinfo['jti'], email=idinfo['email'],
                                            username=idinfo['email'],first_name = idinfo['given_name'],last_name = idinfo['family_name'],is_active = True)

            eadd = Electronic_Address()
            eadd.user = user
            eadd.phone = ""
            eadd.save()
            UserVerification.objects.get_or_create(user_id=user.id, phone_verified=False, email_verified=True)
            data = {"name": user.first_name + ' ' + user.last_name}
            template = get_template("../../home/templates/email/signupemail.html")
            html = template.render(data)
            res = send_mail(subject="Welcome to Picupclean", message="this is a message",
                            from_email="suitclosset@gmail.com",
                            recipient_list=[user.email]
                            , fail_silently=False, html_message=html)
            lin(request, user, backend='django.contrib.auth.backends.ModelBackend')
        except Exception as exc:
            user = User.objects.get(username=idinfo['email'])
            lin(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('homepage')
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, reqs.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        #userid = idinfo['sub']
    except ValueError:
        # Invalid token
        return redirect('login')
    return redirect('homepage')






#Payment Intent
#<QueryDict: {'payment_intent': ['pi_3LHE6tAIj4VUJPcD0zObiKgv'], 'payment_intent_client_secret': ['pi_3LHE6tAIj4VUJPcD0zObiKgv_secret_eWUF4WgLrmFTuH2BQpvVTIozh'], 'redirect_status': ['succeeded']}>

#Twilio
#<QueryDict: {'SmsSid': ['SMe79cf28467c596f70f2be3174f87b0eb'], 'SmsStatus': ['delivered'], 'MessageStatus': ['delivered'], 'To': ['+923130452101'], 'MessageSid': ['SMe79cf28467c596f70f2be3174f87b0eb'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>

def editorder(request):
    if request.method=="GET":
        data={}
        res=[]
        oid=request.GET.get('id')
        order=Order.objects.filter(id=oid).first()
        #picupdate=datetime.datetime.combine(order.pickup_date, datetime.datetime.min.time())+datetime.timedelta(days=1)
        # days = [(picupdate + datetime.timedelta(days=i)).date() for i in range(5) if
        #         (picupdate + datetime.timedelta(days=i)).isoweekday() != 7]
        days = [(datetime.datetime.today() + datetime.timedelta(days=i)).date() for i in range(1,15) if
                (datetime.datetime.today() + datetime.timedelta(days=i)).isoweekday() != 7]
        api_resp = requests.get(
            "https://www.googleapis.com/calendar/v3/calendars/en.uk%23holiday@group.v.calendar.google.com/events?key=AIzaSyBjr42RKZeifwt7Za0P09BJGD8YXTPudLI")
        response = json.loads(api_resp.content)
        holidays = [item['start']['date'] for item in response["items"]]

        days = [day for day in days if str(day) not in holidays]
        sch = ScheduleConfig.objects.all()
        time_schedules = eval(sch[0].value)
        for day in days:
            timeslot_arr = []
            start = int(time_schedules[str(day.isoweekday())]['start'].strftime("%H"))
            end = int(time_schedules[str(day.isoweekday())]['end'].strftime("%H"))
            today = datetime.datetime.now()
            if day == today.date():
                c_hr = today.strftime('%H')
                if start < int(c_hr) and int(c_hr) < end - 2:
                    start = int(c_hr) + 2

            while (start != end):
                timeslot_arr.append({
                    "cleaners": [308, 160],
                    "full_label": day.strftime("%d %B %Y") + ", " + str(start) + ":00 - " + str(start + 1) + ":00",
                    "value": day.strftime("%Y-%m-%d") + "T" + str(start) + ":00:00",
                    "tags": [],
                    "id": str(start) + "-" + str(start + 1),
                    "label": str(start) + ":00 - " + str(start + 1) + ":00"
                })
                start += 1
            if datetime.date.today() == day:
                label = "Today"
            elif datetime.date.today() + datetime.timedelta(days=1) == day:
                label = "Tomorrow"
            else:
                label = time_schedules[str(day.isoweekday())]['day']
            data = {
                "date": day.strftime("%Y-%m-%d"),
                "date_label": day.strftime("%d %B %Y"),
                "weekday_label": f'{label[0].upper()}{label[1:]} ({day.strftime("%d %B %Y")})',
                "time_slots": timeslot_arr
            }
            res.append(data)
        return render(request,'edittime.html',{"country":order.ship_country,"postalcode":order.ship_postal_code,'enable':res,"orderid":order.id})