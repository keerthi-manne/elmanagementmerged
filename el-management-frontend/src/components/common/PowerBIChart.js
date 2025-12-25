import React from 'react';

const PowerBIChart = ({ title, data, type = 'bar' }) => {
    if (!data || data.length === 0) return null;

    const maxValue = Math.max(...data.map(d => d.value));

    if (type === 'donut') {
        const total = data.reduce((sum, item) => sum + item.value, 0);
        let currentAngle = 0;

        return (
            <div style={{ padding: 'var(--space-md)' }}>
                <h4 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)', fontSize: '1rem' }}>
                    {title}
                </h4>
                <div style={{ display: 'flex', gap: 'var(--space-xl)', alignItems: 'center' }}>
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        {data.map((item, idx) => {
                            const percentage = (item.value / total) * 100;
                            const angle = (percentage / 100) * 360;
                            const startAngle = currentAngle;
                            const endAngle = currentAngle + angle;

                            const x1 = 100 + 80 * Math.cos((Math.PI * startAngle) / 180);
                            const y1 = 100 + 80 * Math.sin((Math.PI * startAngle) / 180);
                            const x2 = 100 + 80 * Math.cos((Math.PI * endAngle) / 180);
                            const y2 = 100 + 80 * Math.sin((Math.PI * endAngle) / 180);

                            const largeArc = angle > 180 ? 1 : 0;

                            const pathData = [
                                `M 100 100`,
                                `L ${x1} ${y1}`,
                                `A 80 80 0 ${largeArc} 1 ${x2} ${y2}`,
                                `Z`
                            ].join(' ');

                            currentAngle += angle;

                            const colors = ['#3C50E0', '#10B981', '#F59E0B', '#EF4444', '#6577F3', '#8B5CF6'];

                            return (
                                <path
                                    key={idx}
                                    d={pathData}
                                    fill={colors[idx % colors.length]}
                                    stroke="var(--color-bg)"
                                    strokeWidth="2"
                                    style={{ transition: 'all 0.3s ease' }}
                                />
                            );
                        })}
                        <circle cx="100" cy="100" r="50" fill="var(--color-bg)" />
                    </svg>
                    <div style={{ flex: 1 }}>
                        {data.map((item, idx) => {
                            const colors = ['#3C50E0', '#10B981', '#F59E0B', '#EF4444', '#6577F3', '#8B5CF6'];
                            return (
                                <div key={idx} style={{ marginBottom: 'var(--space-sm)', display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                                    <div style={{
                                        width: '12px',
                                        height: '12px',
                                        borderRadius: '2px',
                                        background: colors[idx % colors.length]
                                    }} />
                                    <span style={{ fontSize: '0.875rem', color: 'var(--color-text)' }}>
                                        {item.label}: <strong>{item.value}</strong>
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        );
    }

    // Bar chart (existing)
    return (
        <div style={{ padding: 'var(--space-md)' }}>
            <h4 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)', fontSize: '1rem' }}>
                {title}
            </h4>
            {data.map((item, index) => (
                <div key={index} style={{ marginBottom: 'var(--space-md)' }}>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: 'var(--space-xs)',
                    }}>
                        <span style={{
                            fontSize: '0.875rem',
                            color: 'var(--color-text)',
                            fontWeight: 500,
                        }}>
                            {item.label}
                        </span>
                        <span style={{
                            fontSize: '0.875rem',
                            color: 'var(--color-accent)',
                            fontWeight: 700,
                        }}>
                            {item.value}
                        </span>
                    </div>
                    <div style={{
                        width: '100%',
                        height: '8px',
                        background: 'var(--color-surface)',
                        borderRadius: 'var(--radius-md)',
                        overflow: 'hidden',
                        position: 'relative',
                    }}>
                        <div style={{
                            width: `${(item.value / maxValue) * 100}%`,
                            height: '100%',
                            background: `linear-gradient(90deg, var(--color-accent) 0%, var(--color-accent-dim) 100%)`,
                            borderRadius: 'var(--radius-md)',
                            transition: 'width 0.6s ease',
                            boxShadow: '0 0 10px rgba(60, 80, 224, 0.5)',
                        }} />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PowerBIChart;
