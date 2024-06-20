import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const EnrollmentRequests = () => {
    const { courseId } = useParams(); // Assuming you're using React Router and courseId is the URL parameter
    const [enrollmentRequests, setEnrollmentRequests] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchEnrollmentRequests = async () => {
            const apiUrl = `${process.env.REACT_APP_API_URL}/courses/${courseId}/enrollment-requests`;
            try {
                const response = await fetch(apiUrl, {
                    headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt')}` }
                });
                const data = await response.json();
                if (response.ok) {
                    setEnrollmentRequests(data);
                } else {
                    // Handle errors here, for example using a toast notificatio
                    console.error('Failed to fetch enrollment requests', data);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
            setIsLoading(false);
        };

        fetchEnrollmentRequests();
    }, [courseId]);

    if (isLoading) return <div>Loading...</div>;
    if (!enrollmentRequests.length) return <div>No enrollment requests found.</div>;

    return (
        <div>
            <h1>Enrollment Requests</h1>
            <ul>
                {enrollmentRequests.map(request => (
                    <li key={request.id}>
                        {request.user.username} - Status: {request.status}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default EnrollmentRequests;
