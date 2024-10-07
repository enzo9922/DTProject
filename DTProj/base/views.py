from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import ParticipantForm, PropertyForm
from .models import Participant, Item, Bidding, Result
from .utils import *
from django.core.mail import send_mail, EmailMessage
from DTProj.settings import EMAIL_HOST_USER 
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.staticfiles import finders
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def home(request):
    return render(request, 'main.html')

def register(request):
    return render (request, 'Register.html')

def submit_form(request):
    
    if request.method == 'POST':
        
        participant_form = ParticipantForm(request.POST)
        property_form = PropertyForm(request.POST)

        if participant_form.is_valid() and property_form.is_valid():
            
            items = generate_unique_id_item()
            
            participants = participant_form.save(items=items)
            for participant in participants:
                participant.save()
                
            properties = property_form.save(items=items)
            for property_instance in properties:
                property_instance.save()

            send_mail_to_participants(
                subject='Sealed Bid',
                sender='inheritancesettlement1@gmail.com',
                item_id=items,
            ) 

            success = 'Registration for the bidding has been successfully completed.'
            return render(request, 'successMsg.html', {'success_message':success})

def send_mail_to_participants(subject, sender, item_id, fail_silently=False):
    # Fetch the most recently registered participants with the same itemID from the database
    participants = Participant.objects.filter(IDItems=item_id)

    # Send email to recently registered participants
    for participant in participants:
        # Construct the personalized URL based on the participant's IDParticipants
        bidding_url = reverse('bidding', args=[participant.IDParticipants])

        # Create the email message
        email_message = f"Greetings {participant.first_name}!\n\n" \
                        f"Attached link is the link that you will be using for bidding:\n" \
                        f"http://127.0.0.1:8000{bidding_url}\n\n" \
                        f"Room Password: {participant.password}\n" \
                        f"Good luck and may you get what you desire!"

        # Send email to the participant
        send_mail(subject, email_message, sender, [participant.email], fail_silently=fail_silently)


def bidding(request, bidding_url):
    participant = Participant.objects.filter(IDParticipants=bidding_url).first()
    participant_IFBid = Bidding.objects.filter(IDParticipants=bidding_url)
   
    if participant_IFBid.exists():
        success = 'You Successfully Bid and Please Wait the Result in Your Email: Check it regularly'
        return render(request, 'successMsg.html', {'success_message': success})
    
    if participant:
        return render(request, 'JoinBidding.html', {'participant': participant})
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

def agreement(request, bidding_url):
    participant = Participant.objects.filter(IDParticipants=bidding_url).first()

    if not participant:
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        entered_password = request.POST.get('password')
        participant_password = request.POST.get('participant_password')

        if entered_password == participant_password:
            return render(request, 'agtPage.html', {'participant': participant})
        
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return render(request, 'JoinBidding.html', {'participant': participant})
        

def auction(request, bidding_url):
    # Fetch participant and associated properties
    participants = Participant.objects.filter(IDParticipants=bidding_url).first()
    properties = Item.objects.filter(Items_ID=participants.IDItems)
    getItems = []

    # Check if participant exists
    if not participants:
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Process POST request (form submission)
    if request.method == 'POST':
        # Iterate over properties and handle bid amounts
        for property in properties:
            item_id = str(property.id)
            bid_amount_key = 'bid_amount_' + item_id
            bid_amount = request.POST.get(bid_amount_key)

            # Check if input bid is less than the minimum bid amount
            if property.min_bid is not None and Decimal(bid_amount) < property.min_bid:
                messages.error(request, f'Bid is less than the minimum bid amount. Please try again.')
                return render(request, 'biddingPage.html', {'participant': participants, 'properties': properties, 'error_message': f'Bid must be equal to or greater than the minimum bid of ${property.min_bid} for {property.property_name}.'})

            getItems.append(bid_amount)

        # Dynamically calculate total and create Bidding instance
        total = sum(int(bid_amount) for bid_amount in getItems)
        bidding_data = {'IDParticipants': participants.IDParticipants, 'total': total}
        for i, bid_amount in enumerate(getItems, start=1):
            bidding_data[f'item{i}'] = int(bid_amount)

        CurrentAuction = Bidding(**bidding_data)
        CurrentAuction.save()


        # Fetch participant and associated items for further processing
        participant = get_object_or_404(Participant, IDParticipants=bidding_url)
        currPTItems = Item.objects.filter(Items_ID=participant.IDItems)
        getParticipants = Participant.objects.filter(IDItems=participant.IDItems)

        # Initialize arrays to store information for each participant
        valItems = []  # Store all the items value of each participant
        totalValItems = []  # Store the total value per participant which they declared for each item

        # Iterate over participants and process bidding results
        for get_participant in getParticipants:
            checkParticipant = Bidding.objects.filter(IDParticipants=get_participant.IDParticipants)

            if checkParticipant.exists():
                currentParticipant = Bidding.objects.get(IDParticipants=get_participant.IDParticipants)
                totalValItems.append(currentParticipant.total)

                valItems1 = [getattr(currentParticipant, f'item{i}') for i in range(1, 16) if getattr(currentParticipant, f'item{i}') >= 0]
                valItems.append(valItems1)
            else:
                success = 'You Successfully Bid and Please Wait for the Result in Your Email: Check it regularly'
                return render(request, 'successMsg.html', {'success_message': success})

        # Initialize arrays for storing final results
 
        PTId = []  # Participant ID
        PTFirstName = []  # Participant first name
        PTLastName = []  # Participant last name
        PTEmail = []  # Participant email
        itemWon = []  # Items they won
        pay = [] # Amount to pay for each participant
        get = [] # Amount to receive for each participant
        totalValue = []  # Total value awarded
        amount = []  # Amount they get or pay
        fairShare = []  # Fair share
        final_amount = []  # Amount minus the surplus


        # Loop for storing participant information
        for getParticipant in getParticipants:
            PTId.append(getParticipant.IDParticipants)
            PTFirstName.append(getParticipant.first_name)
            PTLastName.append(getParticipant.last_name)
            PTEmail.append(getParticipant.email)

        # Loop for initializing arrays
        for i in range(len(getParticipants)):
            totalValue.append(0)
            final_amount.append(0)
            amount.append(0)
            pay.append(0)
            get.append(0)
            itemWon.append('')
            fair_Share = totalValItems[i] / len(getParticipants)
            rounded = round(fair_Share, 2)
            fairShare.append(rounded)

        # Process bidding results and determine winners
        for count, currPTItem in enumerate(currPTItems):
            values = [sublist[count] for sublist in valItems]
            max_value = max(values)
            indices = [i for i, v in enumerate(values) if v == max_value]

            random_winner_index = random.choice(indices) if len(indices) > 1 else indices[0]

            totalValue[random_winner_index] += max_value
            itemWon[random_winner_index] = f"{currPTItem.property_name} {itemWon[random_winner_index]}"

        # Calculate Initial amounts participants will pay or receive
        for i in range(len(getParticipants)):
            amount[i] = fairShare[i] - totalValue[i]   # Total value awarded - fair share

        # Find surplus by totaling amounts
        surplus = sum(amount)

        # Split the surplus among participants
        surplus_split = surplus / len(getParticipants)

        # Round off surplus to 2 decimal places
        rounded_surplus = round(surplus_split, 2)

        # Loop for the final amount participants will pay (or receive)
        for i in range(len(getParticipants)):
            final_amount[i] = amount[i] - rounded_surplus
            if final_amount[i] > 0:
                get[i] = round((final_amount[i]), 2) 
            else:
                pay[i] = round(abs(final_amount[i]), 2)


        # Loop for saving auction result data to the database and sending emails
        for i in range(len(getParticipants)):
            participant_data = {
                'fName': PTFirstName[i],
                'lName': PTLastName[i],
                'email': PTEmail[i],
                'IDParticipants': PTId[i],
                'itemWon': itemWon[i],
                'totalValue': totalValue[i],
                'fairShare': fairShare[i],
                'pay': pay[i],
                'get': get[i],
            }

            # Save auction result data to the database
            auction_result = Result(**participant_data)
            auction_result.save()

            # Send an email with the PDF attachment
            send_auction_result_email(participant_data)

        success = 'Auction results successfully processed and emails sent.'
        return render(request, 'successMsg.html', {'success_message': success})

    # Render the bidding page with participant and property information
    return render(request, 'biddingPage.html', {'participant': participants, 'properties': properties})
        

