"""
Machine Learning Engine for Advanced Recommendations
Implements collaborative filtering, embeddings, and model training
"""
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
import json
import os


class MLEngine:
    def __init__(self):
        self.course_embeddings = None
        self.user_embeddings = None
        self.tfidf_vectorizer = None
        self.nmf_model = None
        self.course_feature_matrix = None
        self.trained = False
        
        # Load or initialize
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models and create course embeddings"""
        # Create TF-IDF based course embeddings
        self._create_course_embeddings()
        
        # Initialize NMF for matrix factorization
        self.nmf_model = NMF(n_components=10, init='random', random_state=42)
    
    def _create_course_embeddings(self):
        """Create TF-IDF embeddings for courses"""
        from services.recommendation_engine import RecommendationEngine
        rec_engine = RecommendationEngine()
        courses = rec_engine.courses_db
        
        # Create text representations of courses
        course_texts = []
        for course in courses:
            text = f"{course['title']} {course['category']} {' '.join(course['skills'])} {course['difficulty']}"
            course_texts.append(text)
        
        # Create TF-IDF vectors
        self.tfidf_vectorizer = TfidfVectorizer(max_features=50)
        self.course_feature_matrix = self.tfidf_vectorizer.fit_transform(course_texts)
        self.course_embeddings = self.course_feature_matrix.toarray()
        
        print(f"✓ Created course embeddings: {self.course_embeddings.shape}")
    
    def create_user_embedding(self, profile: Dict) -> np.ndarray:
        """Create embedding vector for user based on profile"""
        # Combine user interests, goals, and skills into text
        user_text = " ".join(
            profile.get("interests", []) + 
            profile.get("goals", []) + 
            profile.get("skills", [])
        )
        
        # Transform to TF-IDF space
        user_vector = self.tfidf_vectorizer.transform([user_text])
        return user_vector.toarray()[0]
    
    def collaborative_filtering_score(
        self, 
        user_id: str, 
        course_idx: int,
        interaction_matrix: np.ndarray = None
    ) -> float:
        """
        Collaborative filtering using matrix factorization (NMF)
        Simulates user-item interactions for demonstration
        """
        if interaction_matrix is None:
            # Create synthetic interaction matrix for demonstration
            # In production, this would come from real user interactions
            interaction_matrix = self._create_synthetic_interactions()
        
        # Train NMF if not trained
        if not self.trained:
            self.nmf_model.fit(interaction_matrix)
            self.trained = True
        
        # Get latent factors
        W = self.nmf_model.transform(interaction_matrix)  # User factors
        H = self.nmf_model.components_  # Item factors
        
        # Reconstruct ratings
        predicted_ratings = np.dot(W, H)
        
        # Return predicted score for this user-course pair
        # For demo, use a hash of user_id to get consistent user index
        user_idx = hash(user_id) % predicted_ratings.shape[0]
        
        return float(predicted_ratings[user_idx, course_idx])
    
    def _create_synthetic_interactions(self) -> np.ndarray:
        """
        Create synthetic user-course interaction matrix
        In production, replace with real interaction data
        """
        # Simulate 50 users x 5 courses interaction matrix
        np.random.seed(42)
        return np.random.rand(50, 5) * 5  # Ratings 0-5
    
    def content_based_similarity(
        self, 
        user_embedding: np.ndarray, 
        course_idx: int
    ) -> float:
        """Calculate content-based similarity using embeddings"""
        course_embedding = self.course_embeddings[course_idx]
        
        # Cosine similarity
        similarity = cosine_similarity(
            user_embedding.reshape(1, -1),
            course_embedding.reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    def hybrid_recommendation_score(
        self,
        user_id: str,
        profile: Dict,
        course_idx: int,
        alpha: float = 0.6
    ) -> Tuple[float, Dict]:
        """
        Hybrid recommendation combining collaborative and content-based filtering
        
        Args:
            alpha: Weight for collaborative filtering (1-alpha for content-based)
        
        Returns:
            (score, explanation_dict)
        """
        # Content-based score using embeddings
        user_embedding = self.create_user_embedding(profile)
        content_score = self.content_based_similarity(user_embedding, course_idx)
        
        # Collaborative filtering score
        collab_score = self.collaborative_filtering_score(user_id, course_idx)
        
        # Normalize collaborative score to 0-1 range
        collab_score_normalized = collab_score / 5.0  # Assuming 0-5 rating scale
        
        # Hybrid score
        hybrid_score = (alpha * collab_score_normalized + 
                       (1 - alpha) * content_score)
        
        explanation = {
            "content_based": round(content_score, 3),
            "collaborative": round(collab_score_normalized, 3),
            "hybrid": round(hybrid_score, 3),
            "method": "Hybrid ML (Content + Collaborative Filtering)"
        }
        
        return hybrid_score, explanation
    
    def find_similar_courses(self, course_idx: int, top_k: int = 3) -> List[int]:
        """Find similar courses using cosine similarity of embeddings"""
        course_embedding = self.course_embeddings[course_idx]
        
        # Calculate similarities with all courses
        similarities = cosine_similarity(
            course_embedding.reshape(1, -1),
            self.course_embeddings
        )[0]
        
        # Get top-k similar (excluding the course itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_k+1]
        
        return similar_indices.tolist()
    
    def get_feature_importance(self, course_idx: int, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get most important TF-IDF features for a course"""
        course_vector = self.course_feature_matrix[course_idx].toarray()[0]
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        
        # Get top features
        top_indices = np.argsort(course_vector)[::-1][:top_n]
        
        return [(feature_names[i], course_vector[i]) for i in top_indices]
    
    def predict_user_preferences(self, profile: Dict) -> Dict[str, float]:
        """
        Predict user preferences for different categories using ML
        """
        user_embedding = self.create_user_embedding(profile)
        
        # Project user embedding to get category preferences
        categories = ["Programming", "AI/ML", "Web Development", "Data Science", 
                     "Frontend", "Backend", "Database", "Cloud"]
        
        preferences = {}
        for category in categories:
            # Transform category to embedding space
            cat_vector = self.tfidf_vectorizer.transform([category])
            
            # Calculate similarity
            similarity = cosine_similarity(
                user_embedding.reshape(1, -1),
                cat_vector.toarray()
            )[0][0]
            
            preferences[category] = float(similarity)
        
        return preferences
    
    def explain_recommendation_ml(
        self,
        user_id: str,
        profile: Dict,
        course: Dict,
        course_idx: int
    ) -> str:
        """Generate ML-based explanation for recommendation"""
        # Get hybrid scores
        _, scores = self.hybrid_recommendation_score(user_id, profile, course_idx)
        
        # Get important features
        features = self.get_feature_importance(course_idx, 3)
        feature_words = [f[0] for f in features]
        
        explanation = (
            f"ML Confidence: {scores['hybrid']*100:.1f}% "
            f"(Content: {scores['content_based']*100:.1f}%, "
            f"Collaborative: {scores['collaborative']*100:.1f}%). "
            f"Key features: {', '.join(feature_words)}"
        )
        
        return explanation
    
    def get_model_metadata(self) -> Dict:
        """Return metadata about trained models"""
        return {
            "models_trained": self.trained,
            "course_embedding_dim": self.course_embeddings.shape if self.course_embeddings is not None else None,
            "tfidf_features": len(self.tfidf_vectorizer.get_feature_names_out()) if self.tfidf_vectorizer else 0,
            "nmf_components": self.nmf_model.n_components if self.nmf_model else 0,
            "algorithms": [
                "TF-IDF Vectorization",
                "Cosine Similarity",
                "Non-negative Matrix Factorization (NMF)",
                "Hybrid Filtering (Content + Collaborative)"
            ]
        }


# Global ML engine instance (lazy initialized to avoid circular imports)
_ml_engine = None

def get_ml_engine():
    """Get or create the ML engine instance (lazy initialization)"""
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = MLEngine()
    return _ml_engine

# For backward compatibility, create a property-like access
ml_engine = None  # Will be set after imports
