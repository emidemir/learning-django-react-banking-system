import { useEffect, useState } from 'react'
import Tranactions from '../components/Transactions'

export default function ViewAllTransactions(){
    const authToken = localStorage.getItem('authToken');

    const [transactionHistory, setTransactionHistory] = useState()
    
    useEffect(()=> {
        const fetchAllTransactions = async () => {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/transactions/?page_size=13`,{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`
                }
            })
    
            const data = await response.json()
            setTransactionHistory(data["results"])
        }
        fetchAllTransactions()
    }, [])

    return (
        <Tranactions transactions={transactionHistory} isAll={true}/>
    )
}