import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/TransferFundsPage.css'; // You'll create this CSS file

export default function TransferFunds({email}) {
    const navigate = useNavigate();

    const [allAccounts, setAllAccounts] = useState([]);
    const [title, setTitle] = useState('');
    const [fromAccountNumber, setfromAccountNumber] = useState('');
    const [toAccountNumber, setToAccountNumber] = useState('');
    const [amount, setAmount] = useState('');
    const [description, setDescription] = useState('');
    
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const authToken = localStorage.getItem('authToken');

    // Redirect unauthorized users
    useEffect(() => {
        if (!authToken) {
            navigate('/auth', { state: { nextPathname: '/transfer' } });
        }
    }, [authToken, navigate]);

    // Get user accounts
    useEffect(()=>{
        const getUserData = async () => {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/accounts/`,{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`
                }
            })
            const data = await response.json()
            setAllAccounts(data)
            if (data.length > 0) {
                const defaultAccount = data.find(acc => acc.account_type === 'DEBIT') || data[0];
                setfromAccountNumber(defaultAccount.account_number); // Use account_number
            }
        }
        getUserData()
    }, [])

    const handleTransfer = async (e) => {
        e.preventDefault(); // Prevent page refresh on submit (default browser behaviour)
        setError(null);
        setSuccessMessage('');

        if (!fromAccountNumber || !toAccountNumber || !amount) {
            setError("Please fill in all required fields.");
            return;
        }
        if (parseFloat(amount) <= 0) {
            setError("Amount must be greater than zero.");
            return;
        }
        if (fromAccountNumber === toAccountNumber) {
            const selectedFromAcc = allAccounts.find(acc => acc.id === fromAccountNumber);
            if (selectedFromAcc && selectedFromAcc.account_number === toAccountNumber) {
                 setError("Cannot transfer funds to the same account.");
                 return;
            }
        }
        
        // Ensure the amount is a number
        const transferAmount = parseFloat(amount);
        if (isNaN(transferAmount)) {
            setError("Invalid amount entered.");
            return;
        }

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/transactions/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({
                    title: title,
                    send_from: fromAccountNumber,
                    send_to: toAccountNumber,
                    amount: transferAmount,
                    message: description
                })
            });

            const data = await response.json();

            if (!response.ok) {
                const errorMessage = data.detail || data.error || "Transfer failed. Please check your details.";
                throw new Error(errorMessage);
            }

            setSuccessMessage("Funds transferred successfully!");
            setfromAccountNumber(allAccounts.length > 0 ? (allAccounts.find(acc => acc.account_type === 'DEBIT') || allAccounts[0]).id : '');
            setToAccountNumber('');
            setAmount('');
            setDescription('');

            navigate('/home'); 

        } catch (err) {
            console.error("Transfer error:", err);
            setError(err.message || "An unexpected error occurred during transfer.");
        }
    };

    if (error && !allAccounts.length) {
        return <div className="transfer-funds-container error-message">{error}</div>;
    }

    return (
        <div className="transfer-funds-container">
            <header className="transfer-funds-header">
                <h1>Transfer Funds</h1>
            </header>

            <form onSubmit={handleTransfer} className="transfer-form">
                {error && <p className="error-message">{error}</p>}
                {successMessage && <p className="success-message">{successMessage}</p>}

                <div className="form-group">
                    <label htmlFor="fromAccount">From Account:</label>
                    {allAccounts.length > 0 ? (
                        <select
                            id="fromAccount"
                            value={fromAccountNumber}
                            onChange={(e) => setfromAccountNumber(e.target.value)}
                            required
                        >
                            {allAccounts.map(account => (
                                <option key={account.id} value={account.account_number}>
                                    {account.account_type} - {account.account_number} (Balance: ${account.balance})
                                </option>
                            ))}
                        </select>
                    ) : (
                        <p>No accounts available to transfer from.</p>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="toAccountNumber">To Account Number:</label>
                    <input
                        type="text"
                        id="toAccountNumber"
                        value={toAccountNumber}
                        onChange={(e) => setToAccountNumber(e.target.value)}
                        placeholder="Enter destination account number"
                        required
                    />
                </div>
                
                <div className="form-group">
                    <label htmlFor="title">Transaction title:</label>
                    <input
                        type="text"
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="Enter title (required)"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="amount">Amount ($):</label>
                    <input
                        type="number"
                        id="amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        placeholder="0.00"
                        step="0.01"
                        min="0.01"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description (Optional):</label>
                    <textarea
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="E.g., Rent, Groceries, etc."
                        rows="3"
                    ></textarea>
                </div>

                <div className="form-actions">
                    <button type="submit" className="submit-button">Submit</button>
                    <button type="button" onClick={() => navigate('/home', {state: {email: email}})} className="cancel-button">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
}