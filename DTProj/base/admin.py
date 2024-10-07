from django.contrib import admin
from .models import Item, Participant, Result, Bidding

admin.site.register(Item)
admin.site.register(Participant)
admin.site.register(Result)
admin.site.register(Bidding)
