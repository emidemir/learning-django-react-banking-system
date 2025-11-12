import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../css/EmailVerificationPage.css';

export default function EmailVerificationPage({email}) {
    const navigate = useNavigate()
    const location = useLocation();
    const userEmail = email
    const [code, setCode] = useState()
    const [verificationStatus, setVerificationStatus] = useState('');

    
    const handleSubmitCode = async () => {
        
        setVerificationStatus('');
        
        try {
            const token = localStorage.getItem('access_token');
            
            if (!token) {
                console.log('5. No token found - stopping here');
                setVerificationStatus('error');
                console.error('No access token found. Please log in.');
                return;
            }
            
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/verify/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ code: code }),
            });
            
            if (response.ok){
                navigate('/home', {state: {email: userEmail}});
            }
            
        } catch (error) {
            console.log('8. Caught error:', error);
            setVerificationStatus('error');
            console.error('Error submitting verification code:', error);
        }
    };
    return (
        <div className="verification-container">
            <div className="verification-card">
                <div className="icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                </div>
                <h2>Verify Your Email Address</h2>
                <p>
                    A verification email has been sent to <strong>{userEmail}</strong>.
                    Please check your inbox.
                </p>
                <div className="code-input-wrapper">
                    <input
                        type="text"
                        pattern="\d*" // Suggests to mobile keyboards to show numeric keyboard
                        maxLength={6}
                        onChange={(e)=>{setCode(e.target.value)}}
                        placeholder="Enter your code"
                        className="verification-code-input"
                    />
                </div>
                <button className="verify-button" onClick={handleSubmitCode}>Verify Account</button>
                {verificationStatus === 'success' && <p className="success-message">Account Verified!</p>}
                {verificationStatus === 'error' && <p className="error-message">Invalid code or verification failed.</p>}
            </div>
        </div>
    );
}