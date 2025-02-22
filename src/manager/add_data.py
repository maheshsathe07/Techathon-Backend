from src.config.config import get_collection
from datetime import datetime

def add_new_location(latitude, longitude):
    """
    Add a new location data point to the MongoDB collection.
    """
    try:
        collection = get_collection()  # Get the MongoDB collection
        
        # Prepare the location data
        location_data = {
            "timestamp": datetime.utcnow(),
            "latitude": float(latitude),
            "longitude": float(longitude)
        }
        
        # Insert the new location into the collection
        result = collection.insert_one(location_data)
        return result.inserted_id
    
    except Exception as e:
        raise Exception(f"Error adding location data: {str(e)}")