import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import { toast } from 'react-toastify';

const CoursesToEnroll = () => {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    const fetchCourses = async () => {
    const token = localStorage.getItem('jwt');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/courses`
      try {
        const response = await fetch(apiUrl, { headers });
        if (!response.ok) {
          throw new Error('Something went wrong!');
        }
        const data = await response.json();
        console.log(data);
        setCourses(data.results);
      } catch (error) {
        toast(error.message);
      }
      setIsLoading(false);
    };

    fetchCourses();
  }, []);

  const handleEnrollment = async (courseId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/enrollment-requests/`;
    const token = localStorage.getItem('jwt');
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                course: courseId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to enroll in course');
        }

        const data = await response.json();
        toast("Enrollment Request successful")
    } catch (error) {
        console.error('Enrollment error:', error.message);
        alert('Error enrolling in course: ' + error.message);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (courses.length === 0) {
    return <div>No courses available at the time.</div>;
  }

  return (
    <div>
        <div style={styles.grid}>
        {courses.map(course => (
            <div key={course.id} style={styles.card}>
            <h3>{course.id} : {course.title}</h3>
            <p>Enrolled Users: {course.enrolled_users.length}</p>
            <button onClick={() => handleEnrollment(course.id)} style={styles.button}>Enroll in Course</button>
            </div>
        ))}
        </div>
    </div>
  );
};

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px',
    padding: '20px'
  },
  card: {
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

export default CoursesToEnroll;
