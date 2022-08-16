
from django.urls import path,re_path
from .views import smswebhook,setpassword,orderhistory,home,orderdetail,loggedIn,loginsuccess,login,price,resetpass,services,corporate,areas,servicedetail,order,logout,privacy,instruction,status,signup,orderwebhook,smsmarketinhwebhook
from django.conf import settings
from django.conf.urls.static import static
from .api import user_api
urlpatterns = [
    re_path(r'^setpassword/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',setpassword,name="set_password"),
    path('resetpass/', resetpass ,name="resetpass"),
    path('orderhistory/', orderhistory ,name="orderhistory"),
    path('login/', login ,name="login"),
    path('logout/', logout ,name="logout"),
    path('signup/',signup,name="signup"),
    path('privacy/',privacy,name="privacy"),
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
    path('corporate/', corporate ,name="corporate"),
    path('api/',user_api.urls),
    re_path('^order/',status),
    re_path('^sms/status',smswebhook,name="smswebhook"),
    re_path('^smsmarketing/status',smsmarketinhwebhook,name="smsmarketingwebhook")
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)