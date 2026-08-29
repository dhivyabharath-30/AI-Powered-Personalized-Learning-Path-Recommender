from typing import List, Dict
from services.ml_engine import get_ml_engine


class RecommendationEngine:
    def __init__(self):
        self.courses_db = self._load_courses()
        self.user_profiles = {}
    
    def _load_courses(self) -> List[Dict]:
        return [
            {
                "id": "py101",
                "title": "Python for Beginners",
                "category": "Programming",
                "difficulty": "Beginner",
                "duration": "4 weeks",
                "skills": ["Python", "Programming Basics"],
                "prerequisites": [],
                "rating": 4.7
            },
            {
                "id": "ml201",
                "title": "Machine Learning Fundamentals",
                "category": "AI/ML",
                "difficulty": "Intermediate",
                "duration": "8 weeks",
                "skills": ["Machine Learning", "Python", "Statistics"],
                "prerequisites": ["Python", "Math"],
                "rating": 4.8
            },
            {
                "id": "web301",
                "title": "Full Stack Web Development",
                "category": "Web Development",
                "difficulty": "Intermediate",
                "duration": "12 weeks",
                "skills": ["React", "Node.js", "JavaScript", "Database"],
                "prerequisites": ["JavaScript", "HTML", "CSS"],
                "rating": 4.6
            },
            {
                "id": "ds101",
                "title": "Data Science with Python",
                "category": "Data Science",
                "difficulty": "Beginner",
                "duration": "6 weeks",
                "skills": ["Python", "Data Analysis", "Pandas", "NumPy"],
                "prerequisites": ["Python"],
                "rating": 4.5
            },
            {
                "id": "react201",
                "title": "Advanced React Patterns",
                "category": "Frontend",
                "difficulty": "Advanced",
                "duration": "6 weeks",
                "skills": ["React", "State Management", "Performance"],
                "prerequisites": ["React", "JavaScript"],
                "rating": 4.9
            }
        ]
    
    async def get_recommendations(self, user_id: str, limit: int = 10, use_ml: bool = True) -> Dict:
        from services.shared_state import shared_state
        profile = shared_state.get_profile(user_id)
        
        if not profile:
            return {"recommendations": [], "reasoning": "Profile not found"}
        
        user_interests = set(profile.get("interests", []))
        user_skills = set(profile.get("skills", []))
        experience_level = profile.get("experience_level", "Beginner")
        
        scored_courses = []
        
        for idx, course in enumerate(self.courses_db):
            # Traditional rule-based score
            rule_score = self._calculate_relevance_score(
                course, user_interests, user_skills, experience_level
            )
            
            if use_ml:
                # ML-based hybrid score
                ml_score, ml_explanation = get_ml_engine().hybrid_recommendation_score(
                    user_id, profile, idx
                )
                
                # Combine rule-based and ML scores (70% ML, 30% rules)
                final_score = (0.7 * ml_score * 10) + (0.3 * rule_score)
                
                # Enhanced explanation with ML insights
                reasoning = self._explain_recommendation_ml(
                    course, profile, ml_explanation
                )
            else:
                final_score = rule_score
                reasoning = self._explain_recommendation(course, profile)
            
            if final_score > 0:
                scored_courses.append({
                    "course": course,
                    "score": final_score,
                    "reasoning": reasoning,
                    "ml_enabled": use_ml
                })
        
        scored_courses.sort(key=lambda x: x["score"], reverse=True)
        top_recommendations = scored_courses[:limit]
        
        # Get user preference predictions
        preferences = get_ml_engine().predict_user_preferences(profile) if use_ml else {}
        
        return {
            "recommendations": [
                {
                    **rec["course"],
                    "relevance_score": round(rec["score"], 2),
                    "reasoning": rec["reasoning"],
                    "ml_powered": rec["ml_enabled"]
                }
                for rec in top_recommendations
            ],
            "total_found": len(scored_courses),
            "ml_enabled": use_ml,
            "predicted_preferences": preferences if use_ml else None
        }
    
    def _calculate_relevance_score(
        self,
        course: Dict,
        user_interests: set,
        user_skills: set,
        experience_level: str
    ) -> float:
        score = 0.0
        
        # Interest match
        course_category = course.get("category", "").lower()
        for interest in user_interests:
            if interest.lower() in course_category:
                score += 3.0
        
        # Skill match
        course_skills = set(course.get("skills", []))
        skill_overlap = len(user_skills.intersection(course_skills))
        score += skill_overlap * 1.5
        
        # Difficulty alignment
        difficulty_match = {
            "Beginner": {"Beginner": 2.0, "Intermediate": 1.0, "Advanced": 0.3},
            "Intermediate": {"Beginner": 0.5, "Intermediate": 2.0, "Advanced": 1.5},
            "Advanced": {"Beginner": 0.2, "Intermediate": 1.0, "Advanced": 2.0}
        }
        score += difficulty_match.get(experience_level, {}).get(course.get("difficulty"), 0)
        
        # Rating boost
        score += course.get("rating", 0) * 0.5
        
        return score
    
    def _explain_recommendation(self, course: Dict, profile: Dict) -> str:
        reasons = []
        
        user_interests = profile.get("interests", [])
        course_category = course.get("category", "")
        
        for interest in user_interests:
            if interest.lower() in course_category.lower():
                reasons.append(f"Matches your interest in {interest}")
        
        user_skills = set(profile.get("skills", []))
        course_skills = set(course.get("skills", []))
        skill_overlap = user_skills.intersection(course_skills)
        
        if skill_overlap:
            reasons.append(f"Builds on your existing skills: {', '.join(list(skill_overlap)[:2])}")
        
        if course.get("difficulty") == profile.get("experience_level"):
            reasons.append(f"Appropriate for your {profile.get('experience_level')} level")
        
        if not reasons:
            reasons.append("High-quality course based on ratings and content")
        
        return "; ".join(reasons[:3])
    
    def _explain_recommendation_ml(
        self, 
        course: Dict, 
        profile: Dict,
        ml_explanation: Dict
    ) -> str:
        """Enhanced explanation combining rules and ML"""
        reasons = []
        
        # Add ML confidence
        ml_conf = ml_explanation.get("hybrid", 0) * 100
        reasons.append(f"ML Confidence: {ml_conf:.0f}%")
        
        # Traditional reasons
        user_interests = profile.get("interests", [])
        course_category = course.get("category", "")
        
        for interest in user_interests:
            if interest.lower() in course_category.lower():
                reasons.append(f"Matches {interest}")
                break
        
        # Add ML method
        content_score = ml_explanation.get("content_based", 0) * 100
        collab_score = ml_explanation.get("collaborative", 0) * 100
        
        reasons.append(
            f"Content similarity: {content_score:.0f}%, "
            f"Collaborative: {collab_score:.0f}%"
        )
        
        return "; ".join(reasons[:3])
