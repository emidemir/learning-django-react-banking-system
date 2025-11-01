import React, { useState } from 'react';
import '../css/AuthPage.css';

export default function SignUpForm({ onSignUpSuccess }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        const formData = {
            'username': username,
            'email': email,
            'password': password
        }

        // Basic validation
        if (!username || !email || !password || !confirmPassword) {
            setError('All fields are required.');
            return;
        }
        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }
        if (password.length < 6) {
            setError('Password must be at least 6 characters long.');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/signup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const data = await response.json();
                setError(data.detail || "Signup failed. Please try again.");
                setLoading(false);
                return;
            }

            setUsername("");
            setEmail("");
            setPassword("");
            setConfirmPassword("");
            onSignUpSuccess(email);
            
        } catch (error) {
            console.error("Error:", error);
            setError("Failed to connect to server. Please check if the server is running.");
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Sign Up</h2>
            {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
            <div className="form-group">
                <label htmlFor="signUpUsername">Username:</label>
                <input
                    type="text"
                    id="signUpUsername"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="signUpEmail">Email:</label>
                <input
                    type="email"
                    id="signUpEmail"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="signUpPassword">Password:</label>
                <input
                    type="password"
                    id="signUpPassword"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete='off'
                />
            </div>
            <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password:</label>
                <input
                    type="password"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    autoComplete='off'
                />
            </div>
            <button type="submit" className="auth-button" disabled={loading}>
                {loading ? 'Signing Up...' : 'Sign Up'}
            </button>
        </form>
    );
}