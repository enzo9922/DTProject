import random
import string
from .models import Item

def generate_unique_id_item():
    while True:
        new_id_item = generate_random_id()
        if not Item.objects.filter(Items_ID=new_id_item).exists():
            return new_id_item

def generate_random_id():
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for i in range(7))
    return random_id

