import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.template.loader import get_template
from rest_framework.authtoken.models import Token
from .utils.Constants import OrderType, OrderTypeChoice
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




# USER MANAGEMENT
# class UserManager(BaseUserManager):
#
#     def get_or_none(self, **kwargs):
#         try:
#             return self.get(**kwargs)
#         except ObjectDoesNotExist:
#             return None
#
#     def create_user(self, email, phone=None, firstname=None, lasttname=None, Image=None, password=None, is_admin=False,
#                     is_staff=False, is_active=True, is_customer=True ):
#
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#         if not firstname:
#             raise ValueError("User must have a first name")
#         if not lasttname:
#             raise ValueError("User must have a last name")
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.phone = phone
#         user.first_name = firstname
#         user.last_name = lasttname
#         user.set_password(password)
#         user.image = Image
#         user.is_admin = is_admin
#         user.is_staff = is_staff
#         user.is_customer = is_customer
#         # user.is_vendor = is_vendor
#         user.is_active = is_active
#         user.save(using=self._db)
#         token = Token.objects.create(user=user)
#         # data = {"name": user.first_name+' '+user.last_name}
#         # template = get_template("../../home/templates/email/signupemail.html")
#         # html = template.render(data)
#         # res = send_mail(subject="Welcome to Suit Closset", message="this is a message",
#         #                 from_email="suitclosset@gmail.com",
#         #                 recipient_list=[user.email]
#         #                 , fail_silently=False, html_message=html)
#         # if res == 1:
#         #     pass
#         return user
#
#     def create_superuser(self, email, full_name=None, Image=None, password=None, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#
#         user.full_name = full_name
#         user.set_password(password)
#         user.image = Image
#         user.is_admin = True
#         user.is_staff = True
#         user.is_active = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         token = Token.objects.create(user=user)
#         print(token)
#         return user
#
#
# class UserRole(models.Model):
#     USER_ROLES = [
#         (1, 'Admin'),
#         (2, 'Customer')
#     ]
#     name = models.CharField(max_length=50, choices=USER_ROLES, blank=True, null=True)
#
#     def __str__(self):
#         return self.name


# class User(AbstractBaseUser):
#     # CUSTOMER = 1
#     # VENDOR = 2
#     # SUPPLIER = 3
#     # STAFF = 4
#     # ADMIN = 5
#     # ROLES = [
#     #     (CUSTOMER, 'Customer'),
#     #     (VENDOR, 'Vendor'),
#     #     (STAFF, 'Staff'),
#     #     (ADMIN, 'Admin')
#     # ]
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     username=models.CharField(max_length=200, blank=True, null=True)
#     first_name = models.CharField(max_length=200, blank=True, null=True)
#     last_name = models.CharField(max_length=200, blank=True, null=True)
#     user_type = models.ForeignKey('UserRole', null=True, on_delete=models.SET_NULL)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     image = models.ImageField(upload_to='media/UserImages/')
#     joining_date = models.DateTimeField(auto_now_add=True)
#     is_superuser = models.BooleanField(default=False)
#     is_custom_size = models.BooleanField(default=False)
#     is_postal_address = models.BooleanField(default=False)
#     is_electronic_address = models.BooleanField(default=False)
#     is_blocked = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_login = models.BooleanField(default=False)
#     # is_vendor = models.BooleanField(default=False)
#     is_customer = models.BooleanField(default=False)
#
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []  # Email & Password are required by default.
#
#     # def get_full_name(self):
#     #     # The user is identified by their email address
#     #     return f"{self.first_name} {self.last_name}"
#
#     # def get_short_name(self):
#     #     # The user is identified by their email address
#     #     return self.first_name
#
#     # def __str__(self):  # __unicode__ on Python 2
#     #     return self.email if self.email else ''
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     # @property
#     # def is_staff(self):
#     #     return self.staff
#     #
#     # @property
#     # def is_admin(self):
#     #     return self.admin
#     #
#     # @property
#     # def is_active(self):
#     #     return self.active

# Addresses
class Electronic_Address(models.Model):
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='electronic_address')


