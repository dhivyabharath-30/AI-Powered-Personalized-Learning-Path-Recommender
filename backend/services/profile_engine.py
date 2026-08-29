from typing import List, Dict, Optional
from datetime import datetime
from services.shared_state import shared_state


class ProfileEngine:
    def __init__(self):
        self.shared_state = shared_state
    
    def create_or_update_profile(
        self,
        user_id: str,
        interests: List[str],
        experience_level: str,
        goals: List[str],
        completed_courses: Optional[List[str]] = None
    ) -> Dict:
        profile = {
            "user_id": user_id,
            "interests": interests,
            "experience_level": experience_level,
            "goals": goals,
            "completed_courses": completed_courses or [],
            "skills": self._extract_skills(completed_courses or []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.shared_state.set_profile(user_id, profile)
        return profile
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        return self.shared_state.get_profile(user_id)
    
    def _extract_skills(self, completed_courses: List[str]) -> List[str]:
        skill_mapping = {
            "python": ["Python", "Programming", "Backend"],
            "javascript": ["JavaScript", "Frontend", "Web Development"],
            "react": ["React", "Frontend", "UI Development"],
            "machine learning": ["ML", "AI", "Data Science"],
            "data science": ["Data Analysis", "Statistics", "Python"]
        }
        
        skills = set()
        for course in completed_courses:
            course_lower = course.lower()
            for key, values in skill_mapping.items():
                if key in course_lower:
                    skills.update(values)
        
        return list(skills)
    
    def get_learning_progress(self, user_id: str) -> Dict:
        profile = self.get_profile(user_id)
        if not profile:
            return {}
        
        return {
            "user_id": user_id,
            "completed_courses": len(profile.get("completed_courses", [])),
            "skills_acquired": len(profile.get("skills", [])),
            "active_goals": len(profile.get("goals", [])),
            "progress_percentage": self._calculate_progress(profile)
        }
    
    def _calculate_progress(self, profile: Dict) -> int:
        completed = len(profile.get("completed_courses", []))
        goals = len(profile.get("goals", []))
        
        if goals == 0:
            return 0
        
        return min(int((completed / (goals * 3)) * 100), 100)
