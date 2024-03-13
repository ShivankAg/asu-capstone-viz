from django.shortcuts import render
from django.http import JsonResponse
from .models import SpaceDucksData
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
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

"""
Translated into backend code using Shivank's distance.js
"""
import math

def get_distance_from_lat_lon_km(lat1, lon1, lat2, lon2):
    # Returns distance in km and angle in degrees
    R = 6371  # Radius of the earth in km
    d_lat = degrees_to_radians(lat2 - lat1)  # degreesToRadians below
    d_lon = degrees_to_radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(degrees_to_radians(lat1)) * math.cos(
        degrees_to_radians(lat2)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # Distance in km

    y = math.sin(d_lon) * math.cos(degrees_to_radians(lat2))
    x = math.cos(degrees_to_radians(lat1)) * math.sin(degrees_to_radians(lat2)) - math.sin(
        degrees_to_radians(lat1)) * math.cos(degrees_to_radians(lat2)) * math.cos(d_lon)
    angle_radians = math.atan2(y, x)
    angle_degrees = ((angle_radians * 180) / math.pi + 360) % 360

    return d, angle_degrees

def degrees_to_radians(degrees):
    return (degrees * math.pi) / 180

def radians_to_degrees(radians):
    return (radians * 180) / math.pi

def calculate_new_coordinates(latitude, longitude, bearing, distance):
    earth_radius_km = 6371
    angular_distance = distance / earth_radius_km  # Convert distance to angular distance

    lat1 = degrees_to_radians(latitude)
    lon1 = degrees_to_radians(longitude)
    bearing_radians = degrees_to_radians(bearing)

    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance) +
        math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing_radians)
    )
    lon2 = lon1 + math.atan2(
        math.sin(bearing_radians) * math.sin(angular_distance) * math.cos(lat1),
        math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2)
    )

    return {
        'latitude': radians_to_degrees(lat2),
        'longitude': radians_to_degrees(lon2),
    }

def time_to_hit_ground(velocity, height):
    g = -9.81
    discriminant = math.sqrt(math.pow(velocity, 2) + 2 * g * height)
    time = (-velocity + discriminant) / g

    return time

def new_point_added(last_data_point, second_last_data_point):
    gravity = -9.81

    # Calculate y velocity
    time_difference = format_created_at(last_data_point['created_at']) - format_created_at(second_last_data_point['created_at'])
    y_velocity = gravity * time_difference

    if float(last_data_point['Altitude']) > float(second_last_data_point['Altitude']):
        # If we are still rising, we don't make predictions
        print("Still rising!")
        return False

    time_remaining = time_to_hit_ground(y_velocity, float(last_data_point['Altitude']))
    print("Time to hit the ground (s):", time_remaining)

    # Get x velocity
    temp = get_distance_from_lat_lon_km(
        float(second_last_data_point['Latitude']),
        float(second_last_data_point['Longitude']),
        float(last_data_point['Latitude']),
        float(last_data_point['Longitude'])
    )
    distance_between_points = temp[0]
    angle_between_points = temp[1]

    speed = distance_between_points / time_difference

    # Predicted distance to travel
    travel_distance = speed * time_remaining

    # Predicted coordinates
    new_coords = calculate_new_coordinates(
        float(last_data_point['Latitude']),
        float(last_data_point['Longitude']),
        angle_between_points,
        travel_distance
    )
    print("New Latitude: ", new_coords['latitude'])
    print("New Longitude: ", new_coords['longitude'])

    return True
# End prediction code



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
                'y': parsed_data
            }
            formatted_initial_data.append(formatted_data)
    else:
        initial_data = SpaceDucksData.objects.all().first()
        # Parse the initial data
        parsed_initial_data = parse_data(initial_data)

        # Prepare the initial data to pass to the template
        formatted_initial_data = {
            'x': format_created_at(initial_data.created_at),
            'y': parsed_initial_data
        }
    # print(formatted_initial_data)
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
    y = parsed_next_data

    # Update the last sent ID
    last_sent_id = next_data.id

    # Prepare and send the response
    # print(f"Sending: x: {format_created_at(next_data.created_at)} - y:{y} from {next_data.device_id}")
    return JsonResponse({'x': format_created_at(next_data.created_at), 'y': y})

def predict():
    global last_sent_id

    # Retrieve the last two sent data points
    last_data_point = SpaceDucksData.objects.get(id=last_sent_id)
    second_last_data_point = SpaceDucksData.objects.filter(id__lt=last_sent_id).order_by('-id').first()

    if last_data_point is None or second_last_data_point is None:
        print("Not enough data points to make a prediction.")
        return

    # Parse the data points
    parsed_last_data_point = parse_data(last_data_point)
    parsed_second_last_data_point = parse_data(second_last_data_point)

    # Call new_point_added function to predict the next point
    prediction_result = new_point_added(parsed_last_data_point, parsed_second_last_data_point)

    if prediction_result:
        print("Prediction successful.")
    else:
        print("Prediction failed.")

def predict_next_point(request):
    # Call the predict_next_point function
    predict()

    # Return a JsonResponse indicating success
    return JsonResponse({'message': 'Prediction initiated.'})


