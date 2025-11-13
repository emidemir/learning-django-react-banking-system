import React from 'react';

const ActionButtons = ({ isEditing, isSaving, onEditToggle, onPasswordChangeClick, message }) => {
    // Determine message class based on content
    const messageClass = message.includes('success') ? 'success' : message ? 'error' : '';

    return (
        <div className="profile-actions">
            {message && <p className={`message ${messageClass}`}>{message}</p>}
            
            <div className="button-group">
                {isEditing ? (
                    <>
                        <button type="submit" form="profile-form" className="save-btn" disabled={isSaving}>
                            {isSaving ? 'Saving...' : 'Save Changes'}
                        </button>
                        <button type="button" className="cancel-btn" onClick={onEditToggle} disabled={isSaving}>
                            Cancel
                        </button>
                    </>
                ) : (
                    <button type="button" className="edit-btn" onClick={onEditToggle}>
                        Edit Profile
                    </button>
                )}
                <button type="button" className="change-password-btn" onClick={onPasswordChangeClick}>
                    Change Password
                </button>
            </div>
             <small className="password-note">To change your password, please use the dedicated "Change Password" button.</small>
        </div>
    );
};

export default ActionButtons;