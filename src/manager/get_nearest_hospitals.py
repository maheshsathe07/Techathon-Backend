from math import radians, cos, sin, sqrt, atan2
from src.config.config import get_collection_1

def get_nearest_hospitals(lat, lon, limit=5):
    collection = get_collection_1()
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in kilometers

        # Convert latitude and longitude to radians
        lat1, lon1 = radians(lat1), radians(lon1)
        lat2, lon2 = radians(lat2), radians(lon2)
        
        # Differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance

    # Get all hospitals from database
    hospitals = list(collection.find({}, {
        'name': 1,
        'latitude': 1,
        'longitude': 1,
        'contact_number': 1,
        'address': 1
    }))
    
    print(hospitals)
    # Calculate distance for each hospital
    for hospital in hospitals:
        distance = calculate_distance(
            lat,
            lon,
            hospital['latitude'],
            hospital['longitude']
        )
        hospital['distance'] = distance
    
    # Sort hospitals by distance and get top 5
    nearest_hospitals = sorted(hospitals, key=lambda x: x['distance'])[:limit]
    
    # Format the output
    result = []
    for hospital in nearest_hospitals:
        result.append({
            'name': hospital['name'],
            'contact_number': hospital['contact_number'],
            'address': hospital['address'],
        })
    
    return result