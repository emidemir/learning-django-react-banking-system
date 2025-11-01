import React, { useState } from 'react';
import SignInForm from '../components/SignInForm';
import SignUpForm from '../components/SignUpForm';
import { useNavigate, useLocation } from 'react-router-dom';
import '../css/AuthPage.css';

export default function AuthPage() {
    const [isSignIn, setIsSignIn] = useState(true);
    const navigate = useNavigate();
    const location = useLocation();

    const handleSignInSuccess = (email) => {
        if (location.state && location.state.nextPathname) {
            navigate(location.state.nextPathname);
        } else {
            navigate('/home');
        }
    };

    const handleSignUpSuccess = (email) => {
        setIsSignIn(true);
    };

    const toggleForm = () => {
        setIsSignIn((prev) => !prev);
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                {isSignIn ? (
                    <SignInForm onSignInSuccess={handleSignInSuccess} />
                ) : (
                    <SignUpForm onSignUpSuccess={handleSignUpSuccess} />
                )}

                <p className="toggle-link">
                    {isSignIn ? "Don't have an account? " : "Already have an account? "}
                    <button onClick={toggleForm}>
                        {isSignIn ? "Sign Up" : "Sign In"}
                    </button>
                </p>
            </div>
        </div>
    );
}