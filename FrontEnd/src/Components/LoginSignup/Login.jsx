import React, { useState } from "react";

export default function Login(props) {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [emailError, setEmailError] = useState(''); 
    const [loginError, setLoginError] = useState('');

    const isValidEmail = (email) => {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    };

const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isValidEmail(email)) {
        setEmailError('Please enter a valid email address.');
        return;
    }
    
    setEmailError('');
    setLoginError('');

    try {
        const response = await fetch('http://127.0.0.1:3000/login', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password: pass }),
        });

        const data = response.headers.get('Content-Type').includes('application/json') 
                ? await response.json() 
                : null;

        if (response.ok) {
            props.onLoginSuccess();
        } else {
            if (response.status === 400 || (data && data.message === 'Missing email or password')) {
                setLoginError('Missing email or password');
            } else if (response.status === 404 || (data && data.message === 'User does not exist')) {
                setLoginError('User does not exist');
            } else if (response.status === 401 || (data && data.message === 'Password is incorrect')) {
                setLoginError('Password is incorrect');
            } else {
                setLoginError('An error occurred during login');
            }
        }
    } catch (error) {
        console.error('Login failed:', error);
        setLoginError('An error occurred. Please try again later.');
    }
};

    const handleEmailBlur = () => {
        if (!isValidEmail(email)) {
            setEmailError('Please enter a valid email address.');
        } else {
            setEmailError('');
        }
    };

    return (
        <div className="auth-form-container">
            <h2>Login</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="Email">Email</label>
                <input 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}
                    onBlur={handleEmailBlur} 
                    type="email" 
                    placeholder="youremail@gmail.com" 
                    id="email" 
                    name="email" 
                />
                {emailError && <div style={{color: 'red'}}>{emailError}</div>}
                <div className="password-container">
                    <label htmlFor="password">Password</label>
                    <input 
                        value={pass} 
                        onChange={(e) => setPass(e.target.value)} 
                        type={showPassword ? "text" : "password"} 
                        placeholder="********" 
                        id="password" 
                    />
                    <span className="toggle-password" onClick={() => setShowPassword(!showPassword)}>
                        {showPassword ? "Hide" : "Show"}
                    </span>
                </div>
                {loginError && <div style={{color: 'red'}}>{loginError}</div>}
                <button type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('register')}>Don't have an account? Register here.</button>
        </div>
    );
    
};