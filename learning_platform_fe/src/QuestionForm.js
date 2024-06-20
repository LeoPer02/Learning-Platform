import React, { Component } from 'react';
import { toast } from 'react-toastify';

class QuestionForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: '',
      description: '',
      file: null
    };

    this.handleFileChange = this.handleFileChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleFileChange(event) {
    this.setState({ file: event.target.files[0] });
  }

  handleInputChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  async handleSubmit(event) {
    event.preventDefault();
  
    const { title, description, file } = this.state;
    const { forumId, onSuccess } = this.props;
  
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('forum', forumId);
    if (file) {
      formData.append('file', file);
    }
  
    const headers = {};
    const token = localStorage.getItem('jwt');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/questions/`, {
        method: 'POST',
        headers,
        body: formData,
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.file || 'Failed to create question');
      }
  
      toast.success('Question created successfully');
      this.setState({ title: '', description: '', file: null });
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      toast.error(error.message);
    }
  }

  render() {
    const { title, description } = this.state;

    return (
      <form onSubmit={this.handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label htmlFor="title" style={styles.label}>Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={title}
            onChange={this.handleInputChange}
            style={styles.input}
            required
          />
        </div>
        <div style={styles.formGroup}>
          <label htmlFor="description" style={styles.label}>Description</label>
          <textarea
            id="description"
            name="description"
            value={description}
            onChange={this.handleInputChange}
            style={styles.textarea}
            required
          />
        </div>
        <div style={styles.formGroup}>
          <label htmlFor="file" style={styles.label}>Upload File</label>
          <input
            type="file"
            id="file"
            onChange={this.handleFileChange}
            style={styles.input}
          />
        </div>
        <button type="submit" style={styles.button}>Submit</button>
      </form>
    );
  }
}

const styles = {
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    width: '90%',
    margin: '0 auto',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#fff'
  },
  formGroup: {
    marginBottom: '15px',
    width: '98%'
  },
  label: {
    display: 'block',
    marginBottom: '5px',
    fontSize: '16px',
    fontWeight: 'bold'
  },
  input: {
    width: '100%',
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: '1px solid #ccc'
  },
  textarea: {
    width: '100%',
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    height: '100px',
    resize: 'vertical'
  },
  button: {
    padding: '10px 20px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer'
  }
};

export default QuestionForm;
