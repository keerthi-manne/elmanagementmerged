import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await loginUser(email, password);

      if (result.success) {
        if (result.role === 'Admin') {
          navigate('/admin');
        } else if (result.role === 'Faculty') {
          navigate('/faculty');
        } else if (result.role === 'Student') {
          navigate('/student');
        } else {
          navigate('/dashboard');
        }
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, var(--color-bg) 0%, var(--color-primary) 50%, #0a0e27 100%)',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Animated Background Elements */}
      <div style={{
        position: 'absolute',
        top: '10%',
        left: '10%',
        width: '300px',
        height: '300px',
        background: 'radial-gradient(circle, rgba(100, 255, 218, 0.1) 0%, transparent 70%)',
        borderRadius: '50%',
        animation: 'float 6s ease-in-out infinite',
      }} />
      <div style={{
        position: 'absolute',
        bottom: '15%',
        right: '15%',
        width: '400px',
        height: '400px',
        background: 'radial-gradient(circle, rgba(247, 127, 0, 0.1) 0%, transparent 70%)',
        borderRadius: '50%',
        animation: 'float 8s ease-in-out infinite reverse',
      }} />

      {/* Login Card */}
      <div className="glass-card fade-in-up" style={{
        maxWidth: '450px',
        width: '90%',
        padding: 'var(--space-2xl)',
        zIndex: 1,
      }}>
        {/* Logo/Title */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
          <h1 style={{
            fontSize: '2rem',
            fontWeight: 800,
            margin: 0,
            marginBottom: 'var(--space-sm)',
          }} className="text-gradient text-glow">
            EL Management
          </h1>
          <p style={{ color: 'var(--color-text-dim)', margin: 0 }}>
            Project & Evaluation Platform
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--space-md)',
        }}>
          <div>
            <label style={{
              display: 'block',
              marginBottom: 'var(--space-xs)',
              color: 'var(--color-text)',
              fontSize: '0.875rem',
              fontWeight: 600,
            }}>
              Email or User ID
            </label>
            <input
              type="text"
              placeholder="Enter your email or USN"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div>
            <label style={{
              display: 'block',
              marginBottom: 'var(--space-xs)',
              color: 'var(--color-text)',
              fontSize: '0.875rem',
              fontWeight: 600,
            }}>
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{
              marginTop: 'var(--space-md)',
              padding: 'var(--space-md)',
              fontSize: '1rem',
            }}
          >
            {loading ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 'var(--space-sm)' }}>
                <div className="spinner" style={{ width: '20px', height: '20px' }} />
                <span>Logging in...</span>
              </div>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="alert alert-error" style={{ marginTop: 'var(--space-md)' }}>
            {error}
          </div>
        )}

        {/* Demo Credentials */}
        <div style={{
          marginTop: 'var(--space-2xl)',
          padding: 'var(--space-md)',
          background: 'var(--color-surface)',
          borderRadius: 'var(--radius-md)',
          borderLeft: `4px solid var(--color-accent)`,
        }}>
          <div style={{
            fontSize: '0.75rem',
            fontWeight: 600,
            color: 'var(--color-text-dim)',
            marginBottom: 'var(--space-sm)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}>
            Demo Credentials
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text)' }}>
            <div style={{ marginBottom: 'var(--space-xs)' }}>
              <strong style={{ color: 'var(--color-accent)' }}>Admin:</strong> admin@rvce.edu.in / admin123
            </div>
            <div>
              <strong style={{ color: 'var(--color-accent)' }}>Faculty:</strong> faculty@rvce.edu.in / faculty123
            </div>
          </div>
        </div>
      </div>

      {/* Floating Animation Keyframes */}
      <style>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0) translateX(0);
          }
          50% {
            transform: translateY(-20px) translateX(20px);
          }
        }
      `}</style>
    </div>
  );
}

export default Login;
