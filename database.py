from pymongo import MongoClient
from typing import List, Dict, Any

class Database:
    """Database service for MongoDB operations"""
    
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def insert_event(self, event_data: Dict[str, Any]) -> bool:
        """Insert a single event into the database"""
        try:
            self.collection.insert_one(event_data)
            return True
        except Exception as e:
            print(f"Database insert error: {e}")
            return False
    
    def get_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve recent events from the database"""
        try:
            events = list(self.collection.find(
                {},
                {'_id': 0}
            ).sort('timestamp', -1).limit(limit))
            return events
        except Exception as e:
            print(f"Database query error: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()