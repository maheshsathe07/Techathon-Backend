# from datetime import datetime, timedelta
# from src.config.config import get_collection

# class AccidentAnalyticsManager:
#     def __init__(self):
#         self.collection = get_collection()

#     def _safe_round(self, value, decimals=2):
#         """Safely round a value that might be None"""
#         return round(float(value), decimals) if value is not None else 0.0

#     def get_hourly_data(self):
#         """Get hourly accident data for last 24 hours"""
#         try:
#             end_time = datetime.utcnow()
#             start_time = end_time - timedelta(hours=24)
            
#             pipeline = [
#                 {
#                     "$match": {
#                         "timestamp": {
#                             "$gte": start_time,
#                             "$lte": end_time
#                         }
#                     }
#                 },
#                 {
#                     "$group": {
#                         "_id": {
#                             "$dateToString": {
#                                 "format": "%H:00",
#                                 "date": "$timestamp"
#                             }
#                         },
#                         "count": {"$sum": 1},
#                         "avg_response_time": {"$avg": "$response_time"}
#                     }
#                 },
#                 {"$sort": {"_id": 1}}
#             ]
            
#             results = list(self.collection.aggregate(pipeline))
            
#             # Fill missing hours
#             hours_data = {}
#             for i in range(24):
#                 hour_str = f"{i:02d}:00"
#                 hours_data[hour_str] = {
#                     "hour": hour_str,
#                     "count": 0,
#                     "avg_response_time": 0.0
#                 }
            
#             for result in results:
#                 hours_data[result["_id"]] = {
#                     "hour": result["_id"],
#                     "count": result["count"],
#                     "avg_response_time": self._safe_round(result.get("avg_response_time", 0))
#                 }
            
#             return {
#                 "data": list(hours_data.values()),
#                 "total_accidents": sum(item["count"] for item in hours_data.values())
#             }
            
#         except Exception as e:
#             raise Exception(f"Error fetching hourly data: {str(e)}")

#     def get_daily_data(self):
#         """Get daily accident data for last 7 days"""
#         try:
#             end_time = datetime.utcnow()
#             start_time = end_time - timedelta(days=7)
            
#             pipeline = [
#                 {
#                     "$match": {
#                         "timestamp": {
#                             "$gte": start_time,
#                             "$lte": end_time
#                         }
#                     }
#                 },
#                 {
#                     "$group": {
#                         "_id": {
#                             "$dateToString": {
#                                 "format": "%Y-%m-%d",
#                                 "date": "$timestamp"
#                             }
#                         },
#                         "count": {"$sum": 1},
#                         "severity": {
#                             "$push": "$severity"
#                         }
#                     }
#                 },
#                 {"$sort": {"_id": 1}}
#             ]
            
#             results = list(self.collection.aggregate(pipeline))
#             formatted_data = []
            
#             # Fill missing days
#             date_dict = {}
#             current = start_time
#             while current <= end_time:
#                 date_str = current.strftime("%Y-%m-%d")
#                 date_dict[date_str] = {
#                     "date": date_str,
#                     "total": 0,
#                     "severity_breakdown": {"High": 0, "Medium": 0, "Low": 0}
#                 }
#                 current += timedelta(days=1)
            
#             for result in results:
#                 severity_counts = {
#                     "High": result["severity"].count("High"),
#                     "Medium": result["severity"].count("Medium"),
#                     "Low": result["severity"].count("Low")
#                 }
#                 date_dict[result["_id"]] = {
#                     "date": result["_id"],
#                     "total": result["count"],
#                     "severity_breakdown": severity_counts
#                 }
            
#             formatted_data = list(date_dict.values())
            
#             return {
#                 "data": formatted_data,
#                 "total_accidents": sum(item["total"] for item in formatted_data)
#             }
            
#         except Exception as e:
#             raise Exception(f"Error fetching daily data: {str(e)}")

#     def get_monthly_data(self):
#         """Get monthly accident data for last 12 months"""
#         try:
#             end_time = datetime.utcnow()
#             start_time = end_time - timedelta(days=365)
            
