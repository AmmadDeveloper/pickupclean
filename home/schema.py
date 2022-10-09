from ninja import Schema



class districtSchema(Schema):
    name:str
    email:str
    postcode:str
    country:str

class timeSlotSchema(Schema):
    pickupdate:str
    dropoffdate:str
    pickup_timeslot:str
    dropoff_timeslot:str
    order_id:str

class cartSchema(Schema):
    catid: str=None
    catname: str=None
    name: str=None
    id: str=None
    price: float=None
    qty: int=None
    total: float=None
    cartid:int=None

class PromoSchema(Schema):
    code:str

class AuthenticationSchema(Schema):
    email:str
    password:str
    
class GoogleSchema(Schema):
    token:str