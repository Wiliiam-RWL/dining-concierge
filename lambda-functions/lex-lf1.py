from datetime import date, time, datetime, timedelta
import boto3
import json

def validate_location(slot):
    valid = True
    location_value = slot['value']['interpretedValue']
    is_valid = location_value.lower() in ["new york", "new york city", 'nyc', 'ny', 'manhattan']
    message = None
        
    if not is_valid:
        # Invalidate the slot if validation fails
        slot['value']['interpretedValue'] = None
        valid = False
        message = "Sorry, we could not find location " + location_value +". Could you provide another area?"
    
    return valid, message

def validate_date(slot):
    message = None
    date_value = datetime.strptime(slot['value']['interpretedValue'], '%Y-%m-%d').date()
    valid = date.today() <= date_value
    if not valid:
        message = "Sorry, we can only make reservation for future or today. Could you provide anther date?"
        slot['value']['interpretedValue'] = None
    return valid, message

def validate_time(time_slot, date_slot):
    valid = True
    message = None
    date_value = datetime.strptime(date_slot['value']['interpretedValue'], '%Y-%m-%d').date()
    time_value = datetime.strptime(time_slot['value']['interpretedValue'], '%H:%M').time()
    today = datetime.now() - timedelta(hours=5)
    # aws lambda is set to get UTC time, minus 5 hours to get EST time
    if date_value == today.date() and time_value <= (datetime.now() - timedelta(hours=5) + timedelta(minutes=30)).time():
        valid = False
        time_slot['value']['interpretedValue'] = None
        message = 'Sorry, the earliest time we can book is 30 minutes later. Could you provide another time?'
        return valid, message
    morning = datetime.strptime('9:00', '%H:%M').time()
    night = datetime.strptime('23:00', '%H:%M').time()
    if time_value < morning or time_value > night:
        valid = False
        time_slot['value']['interpretedValue'] = None
        message = 'Sorry, our reservation time is from 9 am to 11 pm. Could you provide another time?'
        return valid, message
    return valid, message

def validate_people(slot):
    message = None
    valid = 1 <= int(slot['value']['interpretedValue']) <= 12
    if not valid:
        slot['value']['interpretedValue'] = None
        message = "Sorry, the range of people is from 1 to 12. Could you provide another number?"
    return valid, message
    

def validate_slots(slots):
    location_slot = slots['Location']
    date_slot = slots['Date']
    time_slot = slots['Time']
    people_slot = slots['NumberOfPeople']

    if location_slot is not None:
        valid, message = validate_location(location_slot)
        if not valid:
            return slots, valid, message, 'Location'
    if date_slot is not None:
        valid, message = validate_date(date_slot)
        if not valid:
            return slots, valid, message, 'Date'
    if time_slot is not None:
        valid, message = validate_time(time_slot,date_slot)
        if not valid:
            return slots, valid, message, 'Time'
    if people_slot is not None:
        valid, message = validate_people(people_slot)
        if not valid:
            return slots, valid, message, 'NumberOfPeople'
            
    return slots, True, None, None

def construct_response(event, slots, valid, message=None, slot_to_elicit=None):
    if valid:
        dialogActionType = "Delegate"
    else:
        # If validation fails for a slot, indicate which slot to elicit next
        dialogActionType = "ElicitSlot"

    response = {
        "sessionState": {
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "slots": slots,
                "state": "InProgress",
            },
            "dialogAction": {
                "type": dialogActionType
            }
        },
    }

    if not valid:
        response["sessionState"]["dialogAction"]["slotToElicit"] = slot_to_elicit
        # Add a message to guide the user for the invalid slot
        response["messages"] = [{"contentType": "PlainText", "content": message}]

    return response



def lambda_handler(event, context):
    print(event)
    # Determine the slot currently being processed
    invocation_source = event['invocationSource']
    
    if invocation_source == "DialogCodeHook":
        # Extract the slots and the current slot being filled from the event
        slots = event['sessionState']['intent']['slots']

        print("Slots:\n", slots)
        
        # Validate the slot
        validated_slots, valid, message, slot_to_elicit = validate_slots(slots)
        
        # Construct a response based on validation
        response = construct_response(event, validated_slots, valid, message, slot_to_elicit)
        return response
    elif invocation_source == "FulfillmentCodeHook":
        slots = event['sessionState']['intent']['slots']
        slots_values = {slot:value['value']['interpretedValue'] for slot,value in slots.items()}
        sqs_message = json.dumps(slots_values)
        sqs_url = 'https://sqs.us-east-1.amazonaws.com/894311263883/dining-slot-lf1-Q1'
        sqs = boto3.client('sqs')
        sqs_response = sqs.send_message(QueueUrl=sqs_url, MessageBody = sqs_message)
        print(sqs_response)
        return {
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": {
                "state": "ReadyForFulfillment",
                "name": event['sessionState']['intent']['name'],
                # Include necessary intent and slot information
            }
        }
    }
