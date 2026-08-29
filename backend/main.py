from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv

from services.profile_engine import ProfileEngine
from services.recommendation_engine import RecommendationEngine
from services.path_generator import LearningPathGenerator
from services.ai_assistant import AIAssistant

load_dotenv()

app = FastAPI(title="AI Learning Path Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

profile_engine = ProfileEngine()
recommendation_engine = RecommendationEngine()
path_generator = LearningPathGenerator()
ai_assistant = AIAssistant()


class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_history: Optional[List[Dict]] = []


class ProfileRequest(BaseModel):
    user_id: str
    interests: List[str]
    experience_level: str
    goals: List[str]
    completed_courses: Optional[List[str]] = []


class LearningPathRequest(BaseModel):
    user_id: str
    goal: str
    timeframe: Optional[str] = "3 months"


@app.get("/")
def root():
    return {"message": "AI Learning Path Recommender API"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = await ai_assistant.process_message(
            request.message,
            request.user_id,
            request.conversation_history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile")
async def create_profile(request: ProfileRequest):
    try:
        profile = profile_engine.create_or_update_profile(
            user_id=request.user_id,
            interests=request.interests,
            experience_level=request.experience_level,
            goals=request.goals,
            completed_courses=request.completed_courses
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profile/{user_id}")
async def get_profile(user_id: str):
    profile = profile_engine.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.get("/api/recommendations/{user_id}")
async def get_recommendations(user_id: str, limit: int = 10):
    try:
        recommendations = await recommendation_engine.get_recommendations(
            user_id, limit
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/learning-path")
async def generate_learning_path(request: LearningPathRequest):
    try:
        learning_path = await path_generator.generate_path(
            user_id=request.user_id,
            goal=request.goal,
            timeframe=request.timeframe
        )
        return learning_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/progress/{user_id}")
async def get_progress(user_id: str):
    try:
        progress = profile_engine.get_learning_progress(user_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ml/info")
async def get_ml_info():
    """Get information about ML models and capabilities"""
    try:
        from services.ml_engine import ml_engine
        metadata = ml_engine.get_model_metadata()
        return {
            "ml_enabled": True,
            "models": metadata,
            "capabilities": [
                "TF-IDF Course Embeddings",
                "User Profile Embeddings",
                "Collaborative Filtering (NMF)",
                "Content-Based Filtering",
                "Hybrid Recommendations",
                "Preference Prediction",
                "OpenAI NLP Integration (if configured)"
            ],
            "openai_enabled": ai_assistant.use_openai
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations/{user_id}/similar")
async def get_similar_courses(user_id: str, course_id: str):
    """Get similar courses using ML embeddings"""
    try:
        from services.ml_engine import ml_engine
        
        # Find course index
        course_idx = None
        for idx, course in enumerate(recommendation_engine.courses_db):
            if course["id"] == course_id:
                course_idx = idx
                break
        
        if course_idx is None:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Get similar courses
        similar_indices = ml_engine.find_similar_courses(course_idx, top_k=3)
        similar_courses = [
            recommendation_engine.courses_db[idx] 
            for idx in similar_indices
        ]
        
        return {
            "course_id": course_id,
            "similar_courses": similar_courses,
            "method": "ML Embeddings (Cosine Similarity)"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