class Postal_Address(models.Model):
    HOME = "Home"
    BILLING = "Billing"
    SHIPPING = "Shipping"

    ADDRESS_TYPE = [
        (HOME, "Home"),
        (BILLING, "Billing"),
        (SHIPPING, "Shipping")
    ]
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=ADDRESS_TYPE, default=HOME)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Services and Category
class ServiceType(models.Model):
    name=models.CharField(max_length=200)
    active=models.BooleanField(default=True)
    description=models.CharField(max_length=200)
    picture = models.ImageField(upload_to='typeImage')
    created_on=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=500)
    price = models.FloatField( default=0.0, null=False, blank=False)
    bottom_heading = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_attributes_available = models.BooleanField(default=False)
    sku = models.CharField(max_length=20, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    delivery_time = models.CharField(max_length=254, blank=True, null=True)
    servicetype=models.ForeignKey('ServiceType',related_name="services",on_delete=models.DO_NOTHING)
    category = models.ForeignKey('Category', null=True, related_name="category_products", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="vendor_name")

    # Shipper = models.ForeignKey('ShipmentMethod', null=True, on_delete=models.CASCADE, related_name='product_shipper')

    def __str__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    short_description = models.CharField(max_length=250,default="")
    picture = models.ImageField(upload_to='categoryImage')
    icon = models.ImageField(upload_to='categoryicons')
    active = models.BooleanField(default=True)
    # sub_category = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # parent_category = models.ForeignKey('Category', null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





class Promo(models.Model):
    title=models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    until=models.DateTimeField()
    type=models.CharField(max_length=20)
    active=models.BooleanField(default=True)
    value=models.FloatField(default=0.0,null=False,blank=False)
    created_on=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING,related_name='promos')




class ServiceAttribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=450)
    product = models.ForeignKey('Service', on_delete=models.CASCADE, related_name="productattributes")

class Address(models.Model):
    line1=models.CharField(max_length=250)
    line2=models.CharField(max_length=250,blank=True,null=True)
    city=models.CharField(max_length=250,blank=True,null=True)
    province=models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=250,blank=True,null=True)
    postcode=models.CharField(max_length=250)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name='user_address')

# ORDER AND PAYMENT
class Order(models.Model):
    fullname=models.CharField(max_length=100, blank=True, null=True)
    email=models.CharField(max_length=60, blank=True, null=True)
    phone=models.CharField(max_length=50, blank=True, null=True)
    addressdetail=models.CharField(max_length=100, blank=True, null=True)
    detail=models.BooleanField(default=False)
    ordernotecheck = models.BooleanField(default=False, )
    order_note = models.CharField(max_length=100, blank=True, null=True)
    order_amount = models.DecimalField(max_digits=65, decimal_places=4, blank=True, null=True)
    promo_applied=models.BooleanField(default=False)
    pickup_date=models.DateField()
    pickup_time_slot=models.CharField(max_length=15)
    dropoff_date=models.DateField()
    dropoff_time_slot = models.CharField(max_length=15)
    order_status = models.CharField(max_length=50, choices=OrderTypeChoice.CHOICES, default=OrderType.OPEN)
    deleted = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    err_message = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order_place_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    order_close_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    ship_address1 = models.TextField(blank=True, null=True)
    ship_address2 = models.TextField(blank=True, null=True)
    ship_address3 = models.TextField(blank=True, null=True)
    ship_address4 = models.TextField(blank=True, null=True)
    ship_phone1 = models.CharField(max_length=50, blank=True, null=True)
    ship_postal_code = models.CharField(max_length=20, blank=True, null=True)
    ship_city = models.CharField(max_length=50, blank=True, null=True)
    ship_country = models.CharField(max_length=50, blank=True, null=True)
    shipping_number = models.CharField(max_length=254, blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __fulladdress__(self):
        address=""
        if self.ship_address1!=None and self.ship_address1!='':
            address+=self.ship_address1+", "
        if self.ship_address2!=None and self.ship_address2!='':
            address+=self.ship_address2+", "
        if self.ship_address3!=None and self.ship_address3!='':
            address+=self.ship_address3+", "
        if self.ship_address4!=None and self.ship_address4!='':
            address+=self.ship_address4+", "
        if self.ship_city!=None and self.ship_city!='':
            address+=self.ship_city+", "
        if self.ship_country!=None and self.ship_country!='':
            address+=self.ship_country+", "
        if self.addressdetail!=None and self.addressdetail!='':
            address+=",("+self.addressdetail+"), "
        if self.ship_postal_code!=None and self.ship_postal_code!='':
            address+=self.ship_postal_code
        return address

class Cart(models.Model):
    purchased=models.BooleanField(default=False)
    price=models.FloatField(default=0.0,null=False,blank=False)
    qty = models.IntegerField(default=0, null=False, blank=False)
    total = models.FloatField(default=0.0, null=False, blank=False)
    active=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordercart')
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name='user')
    created_on = models.DateTimeField(auto_now_add=True)

