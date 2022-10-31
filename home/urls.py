
from django.urls import path,re_path
from .views import verify_email, callback, verify_phone, smswebhook, setpassword, orderhistory, home, orderdetail, \
    loggedIn, loginsuccess, login, price, resetpass, services, profile, areas, servicedetail, order, logout, privacy, \
    instruction, status, signup, orderwebhook, smsmarketinhwebhook, create_google_user,editorder,terms,about
from django.conf import settings
from django.conf.urls.static import static
from .api import user_api
urlpatterns = [
    re_path(r'^setpassword/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',setpassword,name="set_password"),
    path('resetpass/', resetpass ,name="resetpass"),
    path('orderhistory/', orderhistory ,name="orderhistory"),
    re_path('^login/', login ,name="login"),
    re_path('^logout/', logout ,name="logout"),
    path('signup/',signup,name="signup"),
    path('about/',about,name="about"),
    path('privacy/',privacy,name="privacy"),
    path('terms/',terms,name="terms"),
    path('instructions/',instruction,name="instructions"),
    path('', home ,name="homepage"),
    path('success/', loginsuccess ,name="success"),
    path('loggedin/', loggedIn ,name="loggedin"),
    path('price/', price ,name="price"),
    path('orderdetail/', orderdetail ,name="orderdetail"),
    path('order/', order ,name="order"),
    path('order/webhook/',orderwebhook,name="webhook"),
    path('areas/', areas ,name="areas"),
    path('services/', services ,name="services"),
    path('servicesdetail/<id>', servicedetail ,name="servicedetail"),
    path('profile/', profile ,name="profile"),
    path('api/',user_api.urls),
    path('verify_email/',verify_email,name="verify_email"),
    path('verify_phone/<phone>',verify_phone,name="verify_phone"),
    re_path('^social/google',create_google_user),
    re_path('^order/',status),
    re_path('^email/callback/',callback,name="emailcallback"),
    re_path('^sms/status',smswebhook,name="smswebhook"),
    re_path('^smsmarketing/status',smsmarketinhwebhook,name="smsmarketingwebhook"),
    re_path('^editorder/',editorder)
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)