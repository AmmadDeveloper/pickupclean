from enum import Enum
import json

class Menu:
    @staticmethod
    def get_menu():
        with open('menu.txt') as f:
            data = json.load(f)
        return data

class Constant:

    SENDER_NAME = "BigBuy"
    SENDER_EMAIL = "noreply@bigbuy.com"


class TransStatus:
    APPROVED = "approved"
    DECLINED = "declined"


class TransType:
    SALE = "sale"
    VOID = "void"
    REFUND = "refund"
    COD = "cod"


class ProcessorType:
    CARDCONNECT = "cardconnect"
    COD = "cod"


class OrderType:
    OPEN='open'
    # SHIPPED = "shipped"
    CANCELLED = "cancelled"
    REFUND = "refunded"
    DELIVERED = "delivered"
    DECLINED = "declined"
    INPROGRESS="in-progress"
#    CONFIRMED = "confirmed"
#     PROCESSING= "processing"
#     PICKEDUP = 'pickedup'
    COMPLETED='completed'


class OrderTypeChoice:
    CHOICES = (
        (OrderType.OPEN, 'open'),
#        (OrderType.CONFIRMED, 'confirmed'),
        (OrderType.INPROGRESS, 'in-progress'),
        (OrderType.CANCELLED, 'cancelled'),
        (OrderType.DECLINED, 'declined'),
        (OrderType.REFUND, 'refunded'),
        # (OrderType.PICKEDUP,'pickedup'),
        # (OrderType.PROCESSING, 'processing'),
        # (OrderType.SHIPPED, 'shipped'),
        (OrderType.COMPLETED, 'completed'),
    )



class UserType(Enum):
    Customer = 1
    Vendor = 2
    Supplier = 3
    Staff = 4
    Admin = 5

class AddressType(Enum):
    HOME = "Home"
    BILL = "Bill"
    SHIPMENT = "Shipment"