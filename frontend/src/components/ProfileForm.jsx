import React, { useState } from 'react';
import FormField from './FormField';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash, faLock } from '@fortawesome/free-solid-svg-icons';

const ProfileForm = ({ profile, isEditing, onInputChange, onSubmit }) => {
    const [isPasswordVisible, setIsPasswordVisible] = useState(false);

    return (
        <form onSubmit={onSubmit} className="profile-form">
            <FormField
                label="Username"
                type="text"
                name="username"
                value={profile.userName}
                isEditing={isEditing}
                onChange={onInputChange}
            />
            <FormField
                label="Email"
                type="email"
                name="email"
                value={profile.email}
                isEditing={false} // Email is never editable
            />
            
            {/* Password Field - special case */}
            <div className="form-group">
                <label>Password</label>
                <div className="password-input-wrapper">
                    <input
                        type={isPasswordVisible ? 'text' : 'password'}
                        value="**********"
                        readOnly
                    />
                    <FontAwesomeIcon icon={faLock} className="password-lock-icon" />
                    <button
                        type="button"
                        onClick={() => setIsPasswordVisible(!isPasswordVisible)}
                        className="password-toggle-btn"
                        aria-label={isPasswordVisible ? "Hide password" : "Show password"}
                    >
                        <FontAwesomeIcon icon={isPasswordVisible ? faEyeSlash : faEye} />
                    </button>
                </div>
            </div>

            <FormField
                label="Phone Number"
                type="tel"
                name="phoneNumber"
                value={profile.phoneNumber}
                isEditing={isEditing}
                onChange={onInputChange}
            />
            <FormField
                label="Date of Birth"
                type="date"
                name="birthDate"
                value={profile.birthDate}
                isEditing={isEditing}
                onChange={onInputChange}
            />
        </form>
    );
};

export default ProfileForm;