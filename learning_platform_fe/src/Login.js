import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { jwtDecode } from 'jwt-decode';

const Login = () => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const login = async (username, password) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/users/login/`;
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('jwt', data.access);
            const decodedToken = jwtDecode(data.access); // Decode JWT
            navigate('/courses');
        } else {
            toast(data.errors[0].detail);
        }
    } catch (error) {
        toast('Failed to process login');
    }
  };

  const register = async (username, password, email) => {
      if (password.length < 8) {
          toast('Password must be at least 8 characters long.', { type: 'error' });
          return;
      }
      if (password !== confirmPassword) {
          toast("Passwords don't match", { type: 'error' });
          return;
      }

      const apiUrl = `${process.env.REACT_APP_API_URL}/users/public-register/`;
      try {
          const response = await fetch(apiUrl, {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ username, password, email })
          });
          const data = await response.json();
          if (data.ok) {
              localStorage.setItem('jwt', data.user.tokens.access);
              navigate('/courses');
          } else {
            Object.keys(data.errors).forEach((field) => {
              data.errors[field].forEach((message) => {
                  toast(`${message}`, { type: 'error' });
              });
          });
          }
      } catch (error) {
          toast('Failed to process registration');
      }
  };

  const handleLogin = async (event) => {
      event.preventDefault();
      if (isRegistering) {
          await register(username, password, email);
      } else {
          await login(username, password);
      }
  };

  const toggleForm = () => {
    setIsRegistering(!isRegistering);
  };

  const anonymous = () =>{
    navigate('/courses');
  }

  return (
    <div style={styles.container}>
      <form onSubmit={handleLogin} style={styles.form}>
        <h2>{isRegistering ? 'Register' : 'Login'}</h2>
        <div style={styles.inputGroup}>
          <label htmlFor="username" style={styles.label}>Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={styles.input}
          />
        </div>
        {isRegistering && (
          <div style={styles.inputGroup}>
            <label htmlFor="email" style={styles.label}>Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              style={styles.input}
            />
          </div>
        )}
        <div style={styles.inputGroup}>
          <label htmlFor="password" style={styles.label}>Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={styles.input}
          />
        </div>
        {isRegistering && (
          <div style={styles.inputGroup}>
            <label htmlFor="confirmPassword" style={styles.label}>Confirm Password:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              style={styles.input}
            />
          </div>
        )}
        <button type="submit" style={styles.button}>
          {isRegistering ? 'Register' : 'Log In'}
        </button>
        <button type="button" onClick={toggleForm} style={styles.button}>
          {isRegistering ? 'Switch to Login' : 'Switch to Register'}
        </button>
        <button type="button" onClick={anonymous} style={styles.button}>
          Continue as anonymous
        </button>
      </form>
    </div>
  );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f7f7f7',
        },
    form: {
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '5px',
        backgroundColor: 'white',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        },
    inputGroup: {
        margin: '10px 0'
        },
    label: {
        display: 'block',
        marginBottom: '5px'
        },
    input: {
        width: '200px',
        padding: '10px',
        fontSize: '16px',
        border: '1px solid #ccc',
        borderRadius: '4px'
        },
    button: {
        width: '100%',
        padding: '10px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
        marginTop: '10px'
    }
};

export default Login;
