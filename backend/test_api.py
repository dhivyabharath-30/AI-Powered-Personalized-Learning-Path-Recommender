"""
Test script to verify all API functions work correctly
Run from backend directory: python test_api.py
"""
import sys
import asyncio
sys.path.insert(0, '.')

from services.profile_engine import ProfileEngine
from services.recommendation_engine import RecommendationEngine
from services.path_generator import LearningPathGenerator
from services.ai_assistant import AIAssistant
from services.shared_state import shared_state


async def test_all_functions():
    print("=" * 60)
    print("Testing AI Learning Path Recommender Functions")
    print("=" * 60)
    
    # Initialize services
    profile_engine = ProfileEngine()
    recommendation_engine = RecommendationEngine()
    path_generator = LearningPathGenerator()
    ai_assistant = AIAssistant()
    
    # Test 1: Create Profile
    print("\n1. Testing Profile Creation...")
    try:
        profile = profile_engine.create_or_update_profile(
            user_id="test_user_001",
            interests=["Python", "Machine Learning", "Data Science"],
            experience_level="Intermediate",
            goals=["Become a data scientist", "Build ML models"],
            completed_courses=["Python Basics"]
        )
        print("✓ Profile created successfully")
        print(f"  User ID: {profile['user_id']}")
        print(f"  Interests: {profile['interests']}")
        print(f"  Skills extracted: {profile['skills']}")
    except Exception as e:
        print(f"✗ Profile creation failed: {e}")
        return
    
    # Test 2: Get Profile
    print("\n2. Testing Profile Retrieval...")
    try:
        retrieved_profile = profile_engine.get_profile("test_user_001")
        if retrieved_profile:
            print("✓ Profile retrieved successfully")
        else:
            print("✗ Profile not found")
    except Exception as e:
        print(f"✗ Profile retrieval failed: {e}")
    
    # Test 3: Get Recommendations
    print("\n3. Testing Recommendation Engine...")
    try:
        recommendations = await recommendation_engine.get_recommendations(
            "test_user_001", limit=5
        )
        print(f"✓ Generated {len(recommendations['recommendations'])} recommendations")
        for i, rec in enumerate(recommendations['recommendations'][:3], 1):
            print(f"  {i}. {rec['title']} (Score: {rec['relevance_score']:.2f})")
            print(f"     Reason: {rec['reasoning']}")
    except Exception as e:
        print(f"✗ Recommendation generation failed: {e}")
    
    # Test 4: Generate Learning Path
    print("\n4. Testing Learning Path Generation...")
    try:
        learning_path = await path_generator.generate_path(
            user_id="test_user_001",
            goal="become a data scientist",
            timeframe="6 months"
        )
        print(f"✓ Learning path generated successfully")
        print(f"  Goal: {learning_path['goal']}")
        print(f"  Total courses: {learning_path['total_courses']}")
        print(f"  Courses in path:")
        for i, course in enumerate(learning_path['path'], 1):
            print(f"    {i}. {course['title']} ({course['duration']})")
    except Exception as e:
        print(f"✗ Learning path generation failed: {e}")
    
    # Test 5: Get Progress
    print("\n5. Testing Progress Tracking...")
    try:
        progress = profile_engine.get_learning_progress("test_user_001")
        print(f"✓ Progress retrieved successfully")
        print(f"  Completed courses: {progress['completed_courses']}")
        print(f"  Skills acquired: {progress['skills_acquired']}")
        print(f"  Progress: {progress['progress_percentage']}%")
    except Exception as e:
        print(f"✗ Progress tracking failed: {e}")
    
    # Test 6: AI Assistant Chat
    print("\n6. Testing AI Assistant...")
    try:
        # Test greeting
        response1 = await ai_assistant.process_message(
            "Hello!",
            "test_user_001",
            []
        )
        print(f"✓ AI Assistant responding")
        print(f"  Query: 'Hello!'")
        print(f"  Response: {response1['response'][:100]}...")
        print(f"  Action: {response1['action']}")
        
        # Test recommendation request
        response2 = await ai_assistant.process_message(
            "Can you recommend some courses?",
            "test_user_001",
            []
        )
        print(f"\n  Query: 'Can you recommend some courses?'")
        print(f"  Action: {response2['action']}")
        
    except Exception as e:
        print(f"✗ AI Assistant failed: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_all_functions())
