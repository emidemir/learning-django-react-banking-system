import React, { useState } from 'react';
import '../css/AuthPage.css'

export default function SignInForm({ onSignInSuccess }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        if (!email || !password) {
            setError('Please enter both email and password.');
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({"email": email, "password": password}),
            });

            if (!response.ok) {
                const data = await response.json();
                setError(data.detail || "Login failed. Please try again.");
                setLoading(false);
                return;
            }

            const data = await response.json();
            
            // Store token if your backend returns one
            if (data.token) {
                localStorage.setItem('authToken', data.token);
            }
            
            // Call success callback to navigate
            onSignInSuccess(email);
            
        } catch (error) {
            console.error("Error:", error);
            setError("Failed to connect to server. Please check if the server is running.");
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Sign In</h2>
            {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
            <div className="form-group">
                <label htmlFor="signInEmail">Email:</label>
                <input
                    type="email"
                    id="signInEmail"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="signInPassword">Password:</label>
                <input
                    type="password"
                    id="signInPassword"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete='off'
                />
            </div>
            <button type="submit" className="auth-button" disabled={loading}>
                {loading ? 'Signing In...' : 'Sign In'}
            </button>
        </form>
    );
}