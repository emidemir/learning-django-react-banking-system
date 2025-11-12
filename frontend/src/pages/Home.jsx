import { React, useState, useEffect } from 'react';
import { Link, useLocation, useNavigate} from 'react-router-dom';
import '../css/HomePage.css';

export default function HomePage() {
    const location = useLocation()
    const navigate = useNavigate();

    // Email is passed down from the AuthPage for data retrieval
    const { email } = location
    
    // States
    const [profileObject, setProfileObject] = useState();
    const [userName, setUserName] = useState();
    const [accountNumber, setAccountNumber] = useState();
    const [accountType, setAccountType] = useState();
    const [currentBalance, setCurrentBalance] = useState();
    const [recentTransactions, setRecentTransactions] = useState();
    const [avatar, setAvatar] = useState();
    const [phoneNumber, setPhoneNumber] = useState();
    const [birthDate, setBirthDate] = useState();

   
    const authToken = localStorage.getItem('authToken')

    // ----- Redirect unauthorized users to login -----
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

    // ----- Data fetch -----
    useEffect(()=>{
        const fetchUserProfile = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/profiles/${email}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${authToken}`
                    }
                });
    
                if (!response.ok){
                    // Error if response status is not ok
                }
    
                const data = await response.json()
                console.log(data)
                setAvatar(data.avatar)
                setPhoneNumber(data.phone_number)
                setBirthDate(data.date_of_birth)

                const baseAccount = data.accounts.filter((acc) => acc.type = "DEBIT")[0]
                setAccountNumber(baseAccount.account_number)
                setAccountType(baseAccount.account_type)
                setCurrentBalance(baseAccount.balance)
                setRecentTransactions(baseAccount.transactions)
                setUserName(data.user.username)
                
            } catch (error) {
                console.log(error)            
            }
    
        }

        fetchUserProfile()
    }, [authToken, email])
    
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
                        {/* https://stackoverflow.com/questions/30115324/pass-props-in-link-react-router */}
                        <Link to="/transfer" className="action-button">Transfer Funds</Link>
                        <Link to="/other-accounts" className="action-button">Other Accounts</Link>
                        <Link to="/profile" className="action-button">Profile</Link>
                        <Link to="/logout" className="action-button">Log Out</Link>
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