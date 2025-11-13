import React, { useState, useEffect, props } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../css/ProfilePage.css';

// Import the child components (ProfileHeader is removed)
import Avatar from '../components/Avatar';
import ProfileForm from '../components/ProfileForm';
import ActionButtons from '../components/ActionButtons';

export default function ProfilePage() {
    const location = useLocation();
    const navigate = useNavigate();

    const authToken = localStorage.getItem('authToken');

    // State for user data
    const [profile, setProfile] = useState({
        userName: location.state.userName,
        email: location.state.email,
        avatar: location.state.avatar,
        phoneNumber: location.state.phoneNumber,
        birthDate: location.state.birthDate,
    });
    
    // UI state
    const [isEditing, setIsEditing] = useState(false);
    const [message, setMessage] = useState('');
    const [isSaving, setIsSaving] = useState(false);

    // Handle input changes in the form
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProfile(prevProfile => ({
            ...prevProfile,
            [name]: value,
        }));
    };

    // Handle saving the updated profile
    const handleSave = async (e) => {
        e.preventDefault();
        setIsSaving(true);
        setMessage('Saving...');

        const updatedProfile = {
            userName: profile.userName,
            phone_number: profile.phoneNumber,
            date_of_birth: profile.birthDate,
        };

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // On success
            setMessage('Profile updated successfully! ✅');
            setIsEditing(false);
        } catch (error) {
            setMessage('Failed to update profile. Please try again.');
        } finally {
            setIsSaving(false);
        }
    };

    // Toggle edit mode
    const handleEditToggle = () => {
        setIsEditing(!isEditing);
        setMessage(''); // Clear any previous messages
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                {/* ProfileHeader component is removed from here */}
                <Avatar avatarUrl={profile.avatar} isEditing={isEditing} />
                <ProfileForm
                    profile={profile}
                    isEditing={isEditing}
                    onInputChange={handleInputChange}
                    onSubmit={handleSave}
                />
                <ActionButtons
                    isEditing={isEditing}
                    isSaving={isSaving}
                    onEditToggle={handleEditToggle}
                    onPasswordChangeClick={() => navigate('/change-password')}
                    message={message}
                />
            </div>
        </div>
    );
}