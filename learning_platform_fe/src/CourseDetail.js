import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { toast } from 'react-toastify';

const CourseDetail = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditMode, setIsEditMode] = useState(false);
  const [showTopicForm, setShowTopicForm] = useState(false);
  const [topicTitle, setTopicTitle] = useState('');
  const [topicDescription, setTopicDescription] = useState('');
  const [topicVisibility, setTopicVisibility] = useState('public');
  const [showForumForm, setShowForumForm] = useState(false);
  const [forumTitle, setForumTitle] = useState('');
  const [forumDescription, setForumDescription] = useState('');
  const [forumVisibility, setForumVisibility] = useState('public');
  const [isCourseAdmin, setCourseAdmin] = useState(false);
  const [editTopicId, setEditTopicId] = useState(null);
  const [editForumId, setEditForumId] = useState(null);
  const [activeTab, setActiveTab] = useState('content');
  const [enrollmentRequests, setEnrollmentRequests] = useState([]);

  useEffect(() => {
    const fetchCourseDetails = async () => {
      const token = localStorage.getItem('jwt');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const apiUrl = `${process.env.REACT_APP_API_URL}/api/courses/${courseId}`;
      try {
        const response = await fetch(apiUrl, { headers });
        const data = await response.json();
        if (response.ok) {
          setCourse(data);
          setCourseAdmin(data.isAdmin ? data.isAdmin : false)
          setCourseAdmin(data.is_course_admin);
          console.log(data);
        } else {
          throw new Error('Failed to fetch course details');
        }
      } catch (error) {
        toast.error(error.message);
      }
      setIsLoading(false);
    };

    fetchCourseDetails();
  }, [courseId]);

  const submitTopic = async () => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/topics/`;
    const body = { title: topicTitle, description: topicDescription, course: courseId, visibility: topicVisibility };
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('jwt')}` },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to create topic');
      toast.success('Topic created successfully');
      setShowTopicForm(false);
      setCourse(previousState => ({
        ...previousState,
        topics: [...previousState.topics, data]
      }));
    } catch (error) {
      toast.error(error.message);
    }
  };

  const updateTopic = async (topicId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/topics/${topicId}/`;
    const body = { title: topicTitle, description: topicDescription, visibility: topicVisibility };
    try {
      const response = await fetch(apiUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('jwt')}` },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to update topic');
      toast.success('Topic updated successfully');
      setCourse(previousState => ({
        ...previousState,
        topics: previousState.topics.map(topic => topic.id === topicId ? data : topic)
      }));
      setEditTopicId(null);
    } catch (error) {
      toast.error(error.message);
    }
  };

  const deleteTopic = async (topicId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/topics/${topicId}/`;
    try {
      const response = await fetch(apiUrl, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      });
      if (!response.ok) throw new Error('Failed to delete topic');
      toast.success('Topic deleted successfully');
      setCourse(previousState => ({
        ...previousState,
        topics: previousState.topics.filter(topic => topic.id !== topicId)
      }));
    } catch (error) {
      toast.error(error.message);
    }
  };

  const submitForum = async () => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/forums/`;
    const body = { title: forumTitle, description: forumDescription, course: courseId, visibility: forumVisibility };
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('jwt')}` },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to create forum');
      toast.success('Forum created successfully');
      setShowForumForm(false);
      setCourse(previousState => ({
        ...previousState,
        forums: [...previousState.forums, data]
      }));
    } catch (error) {
      toast.error(error.message);
    }
  };

  const updateForum = async (forumId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/forums/${forumId}/`;
    const body = { title: forumTitle, description: forumDescription, visibility: forumVisibility };
    try {
      const response = await fetch(apiUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('jwt')}` },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to update forum');
      toast.success('Forum updated successfully');
      setCourse(previousState => ({
        ...previousState,
        forums: previousState.forums.map(forum => forum.id === forumId ? data : forum)
      }));
      setEditForumId(null);
    } catch (error) {
      toast.error(error.message);
    }
  };

  const deleteForum = async (forumId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/forums/${forumId}/`;
    try {
      const response = await fetch(apiUrl, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      });
      if (!response.ok) throw new Error('Failed to delete forum');
      toast.success('Forum deleted successfully');
      setCourse(previousState => ({
        ...previousState,
        forums: previousState.forums.filter(forum => forum.id !== forumId)
      }));
    } catch (error) {
      toast.error(error.message);
    }
  };

  const fetchEnrollmentRequests = async () => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/courses/${courseId}/enrollment-requests/`;
    try {
      const response = await fetch(apiUrl, {
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      });
      const data = await response.json();
      if (response.ok) {
        setEnrollmentRequests(data.results);
      } else {
        //throw new Error('Failed to fetch enrollment requests');
      }
    } catch (error) {
      //toast.error(error.message);
    }
  };

  const updateEnrollmentRequest = async (id, status) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/enrollment-requests/${id}/`;
    try {
        const response = await fetch(apiUrl, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('jwt')}`
            },
            body: JSON.stringify({ status })
        });
        const data = await response.json();
        if (response.ok) {
            toast.success(`Enrollment request ${status}`);
            setEnrollmentRequests(prev => prev.map(request => 
                request.id === id ? { ...request, status, updated_at: data.updated_at } : request
            ));
        } else {
            throw new Error(data.detail || 'Failed to update enrollment request');
        }
    } catch (error) {
        toast.error(error.message);
    }
};

  useEffect(() => {
    if (activeTab === 'members' && isCourseAdmin) {
      fetchEnrollmentRequests();
    }
  }, [activeTab]);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const pendingRequests = enrollmentRequests.filter(request => request.status === 'pending');
  const handledRequests = enrollmentRequests.filter(request => request.status !== 'pending');
  if (isLoading) return <div>Loading course details...</div>;
  if (!course) return <div>No course details found.</div>;

  const handleMakeCourseAdmin = async (userId) => {
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/courseadmins/`;
    const body = {
      user: userId,
      course: courseId
    };
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
        toast.success('User promoted to course admin successfully');
      } else {
        const errorData = await response.json();
        toast.error(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Error making course admin:', error);
      toast.error('Error making course admin');
    }
  };

  return (
    <div>
      <h1>{course?.title || "Loading course details..."}</h1>
      <div>
        <button onClick={() => handleTabChange('content')} style={styles.tabButton}>Content</button>
        <button onClick={() => handleTabChange('members')} style={styles.tabButton}>Members</button>
      </div>

      {activeTab === 'content' && (
        <>
          {isEditMode && isCourseAdmin && (
            <>
              <button onClick={() => {setShowTopicForm(true); setIsEditMode(true);}} style={styles.button}>Add Topic</button>
              <button onClick={() => {setShowForumForm(true); setIsEditMode(true);}} style={styles.button}>Add Forum</button>
            </>
          )}
          <h2>Topics</h2>
          {course?.topics && course.topics.length > 0 ? (
            <div style={styles.itemContainer}>
              {course.topics.map(topic => (
                <div key={topic.id} style={styles.item}>
                  {editTopicId === topic.id && isCourseAdmin ? (
                    <div style={styles.form}>
                      <input 
                        placeholder="Title" 
                        value={topicTitle} 
                        onChange={(e) => setTopicTitle(e.target.value)} 
                        style={styles.input}
                      />
                      <textarea 
                        placeholder="Description" 
                        value={topicDescription} 
                        onChange={(e) => setTopicDescription(e.target.value)} 
                        style={styles.input}
                      />
                      <select 
                        value={topicVisibility} 
                        onChange={(e) => setTopicVisibility(e.target.value)} 
                        style={styles.input}
                      >
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                      </select>
                      <button onClick={() => updateTopic(topic.id)} style={styles.button}>Submit Topic</button>
                      <button onClick={() => setEditTopicId(null)} style={styles.cancelButton}>Cancel</button>
                    </div>
                  ) : (
                    <>
                      <div style={styles.topicContainer}>
                        <h3 style={styles.title}>{topic.title}</h3>
                        <p style={styles.description}>&nbsp;&nbsp;&nbsp;&nbsp;{topic.description}</p>
                      </div>

                      {isEditMode && isCourseAdmin && (
                        <div style={styles.editButtonContainer}>
                          <button 
                            onClick={() => {
                              setEditTopicId(topic.id);
                              setTopicTitle(topic.title);
                              setTopicDescription(topic.description);
                            }} 
                            style={styles.button}
                          >
                            Edit
                          </button>
                          <button 
                            onClick={() => deleteTopic(topic.id)} 
                            style={styles.deleteButton}
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </>
                  )}
                </div>
              ))}

            </div>
          ) : <p>No topics available.</p>}
              {showTopicForm && isEditMode && isCourseAdmin && (
                <div style={styles.form}>
                  <input 
                    placeholder="Title" 
                    value={topicTitle} 
                    onChange={(e) => setTopicTitle(e.target.value)} 
                    style={styles.input}
                  />
                  <textarea 
                    placeholder="Description" 
                    value={topicDescription} 
                    onChange={(e) => setTopicDescription(e.target.value)} 
                    style={styles.input}
                  />
                  <select 
                    value={topicVisibility} 
                    onChange={(e) => setTopicVisibility(e.target.value)} 
                    style={styles.input}
                  >
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                  </select>
                  <button onClick={submitTopic} style={styles.button}>Submit Topic</button>
                </div>
              )}
          <h2>Forums</h2>
          {course?.forums && course.forums.length > 0 ? (
            <div style={styles.itemContainer}>
              {course.forums.map(forum => (
                <div key={forum.id} style={styles.item}>
                  {editForumId === forum.id && isCourseAdmin ? (
                    <div style={styles.form}>
                      <input 
                        placeholder="Title" 
                        value={forumTitle} 
                        onChange={(e) => setForumTitle(e.target.value)} 
                        style={styles.input}
                      />
                      <textarea 
                        placeholder="Description" 
                        value={forumDescription} 
                        onChange={(e) => setForumDescription(e.target.value)} 
                        style={styles.input}
                      />
                      <select 
                        value={forumVisibility} 
                        onChange={(e) => setForumVisibility(e.target.value)} 
                        style={styles.input}
                      >
                        <option value="public">Public</option>
                        <option value="private">Private</option>
                      </select>
                      <button onClick={() => updateForum(forum.id)} style={styles.button}>Submit Forum</button>
                      <button onClick={() => setEditForumId(null)} style={styles.cancelButton}>Cancel</button>
                    </div>
                  ) : (
                    <>
                      <div style={styles.topicContainer}>
                        <Link to={`/forums/${forum.id}`} key={forum.id} style={styles.link}><div style={styles.title}>{forum.title}</div><br /></Link>
                        <div style={styles.description}>&nbsp;&nbsp;&nbsp;&nbsp;{forum.description}</div>
                      </div>

                      {isEditMode && isCourseAdmin && (
                        <div style={styles.editButtonContainer}>
                          <button 
                            onClick={() => {
                              setEditForumId(forum.id);
                              setForumTitle(forum.title);
                              setForumDescription(forum.description);
                            }} 
                            style={styles.button}
                          >
                            Edit
                          </button>
                          <button 
                            onClick={() => deleteForum(forum.id)} 
                            style={styles.deleteButton}
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </>
                  )}
                </div>
              ))}

            </div>
          ) : <p>No forums available.</p>}
              {showForumForm && isEditMode && isCourseAdmin && (
                <div style={styles.form}>
                  <input 
                    placeholder="Title" 
                    value={forumTitle} 
                    onChange={(e) => setForumTitle(e.target.value)} 
                    style={styles.input}
                  />
                  <textarea 
                    placeholder="Description" 
                    value={forumDescription} 
                    onChange={(e) => setForumDescription(e.target.value)} 
                    style={styles.input}
                  />
                  <select 
                    value={forumVisibility} 
                    onChange={(e) => setForumVisibility(e.target.value)} 
                    style={styles.input}
                  >
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                  </select>
                  <button onClick={submitForum} style={styles.button}>Submit Forum</button>
                </div>
              )}
          {isCourseAdmin && (
            <button onClick={() => setIsEditMode(!isEditMode)} style={styles.button}>
              {isEditMode ? 'Finish Editing' : 'Edit Course'}
            </button>
          )}
        </>
      )}
      {activeTab === 'members' && (
        <div>
          <h2>Enrolled Users</h2>
          {course?.enrolled_users && course?.enrolled_users.length > 0 ? (
            <ul>
              {course?.enrolled_users.map((user) => (
                <li key={user.id}>
                  {user}
                  {isCourseAdmin && (
                    <button
                      onClick={() => handleMakeCourseAdmin(user)}
                      style={styles.button}
                    >
                      Make course admin
                    </button>
                  )}  
                </li>
              ))}
            </ul>
          ) : (
            <p>No users enrolled in this course.</p>
          )}
          
          {isCourseAdmin && (
            <>
              <h2>Enrollment Requests</h2>
              {pendingRequests.length > 0 ? (
                <div style={styles.table}>
                  {pendingRequests.map((request) => (
                    <div key={request.id} style={styles.row}>
                      <div style={styles.cell}>{request.user.username}</div>
                      <div style={styles.cell}>{request.user.email}</div>
                      <div style={styles.cell}>{new Date(request.created_at).toISOString().split('T')[0]}</div>
                      <div style={styles.cell}>{request.status}</div>
                      <div style={styles.cell}>
                        <button onClick={() => updateEnrollmentRequest(request.id, 'approved')} style={styles.button}>Accept</button>
                        <button onClick={() => updateEnrollmentRequest(request.id, 'denied')} style={styles.button}>Deny</button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No pending enrollment requests found.</p>
              )}

              {handledRequests.length > 0 && (
                <>
                  <h2>Handled Requests</h2>
                  <div style={styles.table}>
                    {handledRequests.map((request) => (
                      <div key={request.id} style={styles.row}>
                        <div style={styles.cell}>{request.user.username}</div>
                        <div style={styles.cell}>{request.user.email}</div>
                        <div style={styles.cell}>{new Date(request.updated_at).toISOString().split('T')[0]}</div>
                        <div style={styles.cell}>{request.status}</div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
  
};

const styles = {
  topicContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    width: '100%',
  },
  tabButton: {
    padding: '10px 20px',
    margin: '5px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    marginBottom: '20px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#fff'
  },
  itemContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginBottom: '20px',
    justifyContent: 'flex-start',
  },
  item: {
    backgroundColor: '#f0f0f0',
    padding: '10px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)', // Optional: adds a subtle shadow for depth
    marginBottom: '10px', // Ensures space between items
    marginLeft: '0',
    position: 'relative'
  },
  title: {
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '5px', // Adds a small space between the title and the description
    float: 'left'
  },
  description: {
    color: '#666',
    float: 'left'
  },
  input: {
    padding: '10px',
    margin: '5px 0',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '16px',
    width: '100%'
  },
  button: {
    padding: '10px 20px',
    margin: '5px 0',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  },
  cancelButton: {
    padding: '10px 20px',
    margin: '5px 0',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#dc3545',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  },
  editButtonContainer: {
    position: 'absolute',
    right: '10px',
    top: '10px'
  },
  deleteButton: {
    padding: '10px 20px',
    margin: '5px 0',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#dc3545',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
    marginLeft: '10px'
  },
  table: {
    display: 'flex',
    flexDirection: 'column',
    marginTop: '20px'
  },
  row: {
    display: 'flex',
    alignItems: 'center',
    padding: '10px 0',
    borderBottom: '1px solid #ccc'
  },
  cell: {
    flex: '1',
    padding: '0 10px'
  },
};

export default CourseDetail;