#             pipeline = [
#                 {
#                     "$match": {
#                         "timestamp": {
#                             "$gte": start_time,
#                             "$lte": end_time
#                         }
#                     }
#                 },
#                 {
#                     "$group": {
#                         "_id": {
#                             "$dateToString": {
#                                 "format": "%Y-%m",
#                                 "date": "$timestamp"
#                             }
#                         },
#                         "count": {"$sum": 1},
#                         "avg_response_time": {"$avg": "$response_time"},
#                         "road_types": {"$push": "$road_type"}
#                     }
#                 },
#                 {"$sort": {"_id": 1}}
#             ]
            
#             results = list(self.collection.aggregate(pipeline))
            
#             # Fill missing months
#             month_dict = {}
#             current = start_time
#             while current <= end_time:
#                 month_str = current.strftime("%Y-%m")
#                 month_dict[month_str] = {
#                     "month": month_str,
#                     "total": 0,
#                     "avg_response_time": 0.0,
#                     "road_type_breakdown": {}
#                 }
#                 current = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
            
#             for result in results:
#                 road_type_counts = {}
#                 for road_type in result["road_types"]:
#                     road_type_counts[road_type] = road_type_counts.get(road_type, 0) + 1
                    
#                 month_dict[result["_id"]] = {
#                     "month": result["_id"],
#                     "total": result["count"],
#                     "avg_response_time": self._safe_round(result.get("avg_response_time", 0)),
#                     "road_type_breakdown": road_type_counts
#                 }
            
#             formatted_data = list(month_dict.values())
            
#             return {
#                 "data": formatted_data,
#                 "total_accidents": sum(item["total"] for item in formatted_data)
#             }
            
#         except Exception as e:
#             raise Exception(f"Error fetching monthly data: {str(e)}")

#     def get_hotspots_data(self):
#         try:
#             # Calculate the date 10 days ago from now
#             ten_days_ago = datetime.utcnow() - timedelta(days=10)
            
#             pipeline = [
#                 {
#                     "$match": {
#                         "timestamp": {"$gte": ten_days_ago}
#                     }
#                 },
#                 {
#                     # Group by grid cells (0.002 degrees ≈ 222 meters for creating 2km grid)
#                     "$group": {
#                         "_id": {
#                             "lat": {
#                                 "$multiply": [
#                                     {"$floor": {"$multiply": ["$latitude", 500]}},
#                                     0.002
#                                 ]
#                             },
#                             "lon": {
#                                 "$multiply": [
#                                     {"$floor": {"$multiply": ["$longitude", 500]}},
#                                     0.002
#                                 ]
#                             },
#                             "road_type": "$road_type"
#                         },
#                         "accident_count": {"$sum": 1},
#                         "location": {
#                             "$first": {
#                                 "latitude": "$latitude",
#                                 "longitude": "$longitude"
#                             }
#                         },
#                         "avg_response_time": {"$avg": "$response_time"},
#                         "last_accident": {"$max": "$timestamp"},
#                         "accidents": {
#                             "$push": {
#                                 "timestamp": "$timestamp",
#                                 "severity": "$severity",
#                                 "weather_condition": "$weather_condition"
#                             }
#                         }
#                     }
#                 },
#                 {
#                     "$addFields": {
#                         "severity_level": {
#                             "$switch": {
#                                 "branches": [
#                                     {"case": {"$gte": ["$accident_count", 10]}, "then": "High"},
#                                     {"case": {"$gte": ["$accident_count", 5]}, "then": "Medium"},
#                                     {"case": {"$gte": ["$accident_count", 1]}, "then": "Low"}
#                                 ],
#                                 "default": "Low"
#                             }
#                         }
#                     }
#                 },
#                 {
#                     "$match": {
#                         "accident_count": {"$gte": 1}  # Only include areas with at least 1 accident
#                     }
#                 },
#                 {
#                     "$project": {
#                         "location": 1,
#                         "road_type": "$_id.road_type",
#                         "accident_count": 1,
#                         "severity_level": 1,
#                         "avg_response_time": 1,
#                         "last_accident": 1
#                     }
#                 },
#                 {
#                     "$sort": {"accident_count": -1}
#                 }
#             ]

