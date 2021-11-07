import uuid
from profiles.models import Profile
from customers.models import Customer

def generate_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code

def get_customer_name_from_id(val):
    customer_name = Customer.objects.get(id=val)
    return customer_name


def get_salesman_name_from_id(val):
    salesman_name = Profile.objects.get(id=val)
    return salesman_name.user.username