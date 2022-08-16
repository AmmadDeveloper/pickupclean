from ninja import Schema


class AuthenticationSchema(Schema):
    email:str
    password:str


class SignUpSchema(Schema):
    email:str
    fullname:str
    password:str
    phone:str

class CreateOrderSchema(Schema):
    address_line1:str
    address_line2: str
    address_line3: str
    address_line4: str
    postcode:str
    country:str
    city:str
    pickup_date:str
    dropoff_date:str
    pickup_time_slot:str
    dropoff_time_slot:str


class cartSchema(Schema):
    catid: str=None
    catname: str=None
    name: str=None
    id: str=None
    price: float=None
    qty: int=None
    total: float=None
    cartid:int=None
