import React from 'react';

const Avatar = ({ avatarUrl, isEditing }) => (
    <div className="avatar-section">
        <img
            src={avatarUrl || 'default_avatar_url.png'} // Provide a real default
            alt="User Avatar"
            className="profile-avatar"
            onError={(e) => {
                e.target.onerror = null;
                e.target.src = 'placeholder_avatar_url.png'; // Placeholder on error
            }}
        />
        {isEditing && (
            <button className="upload-avatar-btn" disabled>
                Change Avatar (WIP)
            </button>
        )}
    </div>
);

export default Avatar;