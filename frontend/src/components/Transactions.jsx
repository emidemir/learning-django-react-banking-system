import React from 'react';
import { Link } from 'react-router-dom';
import '../css/Transactions.css'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';

export default function Transactions({ transactions }) {
    // A helper function to format the date nicely (optional)
    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <section className="transactions-card">
            <div className="transactions-header">
                <h2>Recent Transactions</h2>
                <Link to="/transactions" className="view-all-link">View All</Link>
            </div>
            
            <div className="transactions-list">
                {!transactions || transactions.length === 0 ? (
                    <p className="no-transactions-message">No recent transactions to display.</p>
                ) : (
                    transactions.map(transaction => {
                        const isCredit = transaction.type === 'credit';
                        
                        return (
                            <div key={transaction.id} className="transaction-item">
                                <div className="transaction-icon-container">
                                    <div className={`transaction-icon ${isCredit ? 'credit' : 'debit'}`}>
                                        <FontAwesomeIcon icon={isCredit ? faArrowDown : faArrowUp} />
                                    </div>
                                </div>
                                <div className="transaction-details">
                                    <span className="transaction-description">{transaction.description}</span>
                                    <span className="transaction-date">{formatDate(transaction.date)}</span>
                                </div>
                                <span className={`transaction-amount ${isCredit ? 'credit' : 'debit'}`}>
                                    {isCredit ? '+' : '-'}
                                    ${Math.abs(transaction.amount).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                                </span>
                            </div>
                        );
                    })
                )}
            </div>
        </section>
    );
}