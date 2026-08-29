import React, { useState } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import ProfileSetup from './components/ProfileSetup';
import LearningPath from './components/LearningPath';

function App() {
  const [currentView, setCurrentView] = useState<'profile' | 'dashboard' | 'chat' | 'path'>('profile');
  const [userId] = useState<string>('user_123');
  const [hasProfile, setHasProfile] = useState<boolean>(false);

  const handleProfileComplete = () => {
    setHasProfile(true);
    setCurrentView('dashboard');
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎓 AI Learning Path Recommender</h1>
        <nav className="nav-menu">
          {hasProfile && (
            <>
              <button onClick={() => setCurrentView('dashboard')}>Dashboard</button>
              <button onClick={() => setCurrentView('chat')}>Chat</button>
              <button onClick={() => setCurrentView('path')}>Learning Path</button>
              <button onClick={() => setCurrentView('profile')}>Profile</button>
            </>
          )}
        </nav>
      </header>

      <main className="app-main">
        {currentView === 'profile' && (
          <ProfileSetup userId={userId} onComplete={handleProfileComplete} />
        )}
        {currentView === 'dashboard' && <Dashboard userId={userId} />}
        {currentView === 'chat' && <ChatInterface userId={userId} />}
        {currentView === 'path' && <LearningPath userId={userId} />}
      </main>
    </div>
  );
}

export default App;
