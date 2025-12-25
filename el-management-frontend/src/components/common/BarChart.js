import React from 'react';

const BarChart = ({ data, maxValue }) => {
    if (!data || data.length === 0) {
        return (
            <div style={{
                padding: 'var(--space-lg)',
                textAlign: 'center',
                color: 'var(--color-text-dim)',
            }}>
                No data available
            </div>
        );
    }

    const max = maxValue || Math.max(...data.map(d => d.value));

    return (
        <div style={{ padding: 'var(--space-md)' }}>
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
                            width: `${(item.value / max) * 100}%`,
                            height: '100%',
                            background: `linear-gradient(90deg, var(--color-accent) 0%, var(--color-accent-dim) 100%)`,
                            borderRadius: 'var(--radius-md)',
                            transition: 'width 0.6s ease',
                            boxShadow: '0 0 10px rgba(100, 255, 218, 0.5)',
                        }} />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default BarChart;
