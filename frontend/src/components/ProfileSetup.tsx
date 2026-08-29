import React, { useState } from 'react';
import axios from 'axios';
import './ProfileSetup.css';

interface ProfileSetupProps {
  userId: string;
  onComplete: () => void;
}

const ProfileSetup: React.FC<ProfileSetupProps> = ({ userId, onComplete }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    interests: [] as string[],
    experienceLevel: '',
    goals: [] as string[],
    completedCourses: [] as string[]
  });

  const interestOptions = [
    'Python', 'JavaScript', 'React', 'Machine Learning', 'Data Science',
    'Web Development', 'Mobile Development', 'DevOps', 'Cloud Computing',
    'Backend Development', 'Frontend Development', 'AI', 'Databases'
  ];

  const experienceLevels = ['Beginner', 'Intermediate', 'Advanced'];

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleGoalAdd = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const input = e.currentTarget.elements.namedItem('goal') as HTMLInputElement;
    if (input.value.trim()) {
      setFormData(prev => ({
        ...prev,
        goals: [...prev.goals, input.value.trim()]
      }));
      input.value = '';
    }
  };

  const handleGoalRemove = (index: number) => {
    setFormData(prev => ({
      ...prev,
      goals: prev.goals.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async () => {
    try {
      await axios.post('http://localhost:8000/api/profile', {
        user_id: userId,
        interests: formData.interests,
        experience_level: formData.experienceLevel,
        goals: formData.goals,
        completed_courses: formData.completedCourses
      });
      onComplete();
    } catch (error) {
      console.error('Error creating profile:', error);
      alert('Failed to create profile. Please try again.');
    }
  };

  return (
    <div className="profile-setup">
      <div className="setup-container">
        <h2>Let's Set Up Your Learning Profile</h2>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${(step / 3) * 100}%` }}></div>
        </div>

        {step === 1 && (
          <div className="setup-step">
            <h3>What are you interested in learning?</h3>
            <p className="step-description">Select all topics that interest you</p>
            <div className="interest-grid">
              {interestOptions.map(interest => (
                <button
                  key={interest}
                  className={`interest-chip ${formData.interests.includes(interest) ? 'selected' : ''}`}
                  onClick={() => handleInterestToggle(interest)}
                >
                  {interest}
                </button>
              ))}
            </div>
            <button
              className="next-btn"
              onClick={() => setStep(2)}
              disabled={formData.interests.length === 0}
            >
              Next
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="setup-step">
            <h3>What's your experience level?</h3>
            <p className="step-description">This helps us recommend appropriate courses</p>
            <div className="experience-options">
              {experienceLevels.map(level => (
                <button
                  key={level}
                  className={`experience-card ${formData.experienceLevel === level ? 'selected' : ''}`}
                  onClick={() => setFormData(prev => ({ ...prev, experienceLevel: level }))}
                >
                  <h4>{level}</h4>
                  <p>
                    {level === 'Beginner' && 'Just getting started'}
                    {level === 'Intermediate' && 'Some experience and fundamentals'}
                    {level === 'Advanced' && 'Experienced and looking to specialize'}
                  </p>
                </button>
              ))}
            </div>
            <div className="step-buttons">
              <button className="back-btn" onClick={() => setStep(1)}>Back</button>
              <button
                className="next-btn"
                onClick={() => setStep(3)}
                disabled={!formData.experienceLevel}
              >
                Next
              </button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="setup-step">
            <h3>What are your learning goals?</h3>
            <p className="step-description">Add specific goals you want to achieve</p>
            <form onSubmit={handleGoalAdd} className="goal-form">
              <input
                type="text"
                name="goal"
                placeholder="E.g., Build a mobile app, Get a data science job..."
              />
              <button type="submit">Add Goal</button>
            </form>
            <div className="goals-list">
              {formData.goals.map((goal, index) => (
                <div key={index} className="goal-item">
                  <span>{goal}</span>
                  <button onClick={() => handleGoalRemove(index)}>✕</button>
                </div>
              ))}
            </div>
            <div className="step-buttons">
              <button className="back-btn" onClick={() => setStep(2)}>Back</button>
              <button
                className="complete-btn"
                onClick={handleSubmit}
                disabled={formData.goals.length === 0}
              >
                Complete Setup
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileSetup;
