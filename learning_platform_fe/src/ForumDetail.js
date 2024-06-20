import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import QuestionForm from './QuestionForm';
import fileIcon from './fileIcon.png'; // Adjust the path as needed

const ForumDetail = () => {
  const { forumId } = useParams();
  const [forum, setForum] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showQuestionForm, setShowQuestionForm] = useState(false);

  const fetchForumDetails = async () => {
    const token = localStorage.getItem('jwt');
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const apiUrl = `${process.env.REACT_APP_API_URL}/api/forums/${forumId}`;
    try {
      const response = await fetch(apiUrl, { headers });
      const data = await response.json();
      if (response.ok) {
        setForum(data);
      } else {
        throw new Error('Failed to fetch forum details');
      }
    } catch (error) {
      toast.error(error.message);
    }
    setIsLoading(false);
    setShowQuestionForm(false);
  };

  useEffect(() => {
    fetchForumDetails();
  }, [forumId]);

  if (isLoading) return <div>Loading forum details...</div>;
  if (!forum) return <div>No forum details found.</div>;

  return (
    <div>
      <h1>{forum.title}</h1>
      <p>{forum.description}</p>

      <h2>Questions</h2>
      {forum.questions && forum.questions.length > 0 ? (
        forum.questions.map(question => (
          <div key={question.id} style={styles.question}>
            <h3 style={styles.text}>{question.title}</h3>
            <p style={styles.text}>&nbsp;&nbsp;&nbsp;&nbsp; {question.description}</p>
            {question.attachments.length > 0 && (
              <div>
                <h4 style={styles.text}>Attachments:</h4>
                {question.attachments.map(attachment => (
                  <div key={attachment.id} style={styles.attachment}>
                    <div style={styles.icon}>
                      <img src={fileIcon} alt="file icon" style={styles.iconImage} />
                    </div>
                    <div style={styles.text}>
                      <a
                        href={`${process.env.REACT_APP_API_URL}/api/question-attachments/${attachment.id}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        download
                      >
                        {attachment.file.split('/').pop()}
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))
      ) : (
        <p>There are still no questions in the forum. Be the first to make one!</p>
      )}

      <button onClick={() => setShowQuestionForm(!showQuestionForm)} style={styles.button}>
        {showQuestionForm ? 'Cancel' : 'Add Question'}
      </button>

      {showQuestionForm && <QuestionForm forumId={forumId} onSuccess={fetchForumDetails} />}
    </div>
  );
};

const styles = {
  question: {
    padding: '10px',
    margin: '10px 0',
    border: '1px solid #ccc',
    borderRadius: '4px',
    justifyContent: 'flex-start',
  },
  button: {
    padding: '10px 20px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  },
  attachment: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '10px'
  },
  icon: {
    marginRight: '10px'
  },
  iconImage: {
    width: '24px',
    height: '24px'
  },
  text: {
    textAlign: 'left'
  },
  description: {
    color: '#666',
    float: 'left'
  },
};

export default ForumDetail;