#             results = list(self.collection.aggregate(pipeline))
            
#             formatted_hotspots = []
#             for spot in results:
#                 formatted_hotspots.append({
#                     "location": {
#                         "latitude": spot["location"]["latitude"],
#                         "longitude": spot["location"]["longitude"]
#                     },
#                     "road_type": spot.get("road_type", "Unknown"),
#                     "total_accidents": spot["accident_count"],
#                     "severity_level": spot["severity_level"],
#                     "high_severity_percentage": self._calculate_severity_percentage(spot["severity_level"]),
#                     "avg_response_time": self._safe_round(spot.get("avg_response_time", 0)),
#                     "last_accident": spot["last_accident"].strftime("%Y-%m-%d %H:%M")
#                 })

#             return {
#                 "hotspots": formatted_hotspots,
#                 "total_hotspots": len(formatted_hotspots),
#                 "query_parameters": {
#                     "grid_size_km": 2,  # 2km grid cells
#                     "days_lookback": 10,
#                     "severity_thresholds": {
#                         "high": 10,
#                         "medium": 5,
#                         "low": 1
#                     }
#                 }
#             }

#         except Exception as e:
#             print(f"Debug error: {str(e)}")
#             return {
#                 "hotspots": [],
#                 "total_hotspots": 0,
#                 "query_parameters": {
#                     "grid_size_km": 2,
#                     "days_lookback": 10,
#                     "severity_thresholds": {
#                         "high": 10,
#                         "medium": 5,
#                         "low": 1
#                     }
#                 },
#                 "error": str(e)
#             }

#     def _calculate_severity_percentage(self, severity_level):
#         """Calculate severity percentage based on severity level"""
#         if severity_level == "High":
#             return 100
#         elif severity_level == "Medium":
#             return 50
#         else:
#             return 25

#     def _safe_round(self, value, decimals=2):
#         """Safely round a value that might be None"""
#         try:
#             return round(float(value), decimals) if value is not None else 0
#         except (TypeError, ValueError):
#             return 0


from datetime import datetime, timedelta
from src.config.config import get_collection
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from functools import lru_cache

