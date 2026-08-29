"""
Shared state manager to ensure all services access the same data
"""
from typing import Dict


class SharedState:
    """Singleton class to manage shared state across services"""
    _instance = None
    _profiles: Dict = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._profiles = {}
        return cls._instance
    
    @property
    def profiles(self) -> Dict:
        return self._profiles
    
    def set_profile(self, user_id: str, profile: Dict):
        self._profiles[user_id] = profile
    
    def get_profile(self, user_id: str) -> Dict:
        return self._profiles.get(user_id)
    
    def clear_all(self):
        """For testing purposes"""
        self._profiles = {}


# Global shared state instance
shared_state = SharedState()
