"""
C: counter
LT: latitude
LG: longitude
IT: internal temp
ET: external temp
IP: internal pressure
EP: external pressure
IA: altitude
EA: external altitude
MX: vibration x-axis
MY: vibration y-axis
MZ: vibration z-axis
AX: acceleration x-axis
AY: acceleration y-axis
AZ: acceleration z-axis
GX: gravitation x-axis
GY: gravitation y-axis
GZ: gravitation z-axis
"""


import pandas as pd
import json
import re
import string

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
    "MX": "Vibration X-axis",
    "MY": "Vibration Y-axis",
    "MZ": "Vibration Z-axis",
    "AX": "Acceleration X-axis",
    "AY": "Acceleration Y-axis",
    "AZ": "Acceleration Z-axis",
    "GX": "Gravitation X-axis",
    "GY": "Gravitation Y-axis",
    "GZ": "Gravitation Z-axis",
}


df = pd.read_csv("./SpaceDucksData.csv")
print(df.head())
payload_dict_array = []

for payload in df["payload"]:
    payload_json = json.loads(payload)
    only_msg = payload_json['Payload']
    pairs = re.findall(r'([A-Z]+)([^A-Z]+)', only_msg)
    # print(pairs)
    payload_dict = {}
    for key, value in pairs:
        if key in keyword_mapping:
            cleaned_value = re.sub(r'[:,\s]+', '', value)
            payload_dict[keyword_mapping[key]] = cleaned_value
    payload_dict_array.append(payload_dict)
payload_df = pd.DataFrame(payload_dict_array)
df_merged = df.join(payload_df)
df_merged.to_csv('ParsedSpaceDucksData.csv', index=False)