class PaymentIntent(models.Model):
    client_secret=models.CharField(max_length=90, blank=False, null=False)
    refund=models.BooleanField(default=False)
    refund_date = models.DateTimeField(blank=True,null=True)
    amount=models.IntegerField(default=0,blank=True, null=False)
    intentid=models.CharField(max_length=50, blank=False, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_intent')
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)


class OrderDetails(models.Model):
    price = models.DecimalField(max_digits=65, decimal_places=4, default=0.00, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    discount = models.DecimalField(max_digits=65, decimal_places=4, default=0.00, blank=True, null=True)
    total = models.DecimalField(max_digits=65, decimal_places=4, default=0.00, blank=True, null=True)
    # color = models.CharField(max_length=20)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="order_lines")
    service = models.ForeignKey('Service', on_delete=models.CASCADE)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=65, decimal_places=4, default=0.0)
    status = models.CharField(max_length=20, blank=True, null=True)
    card_holder_name = models.CharField(max_length=254, blank=True, null=True)
    last4digit = models.CharField(max_length=5, blank=True, null=True)
    card_type = models.CharField(max_length=20, blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    process_type = models.CharField(max_length=25, blank=True, null=True)
    trans_type = models.CharField(max_length=15, blank=True, null=True)
    auth_code = models.CharField(max_length=254, blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    customer_name = models.CharField(max_length=254, blank=True, null=True)
    customer_email = models.EmailField(max_length=50, blank=True, null=True)
    ref_id = models.CharField(max_length=254, blank=True, null=True)
    parent_ref_id = models.CharField(max_length=254, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True, blank=True)
    order = models.ForeignKey('Order', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user.email)


# NEWSLETTERS

class Newsletter(models.Model):
    email = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)


class Files(models.Model):
    File = models.ImageField(upload_to='files')
    created_on = models.DateTimeField(auto_now_add=True)


class HomeBackground(models.Model):
    File=models.ImageField(upload_to='backgrounds')
    created_on=models.DateTimeField(auto_now_add=True)




# POSTCODES & TIMESLOTS

class PostCode(models.Model):
    name = models.CharField(blank=False, max_length=50)
    code = models.CharField(blank=False, max_length=20)
    description = models.CharField(blank=True, max_length=200)
    country = models.CharField(blank=False, default="GB", max_length=50)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)


class PostCodeRequests(models.Model):
    name=models.CharField(blank=False, max_length=100)
    email=models.CharField(blank=False, max_length=200)
    postcode=models.CharField(blank=False, max_length=50)
    country=models.CharField(blank=False, max_length=50)
    created_on=models.DateTimeField(auto_now_add=True)

