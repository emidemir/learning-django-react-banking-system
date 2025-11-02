import React from 'react';
import { Link } from 'react-router-dom';
import '../css/HomePage.css';

export default function HomePage() {
    // Dummy data for demonstration
    const userName = "Jane Doe";
    const accountNumber = "XXXX-XXXX-1234";
    const currentBalance = 12500.50;
    const accountType = "Savings";

    const recentTransactions = [
        { id: 1, description: "Amazon.com", amount: -45.99, type: "debit", date: "2023-10-26" },
        { id: 2, description: "Salary Deposit", amount: 2500.00, type: "credit", date: "2023-10-25" },
        { id: 3, description: "Starbucks Coffee", amount: -5.75, type: "debit", date: "2023-10-24" },
        { id: 4, description: "Utility Bill", amount: -78.20, type: "debit", date: "2023-10-23" },
    ];

    return (
        <div className="home-container">
            <header className="home-header">
                <h1>My Bank</h1>
                <p className="user-greeting">Welcome back, {userName}!</p>
            </header>

            <div className="main-content">
                <section className="account-summary">
                    <h2>Account Overview</h2>
                    <p className="account-balance">${currentBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <div className="account-details">
                        <p>Account Number: <span>{accountNumber}</span></p>
                        <p>Account Type: <span>{accountType}</span></p>
                        {/* More details can be added here, e.g., interest rate, branch */}
                    </div>
                </section>

                <aside className="quick-actions">
                    <h2>Quick Actions</h2>
                    <div className="action-buttons">
                        <Link to="/transfer" className="action-button">Transfer Funds</Link>
                        <Link to="/paybills" className="action-button">Other Accounts</Link>
                        <Link to="/paybills" className="action-button">Profile</Link>
                        <Link to="/statements" className="action-button">Log Out</Link>
                    </div>
                </aside>

                <section className="recent-transactions">
                    <h2>Recent Transactions</h2>
                    <ul className="transactions-list">
                        {recentTransactions.map(transaction => (
                            <li key={transaction.id}>
                                <div>
                                    <span className="transaction-description">{transaction.description}</span>
                                    <br />
                                    <small>{transaction.date}</small>
                                </div>
                                <span className={`transaction-amount ${transaction.type}`}>
                                    {transaction.type === 'credit' ? '+' : '-'}
                                    ${Math.abs(transaction.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                                </span>
                            </li>
                        ))}
                    </ul>
                    {/* Link to full transaction history */}
                    <p style={{ textAlign: 'right', marginTop: '20px' }}>
                        <Link to="/transactions" style={{ color: '#007bff', textDecoration: 'none' }}>View All Transactions</Link>
                    </p>
                </section>
            </div>
        </div>
    );
}