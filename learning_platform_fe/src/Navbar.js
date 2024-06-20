import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { useNavigate, useLocation } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import Modal from 'react-modal';
import { toast } from 'react-toastify';

const Navbar = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('');
  const [visibility, setVisibility] = useState('private');
  const [isLoggedIn, setisLoggedIn] = useState('false');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (token) {
      const decodedToken = jwtDecode(token);
      setisLoggedIn(true);
      if (decodedToken && decodedToken.is_admin) {
        setIsAdmin(true);
      }
    }else{
      setisLoggedIn(false);
    }
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem('jwt');
    setIsAdmin(false);
    navigate('/login');
  };

  const clearCourseCreate = () =>{
    setTitle('');
    setVisibility('private');
  };

  const handleCreateCourse = async () => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/courses/`;
    const body = { title, visibility };

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('jwt')}`
        },
        body: JSON.stringify(body)
      });

      if (response.ok) {
        const data = await response.json();
        toast.success('Course created successfully');
        console.log('Created course:', data);
        setShowModal(false);
        clearCourseCreate();
        navigate(`/courses/${data.id}`);
      } else {
        const errorData = await response.json();
        toast.error(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Error creating course:', error);
      toast.error('Error creating course');
    }
  };

  const gotoLogin = () =>{
    navigate('/login');
  }
  return (
    <div style={styles.navbar}>
      <NavLink to="/" style={styles.link}>Home</NavLink>
      <NavLink to="/courses" style={styles.link} >My courses</NavLink>
      <NavLink to="/enrollCourses" style={styles.link} >All courses</NavLink>
      {isAdmin && <button onClick={() => setShowModal(true)} style={styles.button}>Create Course</button>}
      {isLoggedIn && <button onClick={handleLogout} style={styles.button}>Logout</button>}
      {!isLoggedIn && location.pathname !== '/login' && <button onClick={gotoLogin} style={styles.button}>Login</button>}
      {showModal && isAdmin && (
        <Modal
        isOpen={showModal}
        onRequestClose={() => setShowModal(false)}
        contentLabel="Create Course"
        style={modalStyles}
      >
        <h2>Create Course</h2>
        <div>
          <input 
            type="text" 
            placeholder="Course Title" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            style={styles.input} 
          />
        </div>
        <div>
          <select 
            value={visibility} 
            onChange={(e) => setVisibility(e.target.value)} 
            style={styles.input}
          >
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
       
        <button onClick={handleCreateCourse} style={styles.button}>Create</button>
        <button onClick={() => setShowModal(false)} style={styles.cancelButton}>Cancel</button>
      </Modal>
      )}
    </div>
  );
};

const styles = {
  navbar: {
    padding: '10px 30px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    backgroundColor: '#f0f0f0',
    height: '100vh',
    width: '200px'
  },
  link: {
    textDecoration: 'none',
    color: 'blue',
    fontSize: '18px',
    padding: '8px 0'
  },
  activeLink: {
    color: 'red'
  },
  button: {
    padding: '10px 20px',
    margin: '5px 0',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
  },
  input: {
    margin: '10px 0',
    padding: '10px',
    fontSize: '16px',
    width: '100%'
  },
  cancelButton: {
    padding: '10px 20px',
    margin: '5px 0',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#dc3545',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
  }
};

const modalStyles = {
  content: {
    width: '500px',
    height: '300px',
    margin: 'auto',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
  }
};
export default Navbar;
