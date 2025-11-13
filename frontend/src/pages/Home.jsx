import { React, useState, useEffect } from 'react';
import { Link, useLocation, useNavigate} from 'react-router-dom';
import '../css/HomePage.css';

import Transactions from '../components/Transactions'

export default function HomePage() {
    const {state} = useLocation()
    const navigate = useNavigate();

    // Email is passed down from the AuthPage for data retrieval
    const { email } = state
    
    // States
    const [userName, setUserName] = useState();
    const [accountNumber, setAccountNumber] = useState();
    const [accountType, setAccountType] = useState();
    const [currentBalance, setCurrentBalance] = useState(0);
    const [recentTransactions, setRecentTransactions] = useState([]);
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
                const profile_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/profiles/${email}/`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${authToken}`
                    }
                });

                const transactions_response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/transactions/`, {
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

                if (!profile_response.ok || !transactions_response.ok || !accounts_response.ok){
                    console.log(`Profile status: ${profile_response.status}\n`)
                    console.log(`Transactions status: ${transactions_response.status}\n`)
                    console.log(`Accounts status: ${accounts_response.status}\n`)
                }
    
                const profile_data = await profile_response.json()
                const transactions_data = await transactions_response.json()
                const accounts_data = await accounts_response.json()

                setAvatar(profile_data.avatar)
                setPhoneNumber(profile_data.phone_number)
                setBirthDate(profile_data.date_of_birth)

                if (accounts_data){
                    const baseAccount = accounts_data.filter((acc) => acc.account_type === "DEBIT")[0]
                    setAccountNumber(baseAccount.account_number)
                    setAccountType(baseAccount.account_type)
                    setCurrentBalance(baseAccount.balance)
                }
                setRecentTransactions(transactions_data)
        
                setUserName(profile_data.user.username)        
            } catch (error) {
                console.log(error)            
            }
        }
        fetchUserProfile()
    }, [authToken])
    
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
                    </div>
                </section>

                <aside className="quick-actions">
                    <h2>Quick Actions</h2>
                    <div className="action-buttons">
                        {/* https://stackoverflow.com/questions/30115324/pass-props-in-link-react-router */}
                        <Link to="/transfer" className="action-button">Transfer Funds</Link>
                        <Link to="/other-accounts" className="action-button">Other Accounts</Link>
                        <Link to="/profile" state={{userName, email, avatar, phoneNumber, birthDate}} className="action-button">Profile</Link>
                        <Link to="/logout" className="action-button">Log Out</Link>
                    </div>
                </aside>

                <Transactions transactions={recentTransactions}/>
            </div>
        </div>
    );
}