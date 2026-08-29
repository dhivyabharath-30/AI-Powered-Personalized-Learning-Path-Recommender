# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check

**GET** `/`

Returns API status.

**Response:**
```json
{
  "message": "AI Learning Path Recommender API"
}
```

---

### 2. Create/Update Profile

**POST** `/api/profile`

Create or update a learner profile.

**Request Body:**
```json
{
  "user_id": "user_123",
  "interests": ["Python", "Machine Learning", "Data Science"],
  "experience_level": "Intermediate",
  "goals": ["Become a data scientist", "Build ML models"],
  "completed_courses": ["Python Basics", "Statistics 101"]
}
```

**Response:**
```json
{
  "user_id": "user_123",
  "interests": ["Python", "Machine Learning", "Data Science"],
  "experience_level": "Intermediate",
  "goals": ["Become a data scientist", "Build ML models"],
  "completed_courses": ["Python Basics", "Statistics 101"],
  "skills": ["Python", "Programming", "Statistics"],
  "created_at": "2026-08-28T10:30:00",
  "updated_at": "2026-08-28T10:30:00"
}
```

---

### 3. Get Profile

**GET** `/api/profile/{user_id}`

Retrieve a learner's profile.

**Response:**
```json
{
  "user_id": "user_123",
  "interests": ["Python", "Machine Learning"],
  "experience_level": "Intermediate",
  "goals": ["Become a data scientist"],
  "completed_courses": ["Python Basics"],
  "skills": ["Python", "Programming"],
  "created_at": "2026-08-28T10:30:00",
  "updated_at": "2026-08-28T10:30:00"
}
```

---

### 4. Get Recommendations

**GET** `/api/recommendations/{user_id}`

Get personalized course recommendations.

**Query Parameters:**
- `limit` (optional): Maximum number of recommendations (default: 10)

**Response:**
```json
{
  "recommendations": [
    {
      "id": "ml201",
      "title": "Machine Learning Fundamentals",
      "category": "AI/ML",
      "difficulty": "Intermediate",
      "duration": "8 weeks",
      "skills": ["Machine Learning", "Python", "Statistics"],
      "prerequisites": ["Python", "Math"],
      "rating": 4.8,
      "relevance_score": 8.5,
      "reasoning": "Matches your interest in Machine Learning; Builds on your existing skills: Python"
    }
  ],
  "total_found": 5
}
```

---

### 5. Generate Learning Path

**POST** `/api/learning-path`

Generate a personalized learning path.

**Request Body:**
```json
{
  "user_id": "user_123",
  "goal": "become a data scientist",
  "timeframe": "6 months"
}
```

**Response:**
```json
{
  "user_id": "user_123",
  "goal": "become a data scientist",
  "timeframe": "6 months",
  "total_courses": 3,
  "estimated_hours": 180,
  "path": [
    {
      "id": "py101",
      "title": "Python for Beginners",
      "difficulty": "Beginner",
      "duration": "4 weeks",
      "skills": ["Python", "Programming Basics"]
    },
    {
      "id": "ds101",
      "title": "Data Science with Python",
      "difficulty": "Beginner",
      "duration": "6 weeks",
      "skills": ["Python", "Data Analysis", "Pandas"]
    }
  ],
  "milestones": [
    {
      "milestone_number": 1,
      "course_id": "py101",
      "course_title": "Python for Beginners",
      "target_date": "2026-10-15",
      "skills_to_acquire": ["Python", "Programming Basics"]
    }
  ],
  "explanation": "This learning path is designed to help you achieve: become a data scientist..."
}
```

---

### 6. Get Learning Progress

**GET** `/api/progress/{user_id}`

Track a learner's progress.

**Response:**
```json
{
  "user_id": "user_123",
  "completed_courses": 5,
  "skills_acquired": 8,
  "active_goals": 2,
  "progress_percentage": 45
}
```

---

### 7. Chat with AI Assistant

**POST** `/api/chat`

Interact with the AI learning assistant.

**Request Body:**
```json
{
  "message": "Recommend courses for web development",
  "user_id": "user_123",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hi"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help?"
    }
  ]
}
```

**Response:**
```json
{
  "response": "Here are my top course recommendations for web development...",
  "action": "show_recommendations",
  "data": {
    "recommendations": [...]
  }
}
```

**Actions:**
- `request_profile`: Need profile information
- `show_recommendations`: Display course recommendations
- `show_learning_path`: Display learning path
- `show_progress`: Display progress metrics
- `extract_profile`: Extracting profile information
- `chat`: General conversation

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "detail": "Invalid input data"
}
```

**404 Not Found**
```json
{
  "detail": "Profile not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider:
- Rate limiting per user/IP
- API key authentication
- Usage quotas

---

## CORS

CORS is configured to allow all origins in development. For production:
```python
allow_origins=["https://yourdomain.com"]
```
