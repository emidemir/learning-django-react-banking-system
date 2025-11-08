import React, { useState } from 'react';
import { FcGoogle } from 'react-icons/fc';
import { useGoogleLogin } from '@react-oauth/google';
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
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/signup/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });
    
            const data = await response.json();
            
            console.log('Response data:', data);
    
            if (!response.ok) {
                setError(data.detail || "Signup failed. Please try again.");
                setLoading(false);
                return;
            }
    
            if (data.Token) {
                localStorage.setItem('access_token', data.Token);
                localStorage.setItem('refresh_token', data.refresh_token);
            }
    
            setUsername("");
            setEmail("");
            setPassword("");
            setConfirmPassword("");
            setLoading(false);
            onSignUpSuccess(email);
            
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
                    setError(data.detail || "Google Sign-Up failed.");
                    setLoading(false);
                    return;
                }

                const data = await response.json();

                console.log(data)
                
                if (data.Token) {
                    localStorage.setItem('authToken', data.Token);
                }
                
                const userEmail = data.user.email;
                onSignUpSuccess(userEmail);

            } catch (error) {
                console.error("Google Sign-Up Error:", error);
                setError("Failed to connect for Google Sign-Up.");
                setLoading(false);
            }
        },
        onError: () => {
            setError("Google Sign-Up was cancelled or failed.");
            setLoading(false);
        }
    });

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
                Sign Up with Google
            </button>
        </form>
    );
}