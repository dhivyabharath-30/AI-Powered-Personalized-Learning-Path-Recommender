from typing import List, Dict
import os


class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_context = {}
        self.use_openai = self.api_key is not None and len(self.api_key) > 10
        
        if self.use_openai:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.api_key)
                print("✓ OpenAI integration enabled")
            except Exception as e:
                print(f"⚠ OpenAI import failed: {e}. Using rule-based NLP.")
                self.use_openai = False
        else:
            self.use_openai = False
            print("⚠ OpenAI API key not found. Using rule-based NLP.")
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        conversation_history: List[Dict]
    ) -> Dict:
        from services.shared_state import shared_state
        from services.recommendation_engine import RecommendationEngine
        from services.path_generator import LearningPathGenerator
        
        recommendation_engine = RecommendationEngine()
        path_generator = LearningPathGenerator()
        
        # Use OpenAI for better intent detection if available
        if self.use_openai:
            try:
                intent = await self._detect_intent_openai(message, user_id)
                if intent:
                    return intent
            except Exception as e:
                print(f"OpenAI error: {e}, falling back to rule-based")
        
        # Fallback to rule-based intent detection
        message_lower = message.lower()
        
        # Intent detection
        if any(word in message_lower for word in ["recommend", "suggest", "course"]):
            profile = shared_state.get_profile(user_id)
            if not profile:
                return {
                    "response": "I'd love to help! First, tell me about your interests and goals. What would you like to learn?",
                    "action": "request_profile",
                    "data": None
                }
            
            recommendations = await recommendation_engine.get_recommendations(user_id, 5)
            return {
                "response": self._format_recommendations_response(recommendations),
                "action": "show_recommendations",
                "data": recommendations
            }
        
        elif any(word in message_lower for word in ["path", "roadmap", "plan"]):
            goal = self._extract_goal(message)
            if goal:
                path = await path_generator.generate_path(user_id, goal)
                return {
                    "response": self._format_path_response(path),
                    "action": "show_learning_path",
                    "data": path
                }
            else:
                return {
                    "response": "What's your learning goal? For example: 'become a data scientist' or 'learn web development'",
                    "action": "request_goal",
                    "data": None
                }
        
        elif any(word in message_lower for word in ["progress", "status"]):
            from services.profile_engine import ProfileEngine
            profile_engine = ProfileEngine()
            progress = profile_engine.get_learning_progress(user_id)
            return {
                "response": self._format_progress_response(progress),
                "action": "show_progress",
                "data": progress
            }
        
        elif any(word in message_lower for word in ["interest", "goal", "learn"]):
            interests = self._extract_interests(message)
            return {
                "response": f"Great! I understand you're interested in: {', '.join(interests)}. What's your experience level: Beginner, Intermediate, or Advanced?",
                "action": "extract_profile",
                "data": {"interests": interests}
            }
        
        else:
            return {
                "response": self._generate_conversational_response(message, user_id),
                "action": "chat",
                "data": None
            }
    
    def _extract_goal(self, message: str) -> str:
        message_lower = message.lower()
        
        goal_indicators = ["become", "learn", "master", "study", "path to", "roadmap for"]
        for indicator in goal_indicators:
            if indicator in message_lower:
                goal = message_lower.split(indicator)[-1].strip()
                return goal.replace("?", "").replace(".", "")
        
        return ""
    
    def _extract_interests(self, message: str) -> List[str]:
        tech_keywords = [
            "python", "javascript", "react", "machine learning", "data science",
            "web development", "ai", "backend", "frontend", "devops", "cloud",
            "database", "mobile", "ios", "android", "java", "c++", "rust"
        ]
        
        message_lower = message.lower()
        interests = [keyword for keyword in tech_keywords if keyword in message_lower]
        
        return interests if interests else ["programming"]
    
    def _format_recommendations_response(self, recommendations: Dict) -> str:
        if not recommendations.get("recommendations"):
            return "I don't have enough information about your profile yet. Tell me about your interests and goals!"
        
        response = "Here are my top course recommendations for you:\n\n"
        for i, course in enumerate(recommendations["recommendations"][:5], 1):
            response += f"{i}. **{course['title']}** ({course['difficulty']})\n"
            response += f"   Duration: {course['duration']} | Rating: {course['rating']}/5.0\n"
            response += f"   Why: {course['reasoning']}\n\n"
        
        return response
    
    def _format_path_response(self, path: Dict) -> str:
        if "error" in path:
            return path["error"]
        
        response = f"I've created a personalized learning path for: **{path['goal']}**\n\n"
        response += f"Timeline: {path['timeframe']} | Total courses: {path['total_courses']}\n\n"
        response += "Your Learning Journey:\n\n"
        
        for i, course in enumerate(path.get("path", []), 1):
            response += f"{i}. {course['title']} - {course['duration']}\n"
        
        response += f"\n{path.get('explanation', '')}"
        
        return response
    
    def _format_progress_response(self, progress: Dict) -> str:
        if not progress:
            return "No progress data available yet. Start learning to track your journey!"
        
        response = "Your Learning Progress:\n\n"
        response += f"📚 Completed Courses: {progress.get('completed_courses', 0)}\n"
        response += f"🎯 Skills Acquired: {progress.get('skills_acquired', 0)}\n"
        response += f"🎓 Active Goals: {progress.get('active_goals', 0)}\n"
        response += f"📊 Overall Progress: {progress.get('progress_percentage', 0)}%\n"
        
        return response
    
    def _generate_conversational_response(self, message: str, user_id: str) -> str:
        greetings = ["hi", "hello", "hey", "greetings"]
        if any(greeting in message.lower() for greeting in greetings):
            return "Hello! I'm your AI learning assistant. I can help you discover personalized learning paths, recommend courses, and track your progress. What would you like to learn today?"
        
        return "I'm here to help you with your learning journey! You can ask me to:\n- Recommend courses\n- Create a learning path\n- Check your progress\n- Answer questions about learning resources"
    
    async def _detect_intent_openai(self, message: str, user_id: str) -> Dict:
        """Use OpenAI GPT for advanced intent detection"""
        from services.shared_state import shared_state
        from services.recommendation_engine import RecommendationEngine
        from services.path_generator import LearningPathGenerator
        
        profile = shared_state.get_profile(user_id)
        
        # Create context-aware prompt
        system_prompt = """You are an AI learning assistant. Analyze the user's message and determine their intent.
        
Available intents:
- recommend: User wants course recommendations
- learning_path: User wants to create a learning path/roadmap
- progress: User wants to see their progress
- profile_info: User is providing interests or goals
- general: General questions or greetings

Respond with JSON: {"intent": "intent_name", "extracted_info": "any relevant info"}"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            import json
            intent_data = json.loads(result)
            intent = intent_data.get("intent", "general")
            
            # Route based on detected intent
            recommendation_engine = RecommendationEngine()
            path_generator = LearningPathGenerator()
            
            if intent == "recommend":
                if not profile:
                    return {
                        "response": "I'd love to help! First, tell me about your interests and goals.",
                        "action": "request_profile",
                        "data": None
                    }
                recommendations = await recommendation_engine.get_recommendations(user_id, 5)
                return {
                    "response": self._format_recommendations_response(recommendations),
                    "action": "show_recommendations",
                    "data": recommendations
                }
            
            elif intent == "learning_path":
                extracted = intent_data.get("extracted_info", "")
                if extracted and profile:
                    path = await path_generator.generate_path(user_id, extracted)
                    return {
                        "response": self._format_path_response(path),
                        "action": "show_learning_path",
                        "data": path
                    }
                else:
                    return {
                        "response": "What's your learning goal? For example: 'become a data scientist'",
                        "action": "request_goal",
                        "data": None
                    }
            
            elif intent == "progress":
                from services.profile_engine import ProfileEngine
                profile_engine = ProfileEngine()
                progress = profile_engine.get_learning_progress(user_id)
                return {
                    "response": self._format_progress_response(progress),
                    "action": "show_progress",
                    "data": progress
                }
            
            # For other intents, use GPT to generate response
            return {
                "response": result,
                "action": "chat",
                "data": {"openai_powered": True}
            }
            
        except Exception as e:
            print(f"OpenAI processing error: {e}")
            return None  # Fallback to rule-based
