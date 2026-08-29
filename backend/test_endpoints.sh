#!/bin/bash
# Test script for API endpoints
# Make sure the server is running: uvicorn main:app --reload

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Testing API Endpoints"
echo "=========================================="

# Test 1: Health Check
echo -e "\n1. Testing Health Check..."
curl -s "$BASE_URL/" | python -m json.tool

# Test 2: Create Profile
echo -e "\n\n2. Testing Create Profile..."
curl -s -X POST "$BASE_URL/api/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_api",
    "interests": ["Python", "Machine Learning"],
    "experience_level": "Beginner",
    "goals": ["Learn data science"],
    "completed_courses": []
  }' | python -m json.tool

# Test 3: Get Profile
echo -e "\n\n3. Testing Get Profile..."
curl -s "$BASE_URL/api/profile/test_user_api" | python -m json.tool

# Test 4: Get Recommendations
echo -e "\n\n4. Testing Get Recommendations..."
curl -s "$BASE_URL/api/recommendations/test_user_api?limit=3" | python -m json.tool

# Test 5: Generate Learning Path
echo -e "\n\n5. Testing Generate Learning Path..."
curl -s -X POST "$BASE_URL/api/learning-path" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_api",
    "goal": "become a machine learning engineer",
    "timeframe": "6 months"
  }' | python -m json.tool

# Test 6: Get Progress
echo -e "\n\n6. Testing Get Progress..."
curl -s "$BASE_URL/api/progress/test_user_api" | python -m json.tool

# Test 7: Chat with AI
echo -e "\n\n7. Testing Chat Interface..."
curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you help me?",
    "user_id": "test_user_api",
    "conversation_history": []
  }' | python -m json.tool

echo -e "\n\n=========================================="
echo "All Tests Complete!"
echo "=========================================="
