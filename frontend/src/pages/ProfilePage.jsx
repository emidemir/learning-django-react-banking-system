import React, { useState, useEffect, useEffectEvent } from 'react';
import { Meta, useLocation, useNavigate } from 'react-router-dom';
import '../css/ProfilePage.css';

// Define gender choices based on the CustomUser model for the frontend
const GENDER_CHOICES = [
    { value: 'MALE', label: 'Male' },
    { value: 'FEMALE', label: 'Female' },
    { value: 'OTHER', label: 'Other' },
    { value: 'NOT_SPECIFIED', label: 'Not Specified' },
];

export default function ProfilePage({email}) {
    const navigate = useNavigate()
    
    // ----- UX STATES -----
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateError, setUpdateError] = useState('');
    const [updateSuccess, setUpdateSuccess] = useState('');

    const authToken = localStorage.getItem('authToken');

    // ----- PROFILE INFORMATION STATES -----
    const [user, setUserName] = useState();
    const [avatar, setAvatar] = useState();
    const [phoneNumber, setPhoneNumber] = useState();
    const [birthDate, setBirthDate] = useState();

    // Redirect unauthorized users to login
    useEffect(()=>{
        if(!authToken){
            navigate('/auth', {state: { nextPathname: '/profile' }}) 
            // Passign states between components
            // use 'useLocation' to pick them on /auth
            // const {state} = useLocation();
            // const { nextPathName } = state;
            return;
        }
    }, [authToken, navigate]);

    useEffect(()=>{
        const fetchData = () => {

        }

        fetchData()
    },[authToken])

    // Handle gender update submission
    const handleUpdate = async (e) => {
        e.preventDefault();
        setIsUpdating(true);
        setUpdateError('');
        setUpdateSuccess('');

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/user/profile/${email}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Token ${authToken}`,
                },
                body: JSON.stringify({ gender: user.gender }),
            });

            if (!response.ok) {
                setError("Update failed!")
                const data = await response.json();
                throw new Error(data.detail || data.gender?.[0] || "Failed to update profile.");
            }

            setUpdateSuccess("Profile updated successfully!");
        } catch (err) {
            console.error("Update profile error:", err);
            setUpdateError(err.message);
        } finally {
            setIsUpdating(false);
            // Clear success/error messages after a few seconds
            setTimeout(() => {
                setUpdateSuccess('');
                setUpdateError('');
            }, 5000);
        }
    };

    // Handle Log Out
    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('/auth');
    };

    if (!authToken || loading) {
        return <div className="profile-container"><p>Loading profile...</p></div>;
    }

    if (error) {
        return <div className="profile-container"><p style={{ color: 'red' }}>Error: {error}</p></div>;
    }

    return (
        <div className="profile-container">
            <div className="profile-card">
                <h2>Your Profile Information</h2>
                <div className="info-group">
                    <strong>Username:</strong> <span>{user.username || 'N/A'}</span>
                </div>
                <div className="info-group">
                    <strong>Email:</strong> <span>{user.email}</span>
                </div>
                <div className="info-group">
                    <strong>Verification Status:</strong> 
                    <span style={{ color: user.is_verified ? 'green' : 'red', fontWeight: 'bold' }}>
                        {user.is_verified ? 'Verified ✅' : 'Unverified ❌'}
                    </span>
                </div>
                
                <hr />

                <h3>Update Details</h3>
                <form onSubmit={handleUpdate}>
                    <div className="form-group">
                        <label htmlFor="gender">Gender:</label>
                        <select
                            id="gender"
                            value={user.gender}
                            onChange={(e) => setUser({ ...user, gender: e.target.value })}
                            required
                        >
                            {GENDER_CHOICES.map((choice) => (
                                <option key={choice.value} value={choice.value}>
                                    {choice.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {updateError && <p style={{ color: 'red', marginBottom: '15px' }}>{updateError}</p>}
                    {updateSuccess && <p style={{ color: 'green', marginBottom: '15px' }}>{updateSuccess}</p>}
                    
                    <button type="submit" className="auth-button" disabled={isUpdating}>
                        {isUpdating ? 'Updating...' : 'Update Gender'}
                    </button>
                </form>

                <hr />

                <button 
                    onClick={handleLogout} 
                    className="auth-button logout-button" 
                    style={{ backgroundColor: '#dc3545' }}
                >
                    Log Out
                </button>
            </div>
        </div>
    );
}