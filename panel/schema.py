from models.models import Promo

from ninja import ModelSchema,Schema



from ninja import Schema

class SettingSchema(Schema):
    schedule:dict
    emailConfig:dict
    phoneConfig:dict

class CategorySchema(Schema):
    short_description:str
    description:str
    icon:str
    picture:str
    name:str
    id:int=None

class ServiceSchema(Schema):
    id:int=None
    name:str
    price:str
    description:str
    delivery_time:str
    category_id:int
    type_id:int

    # class Config:
    #     model=Service
    #     model_fields=['name','price','description','delivery_time','category']

class PostCodeSchema(Schema):
    id:int=None
    name:str
    code:str
    description:str
    country:str

    # class Config:
    #     model=PostCode
    #     model_fields=['id','name','code','description','country']


class PromoSchema(ModelSchema):
    class Config:
        model=Promo
        model_fields=['title','until','type','value']

class AuthenticationSchema(Schema):
    email:str
    password:str



class EmailSendSchema(Schema):
    emails:list=None
    to:str
    body:str

class PhoneSendSchema(Schema):
    phones:list=None
    to:str
    body:str

class ServiceTypeSchema(Schema):
    name:str
    id:int = None