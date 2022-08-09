from ninja import Schema



class districtSchema(Schema):
    name:str
    email:str
    postcode:str
    country:str

class cartSchema(Schema):
    catid: str=None
    catname: str=None
    name: str=None
    id: str=None
    price: float=None
    qty: int=None
    total: float=None
    cartid:int=None

class AuthenticationSchema(Schema):
    email:str
    password:str