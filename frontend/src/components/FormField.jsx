import React from 'react';

const FormField = ({ label, type, name, value, isEditing, onChange }) => (
    <div className="form-group">
        <label htmlFor={name}>{label}</label>
        <input
            id={name}
            type={type}
            name={name}
            value={value}
            onChange={onChange}
            readOnly={!isEditing}
            className={isEditing ? 'editable' : 'read-only'}
        />
    </div>
);

export default FormField;