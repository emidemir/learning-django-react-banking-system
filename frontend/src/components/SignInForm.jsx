import React, { useState } from 'react';
import { FcGoogle } from "react-icons/fc";
import { useGoogleLogin } from '@react-oauth/google';
import '../css/AuthPage.css';

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
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "email": email, "password": password }),
            });

            if (!response.ok) {
                const data = await response.json();
                const errorMsg = data.detail || data.non_field_errors?.[0] || data.email?.[0] || data.password?.[0] || "Login failed. Please try again.";
                setError(errorMsg);
                setLoading(false);
                return;
            }

            const data = await response.json();

            if (data.Token) {
                localStorage.setItem('authToken', data.Token);
            }

            onSignInSuccess(email);

        } catch (error) {
            console.error("Error:", error);
            setError("Failed to connect to server. Please check if the server is running.");
            setLoading(false);
        }
    };

    const googleLogin = useGoogleLogin({
        onSuccess: async (tokenResponse) => {
            setLoading(true);
            setError('');

            try {
                // Send the access token to your Django backend
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/oauth/google/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ access_token: tokenResponse.access_token }),
                });

                if (!response.ok) {
                    const data = await response.json();
                    setError(data.detail || "Google Sign-In failed.");
                    setLoading(false);
                    return;
                }

                const data = await response.json();

                if (data.Token) {
                    localStorage.setItem('authToken', data.Token);
                }

                // Extract email from response
                const userEmail = data.user?.email || data.email;
                onSignInSuccess(userEmail);

            } catch (error) {
                console.error("Google Sign-In Error:", error);
                setError("Failed to connect for Google Sign-In.");
                setLoading(false);
            }
        },
        onError: () => {
            setError("Google Sign-In was cancelled or failed.");
            setLoading(false);
        }
    });

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

            <div style={{ textAlign: 'center', margin: '20px 0', color: '#888' }}>
                OR
            </div>

            <button
                type="button"
                className="auth-button google-signin-btn"
                onClick={() => googleLogin()}
                disabled={loading}
                style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    backgroundColor: '#fff',
                    color: '#444',
                    border: '1px solid #ccc'
                }}
            >
                <FcGoogle style={{ marginRight: '10px' }} />
                Sign In with Google
            </button>
        </form>
    );
}