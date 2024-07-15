import json
from datetime import datetime
import os

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths for the JSON files
obstacle_file_path = os.path.join(base_dir, 'data', 'type', 'obstacle_type.json')

# Obstacle Type Data
obstacle_data = {
    "obstacle_type": "Car"
}

# Write the obstacle data to the JSON file
with open(obstacle_file_path, 'w') as f:
    json.dump(obstacle_data, f)
