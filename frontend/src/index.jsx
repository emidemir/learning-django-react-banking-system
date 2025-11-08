import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google';

import App from './App';
import AuthPage from './pages/AuthPage'
import Home from './pages/Home'
import EmailVerificationPage from './pages/EmailVerificationPage';

const root = ReactDOM.createRoot(document.getElementById('root'));

const router = createBrowserRouter([
  {path:'/', element: <App/>},
  {path:'/auth', element:<AuthPage/>},
  {path:'/home', element:<Home/>},
  {path:'/verification', element:<EmailVerificationPage/>}
])

root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_OAUTH_CLIENT_ID}>
      <RouterProvider router={router}/>
    </GoogleOAuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
