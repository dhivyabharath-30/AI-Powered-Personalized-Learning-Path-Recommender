import React, { useState } from 'react';
import axios from 'axios';
import './LearningPath.css';

interface LearningPathProps {
  userId: string;
}

interface Course {
  id: string;
  title: string;
  difficulty: string;
  duration: string;
  skills: string[];
}

interface Milestone {
  milestone_number: number;
  course_title: string;
  target_date: string;
  skills_to_acquire: string[];
}

const LearningPath: React.FC<LearningPathProps> = ({ userId }) => {
  const [goal, setGoal] = useState('');
  const [timeframe, setTimeframe] = useState('3 months');
  const [learningPath, setLearningPath] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!goal.trim()) {
      alert('Please enter a learning goal');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/learning-path', {
        user_id: userId,
        goal: goal,
        timeframe: timeframe
      });
      setLearningPath(response.data);
    } catch (error) {
      console.error('Error generating learning path:', error);
      alert('Failed to generate learning path');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="learning-path">
      <div className="path-generator">
        <h2>Generate Your Learning Path</h2>
        <div className="generator-form">
          <div className="form-group">
            <label>What do you want to learn?</label>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="E.g., Become a full-stack developer, Master machine learning..."
            />
          </div>
          <div className="form-group">
            <label>Timeframe</label>
            <select value={timeframe} onChange={(e) => setTimeframe(e.target.value)}>
              <option value="1 month">1 month</option>
              <option value="3 months">3 months</option>
              <option value="6 months">6 months</option>
              <option value="1 year">1 year</option>
            </select>
          </div>
          <button onClick={handleGenerate} disabled={loading} className="generate-btn">
            {loading ? 'Generating...' : 'Generate Learning Path'}
          </button>
        </div>
      </div>

      {learningPath && (
        <div className="path-result">
          <div className="path-header">
            <h3>Your Personalized Learning Path</h3>
            <div className="path-meta">
              <span>🎯 Goal: {learningPath.goal}</span>
              <span>⏰ Duration: {learningPath.timeframe}</span>
              <span>📚 Courses: {learningPath.total_courses}</span>
            </div>
          </div>

          <div className="path-timeline">
            {learningPath.path?.map((course: Course, index: number) => (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">{index + 1}</div>
                <div className="timeline-content">
                  <h4>{course.title}</h4>
                  <div className="course-details">
                    <span className="badge">{course.difficulty}</span>
                    <span>⏱️ {course.duration}</span>
                  </div>
                  <div className="skills-list">
                    <strong>Skills you'll learn:</strong>
                    <div className="skills-tags">
                      {course.skills.map((skill, i) => (
                        <span key={i} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {learningPath.milestones && (
            <div className="milestones-section">
              <h3>Milestones</h3>
              <div className="milestones-grid">
                {learningPath.milestones.map((milestone: Milestone, index: number) => (
                  <div key={index} className="milestone-card">
                    <div className="milestone-header">
                      <span className="milestone-number">Milestone {milestone.milestone_number}</span>
                      <span className="milestone-date">{milestone.target_date}</span>
                    </div>
                    <h4>{milestone.course_title}</h4>
                    <div className="milestone-skills">
                      {milestone.skills_to_acquire.join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="path-explanation">
            <h3>Why This Path?</h3>
            <p>{learningPath.explanation}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default LearningPath;
