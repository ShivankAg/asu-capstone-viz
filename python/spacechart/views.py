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

# Global variable to store the ID of the last sent data point
last_sent_id = None

# Create your views here.
def index(request):
    return render(request, 'spacechart/index.html')


def fetch_initial_data(request):
    global last_sent_id

    # Retrieve all data points with IDs less than or equal to the last sent ID
    if last_sent_id is not None:
        initial_data = SpaceDucksData.objects.filter(id__lte=last_sent_id).order_by('-id')
        formatted_initial_data = []
        for data_point in initial_data:
            parsed_data = parse_data(data_point)
            formatted_data = {
                'x': format_created_at(data_point.created_at),
                'y': parsed_data.get("Altitude")
            }
            formatted_initial_data.append(formatted_data)
    else:
        initial_data = SpaceDucksData.objects.all().first()
        # Parse the initial data
        parsed_initial_data = parse_data(initial_data)

        # Prepare the initial data to pass to the template
        formatted_initial_data = {
            'x': format_created_at(initial_data.created_at),
            'y': parsed_initial_data.get("Altitude")
        }
    print(formatted_initial_data)
    return JsonResponse({'data': formatted_initial_data})

def send_data(request):
    global last_sent_id

    # If last_sent_id is None, set it to the ID of the first data point
    if last_sent_id is None:
        first_data = SpaceDucksData.objects.first()
        if first_data:
            last_sent_id = first_data.id

    # Retrieve the next object whose ID is greater than the last sent ID
    next_data = SpaceDucksData.objects.filter(id__gt=last_sent_id).first()

    if next_data is None:
        # If there are no more objects with IDs greater than the last sent ID,
        # return an empty response or handle it as needed
        return JsonResponse({})
    
    if next_data.device_id == "TARAQUR1":
        return JsonResponse({})

    # Extract the data to send
    parsed_next_data = parse_data(next_data)
    y = parsed_next_data.get("Altitude")

    # Update the last sent ID
    last_sent_id = next_data.id

    # Prepare and send the response
    print(f"Sending: x: {format_created_at(next_data.created_at)} - y:{y} from {next_data.device_id}")
    return JsonResponse({'x': format_created_at(next_data.created_at), 'y': y})
