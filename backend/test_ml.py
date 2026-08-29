"""
Test script for ML capabilities
Run: python test_ml.py
"""
import sys
import asyncio
sys.path.insert(0, '.')

from services.ml_engine import ml_engine
from services.profile_engine import ProfileEngine
from services.recommendation_engine import RecommendationEngine
from services.shared_state import shared_state
import numpy as np


async def test_ml_capabilities():
    print("=" * 70)
    print("Testing Machine Learning Capabilities")
    print("=" * 70)
    
    # Setup
    profile_engine = ProfileEngine()
    rec_engine = RecommendationEngine()
    
    # Create test profile
    profile = profile_engine.create_or_update_profile(
        user_id="ml_test_user",
        interests=["Python", "Machine Learning", "Data Science"],
        experience_level="Intermediate",
        goals=["Master ML algorithms"],
        completed_courses=["Python Basics", "Statistics 101"]
    )
    
    print("\n1. Testing TF-IDF Vectorization...")
    print("-" * 70)
    try:
        assert ml_engine.tfidf_vectorizer is not None
        vocab_size = len(ml_engine.tfidf_vectorizer.get_feature_names_out())
        print(f"✓ TF-IDF Vectorizer trained")
        print(f"  Vocabulary size: {vocab_size} features")
        print(f"  Sample features: {list(ml_engine.tfidf_vectorizer.get_feature_names_out()[:10])}")
    except Exception as e:
        print(f"✗ TF-IDF test failed: {e}")
        return
    
    print("\n2. Testing Course Embeddings...")
    print("-" * 70)
    try:
        assert ml_engine.course_embeddings is not None
        n_courses, n_dims = ml_engine.course_embeddings.shape
        print(f"✓ Course embeddings created")
        print(f"  Shape: {n_courses} courses × {n_dims} dimensions")
        print(f"  Sample embedding vector (first 10 dims):")
        print(f"  {ml_engine.course_embeddings[0][:10]}")
    except Exception as e:
        print(f"✗ Course embeddings test failed: {e}")
        return
    
    print("\n3. Testing User Embedding Creation...")
    print("-" * 70)
    try:
        user_embedding = ml_engine.create_user_embedding(profile)
        print(f"✓ User embedding created")
        print(f"  Embedding shape: {user_embedding.shape}")
        print(f"  Non-zero features: {np.count_nonzero(user_embedding)}")
        print(f"  L2 norm: {np.linalg.norm(user_embedding):.4f}")
    except Exception as e:
        print(f"✗ User embedding test failed: {e}")
        return
    
    print("\n4. Testing Content-Based Similarity...")
    print("-" * 70)
    try:
        similarities = []
        for idx in range(len(rec_engine.courses_db)):
            sim = ml_engine.content_based_similarity(user_embedding, idx)
            course = rec_engine.courses_db[idx]
            similarities.append((course['title'], sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"✓ Content-based similarity calculated")
        print(f"  Top 3 similar courses:")
        for title, sim in similarities[:3]:
            print(f"    {title}: {sim:.4f}")
    except Exception as e:
        print(f"✗ Content-based test failed: {e}")
        return
    
    print("\n5. Testing Collaborative Filtering (NMF)...")
    print("-" * 70)
    try:
        collab_score = ml_engine.collaborative_filtering_score(
            "ml_test_user", 
            course_idx=0
        )
        print(f"✓ Collaborative filtering working")
        print(f"  Predicted rating for course 0: {collab_score:.4f}/5.0")
        print(f"  NMF components: {ml_engine.nmf_model.n_components}")
        print(f"  Model trained: {ml_engine.trained}")
    except Exception as e:
        print(f"✗ Collaborative filtering test failed: {e}")
        return
    
    print("\n6. Testing Hybrid Recommendation Score...")
    print("-" * 70)
    try:
        for idx in range(min(3, len(rec_engine.courses_db))):
            hybrid_score, explanation = ml_engine.hybrid_recommendation_score(
                "ml_test_user",
                profile,
                idx
            )
            course = rec_engine.courses_db[idx]
            print(f"\n  Course: {course['title']}")
            print(f"    Hybrid score: {hybrid_score:.4f}")
            print(f"    Content-based: {explanation['content_based']:.4f}")
            print(f"    Collaborative: {explanation['collaborative']:.4f}")
            print(f"    Method: {explanation['method']}")
    except Exception as e:
        print(f"✗ Hybrid scoring test failed: {e}")
        return
    
    print("\n7. Testing Similar Course Discovery...")
    print("-" * 70)
    try:
        similar_indices = ml_engine.find_similar_courses(course_idx=1, top_k=3)
        print(f"✓ Similar course discovery working")
        print(f"  For course: {rec_engine.courses_db[1]['title']}")
        print(f"  Similar courses:")
        for idx in similar_indices:
            print(f"    - {rec_engine.courses_db[idx]['title']}")
    except Exception as e:
        print(f"✗ Similar course test failed: {e}")
        return
    
    print("\n8. Testing Feature Importance...")
    print("-" * 70)
    try:
        features = ml_engine.get_feature_importance(course_idx=1, top_n=5)
        print(f"✓ Feature importance extraction working")
        print(f"  Top features for {rec_engine.courses_db[1]['title']}:")
        for feature, score in features:
            print(f"    {feature}: {score:.4f}")
    except Exception as e:
        print(f"✗ Feature importance test failed: {e}")
        return
    
    print("\n9. Testing Preference Prediction...")
    print("-" * 70)
    try:
        preferences = ml_engine.predict_user_preferences(profile)
        print(f"✓ Preference prediction working")
        print(f"  Predicted category preferences:")
        sorted_prefs = sorted(preferences.items(), key=lambda x: x[1], reverse=True)
        for category, score in sorted_prefs[:5]:
            print(f"    {category}: {score:.4f}")
    except Exception as e:
        print(f"✗ Preference prediction test failed: {e}")
        return
    
    print("\n10. Testing ML-Powered Recommendations...")
    print("-" * 70)
    try:
        recommendations = await rec_engine.get_recommendations(
            "ml_test_user",
            limit=5,
            use_ml=True
        )
        print(f"✓ ML-powered recommendations generated")
        print(f"  Total found: {recommendations['total_found']}")
        print(f"  ML enabled: {recommendations['ml_enabled']}")
        print(f"\n  Top 3 recommendations:")
        for rec in recommendations['recommendations'][:3]:
            print(f"\n    {rec['title']}")
            print(f"      Score: {rec['relevance_score']:.2f}")
            print(f"      ML-powered: {rec['ml_powered']}")
            print(f"      Reasoning: {rec['reasoning']}")
        
        if recommendations.get('predicted_preferences'):
            print(f"\n  Predicted preferences available: Yes")
    except Exception as e:
        print(f"✗ ML recommendations test failed: {e}")
        return
    
    print("\n11. Testing Model Metadata...")
    print("-" * 70)
    try:
        metadata = ml_engine.get_model_metadata()
        print(f"✓ Model metadata retrieved")
        print(f"  Models trained: {metadata['models_trained']}")
        print(f"  Embedding dimensions: {metadata['course_embedding_dim']}")
        print(f"  TF-IDF features: {metadata['tfidf_features']}")
        print(f"  NMF components: {metadata['nmf_components']}")
        print(f"\n  Algorithms implemented:")
        for algo in metadata['algorithms']:
            print(f"    - {algo}")
    except Exception as e:
        print(f"✗ Metadata test failed: {e}")
        return
    
    print("\n12. Testing ML vs Rule-Based Comparison...")
    print("-" * 70)
    try:
        # ML-powered recommendations
        ml_recs = await rec_engine.get_recommendations(
            "ml_test_user", limit=3, use_ml=True
        )
        
        # Rule-based recommendations
        rule_recs = await rec_engine.get_recommendations(
            "ml_test_user", limit=3, use_ml=False
        )
        
        print(f"✓ Comparison completed")
        print(f"\n  ML-Powered Top 3:")
        for i, rec in enumerate(ml_recs['recommendations'], 1):
            print(f"    {i}. {rec['title']} (Score: {rec['relevance_score']:.2f})")
        
        print(f"\n  Rule-Based Top 3:")
        for i, rec in enumerate(rule_recs['recommendations'], 1):
            print(f"    {i}. {rec['title']} (Score: {rec['relevance_score']:.2f})")
        
        # Check if rankings differ
        ml_titles = [r['title'] for r in ml_recs['recommendations']]
        rule_titles = [r['title'] for r in rule_recs['recommendations']]
        if ml_titles != rule_titles:
            print(f"\n  ✓ ML produces different rankings (personalization working)")
        else:
            print(f"\n  ⚠ Rankings are similar (limited training data)")
    except Exception as e:
        print(f"✗ Comparison test failed: {e}")
        return
    
    print("\n" + "=" * 70)
    print("ML Testing Complete!")
    print("=" * 70)
    
    # Summary
    print("\n📊 ML Capabilities Summary:")
    print("  ✓ TF-IDF Vectorization - WORKING")
    print("  ✓ Course Embeddings - WORKING")
    print("  ✓ User Embeddings - WORKING")
    print("  ✓ Content-Based Filtering - WORKING")
    print("  ✓ Collaborative Filtering (NMF) - WORKING")
    print("  ✓ Hybrid Recommendations - WORKING")
    print("  ✓ Similar Course Discovery - WORKING")
    print("  ✓ Feature Importance - WORKING")
    print("  ✓ Preference Prediction - WORKING")
    print("  ✓ Model Metadata - WORKING")
    print("\n🎉 All ML Components Operational!")


if __name__ == "__main__":
    asyncio.run(test_ml_capabilities())
