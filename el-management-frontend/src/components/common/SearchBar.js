import React from 'react';

const SearchBar = ({ placeholder, value, onChange, onClear }) => {
    return (
        <div style={{
            position: 'relative',
            width: '100%',
            maxWidth: '400px',
        }}>
            <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
            }}>
                <span style={{
                    position: 'absolute',
                    left: 'var(--space-md)',
                    color: 'var(--color-text-dim)',
                    fontSize: '1.25rem',
                }}>
                    🔍
                </span>
                <input
                    type="text"
                    placeholder={placeholder || 'Search...'}
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    style={{
                        width: '100%',
                        paddingLeft: 'calc(var(--space-md) * 2.5)',
                        paddingRight: value ? 'calc(var(--space-md) * 2.5)' : 'var(--space-md)',
                    }}
                />
                {value && (
                    <button
                        onClick={onClear}
                        style={{
                            position: 'absolute',
                            right: 'var(--space-md)',
                            background: 'none',
                            border: 'none',
                            color: 'var(--color-text-dim)',
                            cursor: 'pointer',
                            fontSize: '1.25rem',
                            padding: 'var(--space-xs)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            transition: 'color var(--transition-base)',
                        }}
                        onMouseEnter={(e) => e.target.style.color = 'var(--color-error)'}
                        onMouseLeave={(e) => e.target.style.color = 'var(--color-text-dim)'}
                    >
                        ✕
                    </button>
                )}
            </div>
        </div>
    );
};

export default SearchBar;
