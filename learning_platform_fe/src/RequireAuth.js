import React from 'react';
import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }) => {
  const auth = localStorage.getItem('jwt');
  return auth ? children : <Navigate to="/login" />;
};

export default RequireAuth;