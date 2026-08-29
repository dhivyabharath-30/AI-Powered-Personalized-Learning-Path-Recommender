import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

interface DashboardProps {
  userId: string;
}

interface Recommendation {
  id: string;
  title: string;
  category: string;
  difficulty: string;
  duration: string;
  rating: number;
  reasoning: string;
}

const Dashboard: React.FC<DashboardProps> = ({ userId }) => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  const fetchData = async () => {
    try {
      const [recsResponse, progressResponse] = await Promise.all([
        axios.get(`http://localhost:8000/api/recommendations/${userId}`),
        axios.get(`http://localhost:8000/api/progress/${userId}`)
      ]);

      setRecommendations(recsResponse.data.recommendations || []);
      setProgress(progressResponse.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const progressData = progress ? [
    { name: 'Completed', value: progress.completed_courses },
    { name: 'In Progress', value: Math.max(1, progress.active_goals) },
  ] : [];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Your Learning Dashboard</h2>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>📚 Courses Completed</h3>
          <p className="stat-value">{progress?.completed_courses || 0}</p>
        </div>
        <div className="stat-card">
          <h3>🎯 Skills Acquired</h3>
          <p className="stat-value">{progress?.skills_acquired || 0}</p>
        </div>
        <div className="stat-card">
          <h3>🎓 Active Goals</h3>
          <p className="stat-value">{progress?.active_goals || 0}</p>
        </div>
        <div className="stat-card">
          <h3>📊 Progress</h3>
          <p className="stat-value">{progress?.progress_percentage || 0}%</p>
        </div>
      </div>

      {progressData.length > 0 && (
        <div className="chart-section">
          <h3>Learning Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={progressData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {progressData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="recommendations-section">
        <h3>Recommended Courses</h3>
        <div className="recommendations-grid">
          {recommendations.slice(0, 6).map((course, index) => (
            <div key={index} className="course-card">
              <div className="course-header">
                <h4>{course.title}</h4>
                <span className="difficulty-badge">{course.difficulty}</span>
              </div>
              <p className="course-category">{course.category}</p>
              <div className="course-meta">
                <span>⏱️ {course.duration}</span>
                <span>⭐ {course.rating}/5.0</span>
              </div>
              <p className="course-reasoning">{course.reasoning}</p>
              <button className="enroll-btn">Start Learning</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
