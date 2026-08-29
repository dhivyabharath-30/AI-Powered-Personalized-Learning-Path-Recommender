from typing import List, Dict
from datetime import datetime, timedelta


class LearningPathGenerator:
    def __init__(self):
        self.courses_db = self._load_courses()
    
    def _load_courses(self) -> List[Dict]:
        from services.recommendation_engine import RecommendationEngine
        engine = RecommendationEngine()
        return engine.courses_db
    
    async def generate_path(
        self,
        user_id: str,
        goal: str,
        timeframe: str = "3 months"
    ) -> Dict:
        from services.shared_state import shared_state
        profile = shared_state.get_profile(user_id)
        
        if not profile:
            return {"error": "Profile not found"}
        
        user_skills = set(profile.get("skills", []))
        experience_level = profile.get("experience_level", "Beginner")
        
        relevant_courses = self._find_relevant_courses(goal, user_skills, experience_level)
        
        ordered_path = self._order_by_prerequisites(relevant_courses, user_skills)
        
        milestones = self._create_milestones(ordered_path, timeframe)
        
        return {
            "user_id": user_id,
            "goal": goal,
            "timeframe": timeframe,
            "total_courses": len(ordered_path),
            "estimated_hours": sum(self._parse_duration(c.get("duration", "4 weeks")) for c in ordered_path),
            "path": ordered_path,
            "milestones": milestones,
            "explanation": self._generate_path_explanation(goal, ordered_path)
        }
    
    def _find_relevant_courses(
        self,
        goal: str,
        user_skills: set,
        experience_level: str
    ) -> List[Dict]:
        goal_lower = goal.lower()
        relevant = []
        
        for course in self.courses_db:
            course_category = course.get("category", "").lower()
            course_skills = [s.lower() for s in course.get("skills", [])]
            
            if (goal_lower in course_category or
                any(goal_word in course_category for goal_word in goal_lower.split()) or
                any(goal_word in " ".join(course_skills) for goal_word in goal_lower.split())):
                relevant.append(course)
        
        return relevant
    
    def _order_by_prerequisites(self, courses: List[Dict], user_skills: set) -> List[Dict]:
        ordered = []
        acquired_skills = user_skills.copy()
        remaining_courses = courses.copy()
        
        while remaining_courses:
            added = False
            for course in remaining_courses[:]:
                prerequisites = set(course.get("prerequisites", []))
                
                if prerequisites.issubset(acquired_skills):
                    ordered.append(course)
                    acquired_skills.update(course.get("skills", []))
                    remaining_courses.remove(course)
                    added = True
            
            if not added and remaining_courses:
                ordered.extend(remaining_courses)
                break
        
        return ordered
    
    def _create_milestones(self, courses: List[Dict], timeframe: str) -> List[Dict]:
        milestones = []
        total_weeks = self._parse_timeframe(timeframe)
        
        if not courses:
            return milestones
        
        weeks_per_course = total_weeks / len(courses)
        current_date = datetime.now()
        
        for i, course in enumerate(courses):
            milestone_date = current_date + timedelta(weeks=weeks_per_course * (i + 1))
            milestones.append({
                "milestone_number": i + 1,
                "course_id": course.get("id"),
                "course_title": course.get("title"),
                "target_date": milestone_date.strftime("%Y-%m-%d"),
                "skills_to_acquire": course.get("skills", [])
            })
        
        return milestones
    
    def _parse_duration(self, duration: str) -> int:
        if "week" in duration:
            return int(duration.split()[0]) * 10
        return 40
    
    def _parse_timeframe(self, timeframe: str) -> int:
        if "month" in timeframe.lower():
            months = int(timeframe.split()[0])
            return months * 4
        elif "week" in timeframe.lower():
            return int(timeframe.split()[0])
        return 12
    
    def _generate_path_explanation(self, goal: str, courses: List[Dict]) -> str:
        if not courses:
            return f"No courses found matching '{goal}'. Try refining your goal or interests."
        
        explanation = f"This learning path is designed to help you achieve: {goal}.\n\n"
        explanation += f"The path includes {len(courses)} courses that build progressively:\n"
        
        for i, course in enumerate(courses, 1):
            explanation += f"{i}. {course.get('title')} - {course.get('difficulty')} level\n"
        
        explanation += "\nEach course is sequenced to build upon previous knowledge and skills."
        
        return explanation
