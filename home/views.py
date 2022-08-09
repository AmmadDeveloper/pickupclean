import datetime
import functools
from django.http import JsonResponse
from django.shortcuts import render,redirect
from models.models import Category,Message,PostCode,Electronic_Address,Order,Cart,PaymentIntent
from models.utils.Constants import OrderType
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as lout, authenticate,login as lin
from .forms import loginform,signupform
from django.contrib.auth.models import User
from django.contrib.messages import add_message,get_messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import get_template
from django.db.models.query_utils import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections import OrderedDict
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def home(request):
    if request.method=="GET":
        return render(request,'index.html')
    elif request.method=="POST":
        if request.user.is_authenticated:
            if request.POST.get('pickup_date') !='' and request.POST.get('dropoff_date')!='':
                ord = Order.objects.filter(user_id=request.user.id, order_status=OrderType.OPEN).first()
                eaddress=Electronic_Address.objects.filter(user_id=request.user.id).first()
                if not ord:
                    ord=Order()
                    ord.fullname=request.user.first_name+request.user.last_name
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


def orderdetail(request):
    return render(request,'orderdetail.html')

def login(request):
    if request.method=="GET":
        return render(request, 'account/login.html')
    if request.method == "POST":
        lform = loginform(request.POST or None)
        if (lform.is_valid()):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user == None:
                return redirect('login')
            else:
                lin(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('homepage')
        else:
            return render(request, 'account/login.html')


    return render(request,'account/login.html')
def signup(request):
    if request.method=="GET":
        return render(request,'account/signup.html')
    elif request.method=="POST":
        sform=signupform(request.POST or None)
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
                lin(request,user,backend='django.contrib.auth.backends.ModelBackend')
            except Exception as exc:
                add_message(request,level=7,message="User already exists")
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
    return render(request,'price.html')



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
                'site_name': 'Pick Up Clean',
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


def orderhistory(request):
    if request.user.is_authenticated:
        query=Q()
        query.add(Q(email__iexact=request.user.email),Q.OR)
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

def corporate(request):
    return render(request,'corporate.html')


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
    order.order_amount=total_amount
    order.save()
    intent=PaymentIntent.objects.filter(order_id=order.id).first()
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
            res=stripe.PaymentIntent.modify(
                stripe_intent.id,
                amount=int(total_amount*100),
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
    return render(request,'order.html',{'addressdetail':order.addressdetail,'detail':order.detail,'name':order.fullname,'email':order.email,'phone':order.phone,'cart':cart,'total':total_amount,'address':address,'city':city,'country':country,'postcode':postcode,'pickup':pickup,'dropoff':dropoff})


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



#Payment Intent
#<QueryDict: {'payment_intent': ['pi_3LHE6tAIj4VUJPcD0zObiKgv'], 'payment_intent_client_secret': ['pi_3LHE6tAIj4VUJPcD0zObiKgv_secret_eWUF4WgLrmFTuH2BQpvVTIozh'], 'redirect_status': ['succeeded']}>

#Twilio
#<QueryDict: {'SmsSid': ['SMe79cf28467c596f70f2be3174f87b0eb'], 'SmsStatus': ['delivered'], 'MessageStatus': ['delivered'], 'To': ['+923130452101'], 'MessageSid': ['SMe79cf28467c596f70f2be3174f87b0eb'], 'AccountSid': ['AC1bfc23beba30546467e2c4351485b009'], 'From': ['+19707164935'], 'ApiVersion': ['2010-04-01']}>