from django.shortcuts import render
from django.http import JsonResponse
from .models import SpaceDucksData
from django.utils import timezone
from datetime import datetime
import json
import re


keyword_mapping = {
    "C": "Counter",
    "LT": "Latitude",
    "LG": "Longitude",
    "IT": "Internal Temp",
    "ET": "External Temp",
    "IP": "Internal Pressure",
    "EP": "External Pressure",
    "IA": "Altitude",
    "EA": "External Altitude",
    "MX": "Magnetic X-axis",
    "MY": "Magnetic Y-axis",
    "MZ": "Magnetic Z-axis",
    "AX": "Acceleration X-axis",
    "AY": "Acceleration Y-axis",
    "AZ": "Acceleration Z-axis",
    "GX": "Gyroscope X-axis",
    "GY": "Gyroscope Y-axis",
    "GZ": "Gyroscope Z-axis",
}


# Helper functions:
def parse_data(spaceduck_data):
    payload_from_data = spaceduck_data.payload
    payload_json = json.loads(payload_from_data)
    only_msg = payload_json['Payload']
    pairs = re.findall(r'([A-Z]+)([^A-Z]+)', only_msg)
    data_dict = {}
    for field_name, field_value in spaceduck_data.__dict__.items():
        if field_name != "payload":
            if field_name != "_state":
                data_dict[field_name] = field_value
    for key, value in pairs:
        if key in keyword_mapping:
            cleaned_value = re.sub(r'[:,\s]+', '', value)
            data_dict[keyword_mapping[key]] = cleaned_value
    return data_dict

def format_created_at(created_at_str):
    # Remove the timezone offset (+00)
    created_at_str = created_at_str[:-3]

    # Convert the string representation of datetime to a datetime object
    created_at_datetime = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S.%f")

    # Convert the datetime object to a timestamp
    return created_at_datetime.timestamp()



# Create your views here.
def index(request):
    # Retrieve the first object
    first_data = SpaceDucksData.objects.first()

    # Store the ID of the first object in the session
    if first_data:
        request.session['last_sent_id'] = first_data.id

    # Prepare the initial data to pass to the template
    initial_data = {}
    if first_data:
        data_dict = parse_data(first_data)
        initial_data['x'] = format_created_at(first_data.created_at)
        initial_data['y'] = data_dict.get("Altitude")

    return render(request, 'spacechart/index.html', {'data': initial_data})

def send_data(request):
    # Get the ID of the last sent object from the session
    last_sent_id = request.session.get('last_sent_id')

    # Retrieve the next object whose ID is greater than the last sent ID
    next_data = SpaceDucksData.objects.filter(id__gt=last_sent_id).first()

    if next_data is None:
        # If there are no more objects with IDs greater than the last sent ID,
        # return an empty response or handle it as needed
        return JsonResponse({})

    # Extract the data to send
    data_dict = parse_data(next_data)
    y = data_dict.get("Altitude")

    # Update the last sent ID in the session
    request.session['last_sent_id'] = next_data.id

    # Prepare and send the response
    print(f"Sending: x: {format_created_at(next_data.created_at)} - y:{y} from {next_data.device_id}")
    return JsonResponse({'x': format_created_at(next_data.created_at), 'y': y})