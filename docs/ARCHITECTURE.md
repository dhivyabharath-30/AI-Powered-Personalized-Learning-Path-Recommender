# Architecture Documentation

## System Overview

The AI-Powered Personalized Learning Path Recommender is built with a modern microservices architecture consisting of:

1. **Backend API** (Python FastAPI)
2. **Frontend Web App** (React + TypeScript)
3. **AI Services** (OpenAI GPT-4 integration)
4. **Data Layer** (PostgreSQL)

## Component Architecture

### Backend Services

#### 1. Profile Engine (`profile_engine.py`)
- Manages learner profiles
- Tracks completed courses and skills
- Calculates learning progress
- Extracts skills from course history

#### 2. Recommendation Engine (`recommendation_engine.py`)
- Implements content-based filtering
- Calculates relevance scores based on:
  - Interest matching
  - Skill alignment
  - Difficulty level
  - Course ratings
- Provides explainable recommendations

#### 3. Learning Path Generator (`path_generator.py`)
- Creates structured learning roadmaps
- Orders courses by prerequisites
- Generates milestones with target dates
- Estimates total learning time

#### 4. AI Assistant (`ai_assistant.py`)
- Natural language processing for user queries
- Intent detection and classification
- Conversational responses
- Context-aware interactions

### Frontend Components

#### 1. Dashboard
- Visual progress tracking
- Quick stats overview
- Course recommendations display
- Interactive charts (Recharts)

#### 2. Chat Interface
- Real-time messaging with AI assistant
- Conversation history
- Quick action buttons
- Typing indicators

#### 3. Learning Path Visualizer
- Timeline-based path display
- Milestone tracking
- Goal input and generation
- Skills breakdown

#### 4. Profile Setup
- Multi-step onboarding
- Interest selection
- Experience level assessment
- Goal definition

## Data Flow

```
User Input → Frontend → API Gateway → Service Layer → AI/ML Processing → Database
                ↓                                           ↓
           Response ← JSON ← Business Logic ← Recommendations ← Data
```

## API Endpoints

### Profile Management
- `POST /api/profile` - Create/update learner profile
- `GET /api/profile/{user_id}` - Retrieve profile
- `GET /api/progress/{user_id}` - Get learning progress

### Recommendations
- `GET /api/recommendations/{user_id}` - Get personalized course recommendations

### Learning Paths
- `POST /api/learning-path` - Generate personalized learning path

### Chat
- `POST /api/chat` - Conversational AI interaction

## Recommendation Algorithm

### Scoring Formula

```
relevance_score = interest_match × 3.0
                + skill_overlap × 1.5
                + difficulty_alignment × 2.0
                + rating_boost × 0.5
```

### Factors

1. **Interest Match**: Direct correlation between user interests and course category
2. **Skill Overlap**: Existing skills that align with course prerequisites
3. **Difficulty Alignment**: Matching course difficulty to user experience level
4. **Rating Boost**: Quality indicator based on course ratings

## Path Generation Algorithm

### Steps

1. **Course Selection**: Filter courses relevant to learning goal
2. **Prerequisite Analysis**: Build dependency graph
3. **Topological Sort**: Order courses by prerequisites
4. **Milestone Creation**: Divide timeline into achievable segments
5. **Skill Mapping**: Track skill acquisition at each milestone

## Security Considerations

- Input validation on all API endpoints
- Environment variable management for secrets
- CORS configuration for cross-origin requests
- User data isolation by user_id

## Scalability

### Current Implementation
- In-memory storage for profiles and courses
- Single-instance deployment

### Production Recommendations
- PostgreSQL database integration
- Redis caching layer
- Load balancing for API servers
- CDN for frontend assets
- Message queue for async processing

## Technology Stack

### Backend
- **FastAPI**: High-performance async API framework
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: ORM for database operations
- **OpenAI API**: LLM integration for AI assistant

### Frontend
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client for API calls
- **Recharts**: Data visualization library

### DevOps
- **Uvicorn**: ASGI server
- **Docker**: Containerization (future)
- **GitHub Actions**: CI/CD (future)

## Future Enhancements

1. **Adaptive Learning**: Adjust paths based on learner performance
2. **Collaborative Filtering**: User similarity-based recommendations
3. **Content Integration**: Direct course content embedding
4. **Mobile App**: React Native implementation
5. **Social Features**: Peer learning and discussion forums
6. **Analytics Dashboard**: Admin insights and metrics
7. **A/B Testing**: Recommendation algorithm optimization
