import React from 'react';

const StatsWidget = ({ title, value, subtitle, icon, trend, color = 'accent' }) => {
  const colorMap = {
    accent: 'var(--color-accent)',
    success: 'var(--color-success)',
    warning: 'var(--color-warning)',
    error: 'var(--color-error)',
    info: 'var(--color-info)',
  };

  return (
    <div className="glass-card fade-in-up" style={{
      padding: 'var(--space-lg)',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Background Glow */}
      <div style={{
        position: 'absolute',
        top: '-50%',
        right: '-20%',
        width: '150px',
        height: '150px',
        background: `radial-gradient(circle, ${colorMap[color]}20 0%, transparent 70%)`,
        borderRadius: '50%',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 1 }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: 'var(--space-md)',
        }}>
          <h3 style={{
            fontSize: '0.875rem',
            fontWeight: 600,
            color: 'var(--color-text-dim)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            margin: 0,
          }}>
            {title}
          </h3>
          {icon && (
            <span style={{
              fontSize: '1.5rem',
              opacity: 0.6,
            }}>
              {icon}
            </span>
          )}
        </div>

        {/* Value */}
        <div style={{
          fontSize: '2.5rem',
          fontWeight: 800,
          color: colorMap[color],
          marginBottom: 'var(--space-sm)',
          textShadow: `0 0 20px ${colorMap[color]}40`,
        }}>
          {value}
        </div>

        {/* Subtitle/Trend */}
        {subtitle && (
          <div style={{
            fontSize: '0.875rem',
            color: 'var(--color-text-dim)',
          }}>
            {subtitle}
          </div>
        )}

        {trend && (
          <div style={{
            marginTop: 'var(--space-sm)',
            fontSize: '0.875rem',
            color: trend > 0 ? 'var(--color-success)' : 'var(--color-error)',
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-xs)',
          }}>
            <span>{trend > 0 ? '↗' : '↘'}</span>
            <span>{Math.abs(trend)}%</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsWidget;