class Weekday(models.Model):
    weekday = models.CharField(blank=False, max_length=20)
    postcode = models.ForeignKey('PostCode', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class TimeSlot(models.Model):
    slot = models.TimeField(blank=False)
    weekday = models.ForeignKey('Weekday', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class ScheduleConfig(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    value=models.TextField(default="")


class EmailConfig(models.Model):
    updated_on = models.DateTimeField(auto_now_add=True)
    created_on=models.DateTimeField(auto_now_add=True)
    email=models.EmailField()
    password=models.CharField(max_length=100,null=False,blank=False,default="")

class PhoneConfig(models.Model):
    updated_on = models.DateTimeField(auto_now_add=True)
    created_on=models.DateTimeField(auto_now_add=True)
    phone=models.CharField(max_length=30,blank=False,null=False)


class Notification(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    message=models.CharField(max_length=200)
    heading = models.CharField(max_length=100, default='')
    order=models.ForeignKey('Order',on_delete=models.CASCADE,related_name="order_notification",null=True,blank=True)

class NotificationRead(models.Model):
    read_on=models.DateTimeField(auto_now_add=True)
    notification=models.ForeignKey('Notification',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="read_notifications")

class PromoUsage(models.Model):
    used_on=models.DateTimeField(auto_now_add=True)
    order=models.ForeignKey('Order',on_delete=models.CASCADE,related_name="order_promo")
    promo=models.ForeignKey('Promo',on_delete=models.DO_NOTHING,related_name='used_by')
    used_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="used_promo")


class Message(models.Model):
    sid=models.CharField(max_length=50,blank=False,null=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(blank=True,null=True)
    body=models.CharField(max_length=500,blank=False,null=False)
    accountsid=models.CharField(max_length=150,blank=False,null=False)
    status = models.CharField(max_length=50, blank=True, null=True)
    error_code=models.CharField(max_length=50,blank=True,null=True)
    error_message = models.CharField(max_length=150, blank=True, null=True)
    sent_to=models.CharField(max_length=50,blank=False,null=False)
    sent_from = models.CharField(max_length=50, blank=False, null=False)
    uri=models.CharField(max_length=200,blank=True,null=True)


class UserVerification(models.Model):
    email_verified=models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class EmailCode(models.Model):
    code=models.CharField(max_length=100)
    created_on=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class PhoneCode(models.Model):
    code=models.CharField(max_length=20)
    created_on=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class EmailRecord(models.Model):
    subject=models.CharField(max_length=1000,blank=False,null=False)
    recipient_type=models.CharField(max_length=15)
    status=models.CharField(max_length=20)
    status_message = models.TextField()
    recipients=models.TextField()
    created_by= models.ForeignKey(User, on_delete=models.CASCADE,related_name="emails_sent")
    created_on=models.DateTimeField(auto_now_add=True)
    body=models.TextField()


class MessageRecord(models.Model):
    sid=models.CharField(max_length=100,default='',null=True,blank=True)
    recipient_type = models.CharField(max_length=15)
    status = models.CharField(max_length=50)
    status_message = models.TextField()
    recipients = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()


#Signals


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# from allauth.account.models import EmailAddress
# @receiver(post_save,sender=User)
# def user_signup_procedure(sender, instance=None, created=False, **kwargs):
#     user=instance
#     email=EmailAddress.objects.filter(user_id=user.id).first()
#     if not email:
#         UserVerification.objects.get_or_create(user_id=user.id,phone_verified=False,email_verified=False)
#         data = {"name": user.first_name + ' ' + user.last_name}
#         template = get_template("../../home/templates/email/signupemail.html")
#         html = template.render(data)
#         res = send_mail(subject="Welcome to Pick up clean", message="this is a message",
#                         from_email="suitclosset@gmail.com",
#                         recipient_list=[user.email]
#                         , fail_silently=False, html_message=html)
#     else:
#         userverification=UserVerification.objects.get(user_id=user.id)
#         if userverification:
#             userverification.email_verified=email.verified
#             userverification.save()
#         else:
#             UserVerification.objects.get_or_create(user_id=user.id, phone_verified=False, email_verified=email.verified)



@receiver(post_save, sender=Order)
def create_notification(sender, instance=None, created=False, **kwargs):
    order=instance
    if order.paid and order.order_status=='confirmed':
        notf=Notification.objects.filter(order_id=order.id).first()
        if not notf:
            notification=Notification()
            notification.order_id=order.id
            notification.heading="Order Received"
            notification.message="You have a new order, Order number is "+str(order.id)+", pick up time slot is "+str(order.pickup_time_slot)+" on "+order.pickup_date.strftime("%B %d, %y")+" and postal code is "+str(order.ship_postal_code)
            notification.save()

