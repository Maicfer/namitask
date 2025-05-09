import React, { useContext, useState } from 'react';
import axios from 'axios';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Container, Card, Button } from 'react-bootstrap';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { loginUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const [generalError, setGeneralError] = useState('');

  const validationSchema = Yup.object({
    email: Yup.string().email('Email inválido').required('Requerido'),
    password: Yup.string().required('Requerido'),
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      setGeneralError('');
      const payload = {
        email: values.email.trim().toLowerCase(),
        password: values.password,
      };

      const response = await axios.post('http://localhost:8000/api/login/', payload);
      loginUser(response.data);
      navigate('/dashboard');
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setGeneralError(error.response.data.error);
      } else {
        setGeneralError('Error desconocido. Intenta de nuevo.');
      }
      console.error('Login error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container className="mt-5">
      <Card className="p-4 mx-auto" style={{ maxWidth: '500px' }}>
        <h3 className="text-center mb-3">Iniciar sesión</h3>
        {generalError && <div className="text-danger text-center mb-2">{generalError}</div>}
        <Formik
          initialValues={{ email: '', password: '' }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          <Form>
            <label>Correo</label>
            <Field className="form-control" name="email" type="email" />
            <ErrorMessage name="email" component="div" className="text-danger" />

            <label className="mt-2">Contraseña</label>
            <Field className="form-control" name="password" type="password" />
            <ErrorMessage name="password" component="div" className="text-danger" />

            <Button className="mt-3 w-100" type="submit">Ingresar</Button>
          </Form>
        </Formik>
      </Card>
    </Container>
  );
};

export default Login;






