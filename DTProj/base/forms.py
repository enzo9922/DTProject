from django import forms
from .models import Participant, Item
from decimal import Decimal, InvalidOperation
from .utils import *

class ParticipantForm(forms.Form):
    participants = forms.JSONField()
    
    def save(self, items):
        participants_data = self.cleaned_data.get('participants', [])
        participants = []
        
        for participant_data in participants_data:
            participant = Participant(
                first_name=participant_data.get('firstName', ''),
                last_name=participant_data.get('lastName', ''),
                email=participant_data.get('email', ''),
                password=participant_data.get('password', ''),
                IDParticipants = generate_random_id(),
                IDItems = items
            )
            participants.append(participant)

        return participants


class PropertyForm(forms.Form):
    properties = forms.JSONField()

    def save(self, items, commit=True):
        properties_data = self.cleaned_data.get('properties', [])
        properties = []

        for property_data in properties_data:
            property_name = property_data.get('propertyName', '')
            min_bid = property_data.get('minBid', None)

            try:
                min_bid = Decimal(min_bid)
            except InvalidOperation:
                min_bid = None

            property_instance = Item(
                property_name=property_name,
                min_bid=min_bid,
                Items_ID = items
            )
            properties.append(property_instance)

        if commit:
            Item.objects.bulk_create(properties)

        return properties

