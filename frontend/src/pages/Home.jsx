import { React, useState, useEffect } from 'react';
import { Link, useLocation, useNavigate} from 'react-router-dom';
import '../css/HomePage.css';

import Transactions from '../components/Transactions'

export default function HomePage() {
    const navigate = useNavigate();

    // States
    const [userName, setUserName] = useState();
    const [email, setEmail] = useState();
    const [accountNumber, setAccountNumber] = useState();
    const [accountType, setAccountType] = useState();
    const [currentBalance, setCurrentBalance] = useState(0);
    const [recentTransactions, setRecentTransactions] = useState([]);
    const [avatar, setAvatar] = useState();
    const [phoneNumber, setPhoneNumber] = useState();
    const [birthDate, setBirthDate] = useState();
    const [allAccounts, setAllAccounts] = useState([]);
    const [selectedAccountId, setSelectedAccountId] = useState(null);

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

                const user_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/users/`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${authToken}`
                    }
                })

                const user_data = await user_response.json()
                setEmail(user_data.email)

                // Don't use state email because of asynrnonus nature of the operations. Use user_data.email instead
                const profile_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/profiles/${user_data.email}/`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${authToken}`
                    }
                });

                const accounts_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/accounts/`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${authToken}`
                    }
                })

                if (!profile_response.ok || !accounts_response.ok){
                    console.log(`Profile status: ${profile_response.status}\n`)
                    console.log(`Accounts status: ${accounts_response.status}\n`)
                }
    
                const profile_data = await profile_response.json()
                const accounts_data = await accounts_response.json()

                setAvatar(profile_data.avatar)
                setPhoneNumber(profile_data.phone_number)
                setBirthDate(profile_data.date_of_birth)

                if (accounts_data && accounts_data.length > 0){
                    setAllAccounts(accounts_data); // Store all accounts
                    
                    const initialAccount = accounts_data.find((acc) => acc.account_type === "DEBIT") || accounts_data[0];
                    if (initialAccount) {
                        setSelectedAccountId(initialAccount.id); // Assuming accounts have an 'id'
                    }
                }
                setUserName(profile_data.user.username)        
            } catch (error) {
                console.log(error)            
            }
        }
        fetchUserProfile()
    }, [authToken])

    // ----- Fetch account transactions -----
    useEffect(() => {
        const updateAccountAndTransactions = async () => {
            if (!authToken || !selectedAccountId) return;

            const account = allAccounts.find(acc => acc.id === selectedAccountId);
            if (account) {
                setAccountNumber(account.account_number);
                setAccountType(account.account_type);
                setCurrentBalance(account.balance);
                
                try {
                    const transactions_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/transactions/?account_id=${selectedAccountId}`, {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${authToken}`
                        }
                    });

                    if (!transactions_response.ok) {
                        console.error(`Transactions status for account ${selectedAccountId}: ${transactions_response.status}`);
                        setRecentTransactions([]);
                        return;
                    }

                    const transactions_data = await transactions_response.json();
                    setRecentTransactions(transactions_data["results"] || []);
                } catch (error) {
                    console.error(`Error fetching transactions for account ${selectedAccountId}:`, error);
                    setRecentTransactions([]);
                }
            }
        };

        updateAccountAndTransactions();
    }, [selectedAccountId, authToken, allAccounts]);

    const handleLogOut = async () => {
        try {
            // Call the backend logout endpoint
            await fetch(`${process.env.REACT_APP_BACKEND_URL}/logout/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`
                }
            });
    
            // Clear the auth token from localStorage
            localStorage.removeItem('authToken');
            
            // Redirect to login page
            navigate('/auth');
        } catch (error) {
            console.error('Logout error:', error);
            localStorage.removeItem('authToken');
            navigate('/auth');
        }
    }

    const handleAccountChange = (event) => {
        setSelectedAccountId(parseInt(event.target.value)); // Convert value to integer ID
    };
    
    return (
        <div className="home-container">
            <header className="home-header">
                <h1>My Bank</h1>
                <p className="user-greeting">Welcome back, {userName}!</p>
            </header>

            <div className="main-content">
                <section className="account-summary">
                    <h2>Account Overview</h2>
                    {allAccounts.length > 1 && ( // Only show dropdown if user has more than one account
                        <div className="account-selector">
                            <label htmlFor="account-select">Select Account:</label>
                            <select 
                                id="account-select" 
                                value={selectedAccountId || ''} 
                                onChange={handleAccountChange}
                            >
                                {allAccounts.map(account => (
                                    <option key={account.id} value={account.id}>
                                        {account.account_type} - {account.account_number}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}

                    <p className="account-balance">${currentBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    <div className="account-details">
                        <p>Account Number: <span>{accountNumber}</span></p>
                        <p>Account Type: <span>{accountType}</span></p>
                    </div>
                </section>

                <aside className="quick-actions">
                    <h2>Quick Actions</h2>
                    <div className="action-buttons">
                        <Link to="/transfer" state={{allAccounts}} email={{email}} className="action-button">Transfer Funds</Link>
                        <Link to="/profile" state={{userName, email, avatar, phoneNumber, birthDate}} className="action-button">Profile</Link>
                        <button onClick={handleLogOut} className="action-button">Log Out</button> {/* Changed to button for consistency */}
                    </div>
                </aside>

                {/* MODIFIED: Pass selectedAccountId to Transactions component if needed for further filtering/display */}
                <Transactions transactions={recentTransactions} isAll={false} selectedAccountId={selectedAccountId} />
            </div>
        </div>
    );
}