import logo from './logo.svg';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import Courses from './Courses'
import Navbar from './Navbar';
import Login from './Login';
import RequireAuth from './RequireAuth'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import EnrollmentRequests from './EnrollmentRequest';
import CoursesToEnroll from './CoursesToEnroll';
import CourseDetail from './CourseDetail';
import ForumDetail from './ForumDetail';
import NotFound from './NotFound';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="app-container">
          <Navbar />
          <div className="content-container">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/courses" element={<Courses />}/>
              <Route path="/enrollCourses" element={<RequireAuth><CoursesToEnroll /></RequireAuth>} />
              <Route path="/courses/:courseId" element={<CourseDetail />} />
              <Route path="/forums/:forumId" element={<ForumDetail /> }/>
              <Route path="/" element={<Navigate replace to="/login" />} />
              <Route path="*" element={<NotFound />} /> {/* Catch-all route for 404 */}
            </Routes>
          </div>
        </div>
        <ToastContainer />
      </div>
    </Router>
  );
}

export default App;