def send_auction_result_email(participant_data):

    pdf_content = generate_pdf(participant_data)

    email = EmailMessage(
        'AUCTION RESULT',
        f'Greetings!\n\n'
        f'This is the properties settlement team. We are excited to inform you that the results of your bidding are now available. '
        f'Please find attached the PDF with detailed information about your auction results. You can download and review the document at your convenience.\n\n'
        f'Thank you for participating in the auction!\n\n'
        f'Best regards,\n'
        f'Your Properties Settlement Team',
        'from@example.com',
        [participant_data['email']],
    )
    
    email.attach('auction_result.pdf', pdf_content.getvalue(), 'application/pdf')
    email.send() 

def generate_pdf(participant_data):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="auction_result.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    current_date = datetime.now().strftime("%m-%d-%Y")

    image_path = finders.find('files/PS-brand.png')
    width, height = 400, 85
    x_offset = (letter[0] - width) / 2
    y_offset = letter[1] - height - 40
    p.drawImage(image_path, x_offset, y_offset, width, height)
    
    y = y_offset - 50
    header_width = p.stringWidth(f"SEALEAD BID AUCTION", "Times-Bold", 20)
    x = (letter[0] - header_width) / 2
    p.setFont("Times-Bold", 20)
    p.drawString(x, y, f"SEALED BID AUCTION")
    
    h_width = p.stringWidth(f"Result for {participant_data['fName']}", "Times-Bold", 20)
    h_widthx = (letter[0] - h_width) / 2
    p.setFont("Times-Bold", 20)
    p.drawString(h_widthx, 595, f"Result for {participant_data['fName']}")
    
    p.setFont("Times-Roman", 14)
    p.drawString(90, 535, f"Full Name: {participant_data['fName']} {participant_data['lName']}")
    p.drawString(430, 535, f"Date: {current_date}")
    p.drawString(90, 515 , f"Email: {participant_data['email']}")
    p.drawString(430, 515 , f"ID: {participant_data['IDParticipants']}")
    
    table_data = [
        ['Total Value Won:', f"${participant_data['totalValue']}"],
        ['Fair Share:', f"${participant_data['fairShare']}"],
        ['Pay:', f"${participant_data['pay']}"],
        ['Get:', f"${participant_data['get']}"],
        ['Item/s Won:', ''],
        [f"{participant_data['itemWon']}", ','],
    ]
    rowHeights = [40, 40, 40, 40, 40, 40] 
    table = Table(table_data, colWidths=[200, 200], rowHeights=rowHeights)

    style = TableStyle([
        ('SPAN', (0, 4), (1, 4)), 
        ('SPAN', (0, 5), (1, 5)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'), 
        ('FONTSIZE', (0, 0), (-1, -1), 16),  
        ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ])
    table.setStyle(style)
    
    table_width, table_height = table.wrapOn(p, 0, 0)
    tableX = (letter[0] - table_width) / 2
    table.drawOn(p, tableX, 240)  
    
    p.showPage()
    p.save()

    return response
  