class AccidentAnalyticsManager:
    def __init__(self):
        self.collection = get_collection()
        self.geolocator = Nominatim(user_agent="accident_analytics_app")
        self.last_request_time = 0
        self.min_delay = 1.1  # Minimum delay between requests in seconds

    def _safe_round(self, value, decimals=2):
        """Safely round a value that might be None"""
        return round(float(value), decimals) if value is not None else 0.0

    def get_hourly_data(self):
        """Get hourly accident data for last 24 hours"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=24)
            
            pipeline = [
                {
                    "$match": {
                        "timestamp": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%H:00",
                                "date": "$timestamp"
                            }
                        },
                        "count": {"$sum": 1},
                        "avg_response_time": {"$avg": "$response_time"}
                    }
                },
                {"$sort": {"_id": 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            # Fill missing hours
            hours_data = {}
            for i in range(24):
                hour_str = f"{i:02d}:00"
                hours_data[hour_str] = {
                    "hour": hour_str,
                    "count": 0,
                    "avg_response_time": 0.0
                }
            
            for result in results:
                hours_data[result["_id"]] = {
                    "hour": result["_id"],
                    "count": result["count"],
                    "avg_response_time": self._safe_round(result.get("avg_response_time", 0))
                }
            
            return {
                "data": list(hours_data.values()),
                "total_accidents": sum(item["count"] for item in hours_data.values())
            }
            
        except Exception as e:
            raise Exception(f"Error fetching hourly data: {str(e)}")

    def get_daily_data(self):
        """Get daily accident data for last 7 days"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)
            
            pipeline = [
                {
                    "$match": {
                        "timestamp": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$timestamp"
                            }
                        },
                        "count": {"$sum": 1},
                        "severity": {
                            "$push": "$severity"
                        }
                    }
                },
                {"$sort": {"_id": 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            formatted_data = []
            
            # Fill missing days
            date_dict = {}
            current = start_time
            while current <= end_time:
                date_str = current.strftime("%Y-%m-%d")
                date_dict[date_str] = {
                    "date": date_str,
                    "total": 0,
                    "severity_breakdown": {"High": 0, "Medium": 0, "Low": 0}
                }
                current += timedelta(days=1)
            
            for result in results:
                severity_counts = {
                    "High": result["severity"].count("High"),
                    "Medium": result["severity"].count("Medium"),
                    "Low": result["severity"].count("Low")
                }
                date_dict[result["_id"]] = {
                    "date": result["_id"],
                    "total": result["count"],
                    "severity_breakdown": severity_counts
                }
            
            formatted_data = list(date_dict.values())
            
            return {
                "data": formatted_data,
                "total_accidents": sum(item["total"] for item in formatted_data)
            }
            
        except Exception as e:
            raise Exception(f"Error fetching daily data: {str(e)}")

    def get_monthly_data(self):
        """Get monthly accident data for last 12 months"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=365)
            
            pipeline = [
                {
                    "$match": {
                        "timestamp": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m",
                                "date": "$timestamp"
                            }
                        },
                        "count": {"$sum": 1},
                        "avg_response_time": {"$avg": "$response_time"},
                        "road_types": {"$push": "$road_type"}
                    }
                },
                {"$sort": {"_id": 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            # Fill missing months
            month_dict = {}
            current = start_time
            while current <= end_time:
                month_str = current.strftime("%Y-%m")
                month_dict[month_str] = {
                    "month": month_str,
                    "total": 0,
                    "avg_response_time": 0.0,
                    "road_type_breakdown": {}
                }
                current = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
            
            for result in results:
                road_type_counts = {}
                for road_type in result["road_types"]:
                    road_type_counts[road_type] = road_type_counts.get(road_type, 0) + 1
                    
                month_dict[result["_id"]] = {
                    "month": result["_id"],
                    "total": result["count"],
                    "avg_response_time": self._safe_round(result.get("avg_response_time", 0)),
                    "road_type_breakdown": road_type_counts
                }
            
            formatted_data = list(month_dict.values())
            
            return {
                "data": formatted_data,
                "total_accidents": sum(item["total"] for item in formatted_data)
            }
            
        except Exception as e:
            raise Exception(f"Error fetching monthly data: {str(e)}")

    def _respect_rate_limit(self):
        """Ensure we respect Nominatim's rate limit"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)
        self.last_request_time = time.time()

    @lru_cache(maxsize=1000)
    def _get_location_name(self, latitude, longitude):
        """
        Get location name from coordinates using OpenStreetMap/Nominatim
        Uses caching to minimize API calls
        """
        try:
            self._respect_rate_limit()
            location = self.geolocator.reverse(f"{latitude}, {longitude}", language="en")
            
            if location and location.raw.get('address'):
                address = location.raw['address']
                
                # Try to build the most meaningful location string
                components = []
                
                # Try to get the street name first
                if address.get('road'):
                    components.append(address['road'])
                elif address.get('pedestrian'):
                    components.append(address['pedestrian'])
                elif address.get('highway'):
                    components.append(address['highway'])
                
                # Add area/neighborhood for context
                if address.get('suburb'):
                    components.append(address['suburb'])
                elif address.get('neighbourhood'):
                    components.append(address['neighbourhood'])
                
                # Add city/town if available
                if address.get('city'):
                    components.append(address['city'])
                elif address.get('town'):
                    components.append(address['town'])
                elif address.get('village'):
                    components.append(address['village'])
                
                if components:
                    return ", ".join(components)
                    
                # Fallback to formatted address if we couldn't build a meaningful string
                return location.address if location.address else "Unknown Location"
            
            return "Unknown Location"
            
        except GeocoderTimedOut:
            # Handle timeout specifically
            print(f"Geocoding timed out for coordinates: {latitude}, {longitude}")
            return "Location Lookup Timed Out"
        except Exception as e:
            print(f"Error in geocoding: {str(e)}")
            return "Unknown Location"

    def get_hotspots_data(self):
        try:
            ten_days_ago = datetime.utcnow() - timedelta(days=10)
            
            pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": ten_days_ago}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "lat": {
                                "$multiply": [
                                    {"$floor": {"$multiply": ["$latitude", 500]}},
                                    0.002
                                ]
                            },
                            "lon": {
                                "$multiply": [
                                    {"$floor": {"$multiply": ["$longitude", 500]}},
                                    0.002
                                ]
                            },
                            "road_type": "$road_type"
                        },
                        "accident_count": {"$sum": 1},
                        "location": {
                            "$first": {
                                "latitude": "$latitude",
                                "longitude": "$longitude"
                            }
                        },
                        "avg_response_time": {"$avg": "$response_time"},
                        "last_accident": {"$max": "$timestamp"},
                        "accidents": {
                            "$push": {
                                "timestamp": "$timestamp",
                                "severity": "$severity",
                                "weather_condition": "$weather_condition"
                            }
                        }
                    }
                },
                {
                    "$addFields": {
                        "severity_level": {
                            "$switch": {
                                "branches": [
                                    {"case": {"$gte": ["$accident_count", 10]}, "then": "High"},
                                    {"case": {"$gte": ["$accident_count", 5]}, "then": "Medium"},
                                    {"case": {"$gte": ["$accident_count", 1]}, "then": "Low"}
                                ],
                                "default": "Low"
                            }
                        }
                    }
                },
                {
                    "$match": {
                        "accident_count": {"$gte": 1}
                    }
                },
                {"$sort": {"accident_count": -1}},
                {"$limit": 100}  # Limit results to avoid too many geocoding requests
            ]

            results = list(self.collection.aggregate(pipeline))
            
            formatted_hotspots = []
            for spot in results:
                # Get location name from coordinates
                location_name = self._get_location_name(
                    spot["location"]["latitude"],
                    spot["location"]["longitude"]
                )
                
                formatted_hotspots.append({
                    "location": {
                        "name": location_name,
                        "latitude": spot["location"]["latitude"],
                        "longitude": spot["location"]["longitude"]
                    },
                    "road_type": spot.get("road_type", "Unknown"),
                    "total_accidents": spot["accident_count"],
                    "severity_level": spot["severity_level"],
                    "high_severity_percentage": self._calculate_severity_percentage(spot["severity_level"]),
                    "avg_response_time": self._safe_round(spot.get("avg_response_time", 0)),
                    "last_accident": spot["last_accident"].strftime("%Y-%m-%d %H:%M")
                })

            return {
                "hotspots": formatted_hotspots,
                "total_hotspots": len(formatted_hotspots),
                "query_parameters": {
                    "grid_size_km": 2,
                    "days_lookback": 10,
                    "severity_thresholds": {
                        "high": 10,
                        "medium": 5,
                        "low": 1
                    }
                }
            }

        except Exception as e:
            print(f"Debug error: {str(e)}")
            return {
                "hotspots": [],
                "total_hotspots": 0,
                "query_parameters": {
                    "grid_size_km": 2,
                    "days_lookback": 10,
                    "severity_thresholds": {
                        "high": 10,
                        "medium": 5,
                        "low": 1
                    }
                },
                "error": str(e)
            }
    
    def _calculate_severity_percentage(self, severity_level):
        """Calculate severity percentage based on severity level"""
        if severity_level == "High":
            return 100
        elif severity_level == "Medium":
            return 50
        else:
            return 25

    def _safe_round(self, value, decimals=2):
        """Safely round a value that might be None"""
        try:
            return round(float(value), decimals) if value is not None else 0
        except (TypeError, ValueError):
            return 0