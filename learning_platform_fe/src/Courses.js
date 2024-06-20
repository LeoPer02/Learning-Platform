import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // Import useNavigate or Link for navigation
import { toast } from 'react-toastify';

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate(); // For programmatic navigation

  useEffect(() => {
    const checkEnrollment = async () => {
      const apiUrl = `${process.env.REACT_APP_API_URL}/api/enrolled-courses`;
      const token = localStorage.getItem('jwt');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      try {
        const response = await fetch(apiUrl, { headers });
        if (response.ok) {
          const data = await response.json();
          setCourses(data.results);
          setIsLoading(false);
        } else {
          throw new Error('Failed to check enrollment status');
        }
      } catch (error) {
        console.error('Error checking enrollment:', error.message);
      }
    };

    checkEnrollment();
  }, []);

  const handleEnrollment = (id) =>{
    navigate(`../courses/${id}`);
  };

  const handleEnrollClick = () => {
    navigate('/enrollCourses');
  };

  if (isLoading) return <div>Loading...</div>;
  if (!courses) {
    return (
      <div>
        <p>You are not enrolled in any courses.</p>
        <button onClick={() => navigate('/enrollCourses')}>Enroll in Courses</button>
      </div>
    );
  }
    if (courses.length === 0) {
    return (
      <div>
        <p>You haven't enrolled in a course. Consider enrolling in one!</p>
        <button onClick={handleEnrollClick}>Enroll in a Course</button>
      </div>
    );
  }

  return (
    <div style={styles.grid}>
      {courses.map(course => (
        <div key={course.id} style={styles.card}>
          <h3>{course.title}</h3>
          <p>Enrolled Users: {course.enrolled_users.length}</p>
          <button onClick={() => handleEnrollment(course.id)} style={styles.button}>Enter course</button>
        </div>
      ))}
    </div>
  );
};

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)', // Three columns layout
    gap: '20px',
    padding: '20px'
  },
  card: {
    cursor: 'pointer',
    border: '1px solid #ccc',
    borderRadius: '10px',
    padding: '20px',
    textAlign: 'center',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
  },
  button: {
    marginTop: '10px',
    padding: '10px 15px',
    fontSize: '16px',
    color: 'white',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
  }
};

export default Courses;
