import json
from datetime import datetime
import os

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths for the JSON files
distance_file_path = os.path.join(base_dir, 'data', 'distance', 'ultra_sonic_distance.json')

# Ultra Sonic Distance Data
distance_data = {
    "ultra_sonic_distance": 1200
}

# Write the distance data to the JSON file
with open(distance_file_path, 'w') as f:
    json.dump(distance_data, f)