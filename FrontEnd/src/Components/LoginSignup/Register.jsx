import React, { useState } from "react";

export default function Register(props) {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const [confirmPass, setConfirmPass] = useState('');
    const [name, setName] = useState('');
    const [errors, setErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [emailError, setEmailError] = useState(''); 

    const isValidEmail = email => {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    const handleEmailBlur = () => {
        if (!isValidEmail(email)) {
            setEmailError('Please enter a valid email address.');
        } else {
            setEmailError('');
        }
    };

    const validateInputs = () => {
        const newErrors = {};
        if (!name.trim()) newErrors.name = 'Username is required';
        if (!email.trim()) {
            newErrors.email = 'Email is required';
        } else if (!isValidEmail(email)) {
            newErrors.email = 'Provide a valid email address';
        }
        if (!pass.trim()) {
            newErrors.pass = 'Password is required';
        } else if (pass.length < 8) {
            newErrors.pass = 'Password must be at least 8 characters';
        }
        if (pass !== confirmPass) {
            newErrors.confirmPass = "Passwords don't match";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (validateInputs()) {
            try {
                const response = await fetch('http://127.0.0.1:3000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: pass,
                        name: name,
                    }),
                });
    
    
                const data = response.headers.get('Content-Type').includes('application/json') 
                                ? await response.json() 
                                : null;

                if (!response.ok) {
                    if (response.status === 400 || (data && data.message === 'Email already registered')) {
                        setEmailError('This email is already registered.');
                    } else {
                        setEmailError('An error occurred. Please try again.');
                    }
                } else {
                    props.onRegistrationSuccess();
                }
            } catch (error) {
                console.error('Failed to register:', error);
            }
        } else {
            console.log('Form is invalid');
        }
    };

    return (
        <div className="auth-form-container">
            <h2>Register</h2>
            <form className="register-form" onSubmit={handleSubmit}>
                <label htmlFor="name">Full name</label>
                <input value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    id="name" 
                    placeholder="Full Name" 
                />
                {errors.name && <div style={{color: 'red'}}>{errors.name}</div>}
                
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
                        placeholder="At least 8 characters" 
                        id="password" 
                    />
                    <span className="toggle-password" onClick={() => setShowPassword(!showPassword)}>
                        {showPassword ? "Hide" : "Show"}
                    </span>
                </div>

                <div className="password-container">
                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input 
                        value={confirmPass} 
                        onChange={(e) => setConfirmPass(e.target.value)} 
                        type={showConfirmPassword ? "text" : "password"} 
                        placeholder="Confirm your password" 
                        id="confirmPassword" 
                    />
                    <span className="toggle-password" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                        {showConfirmPassword ? "Hide" : "Show"} 
                    </span>
                    {errors.confirmPass && <div style={{color: 'red'}}>{errors.confirmPass}</div>}
                </div>


                <button type="submit">Sign Up</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('login')}>Already have an account? Login here.</button>
        </div>
    )
}