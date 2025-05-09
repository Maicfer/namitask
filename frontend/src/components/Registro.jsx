import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Container, Card, Button, Row, Col } from 'react-bootstrap';

const Registro = () => {
  const navigate = useNavigate();

  const initialValues = {
    nombre_completo: '',
    email: '',
    password: '',
    confirmPassword: '',
    numero_documento: '',
    fecha_nacimiento: '',
    pais: '',
    ciudad: '',
    celular: '',
    genero: '',
  };

  const validationSchema = Yup.object({
    nombre_completo: Yup.string().required('Requerido'),
    email: Yup.string().email('Email inválido').required('Requerido'),
    password: Yup.string().min(6, 'Mínimo 6 caracteres').required('Requerido'),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref('password'), null], 'Las contraseñas no coinciden')
      .required('Requerido'),
    numero_documento: Yup.string().required('Requerido'),
    fecha_nacimiento: Yup.date().required('Requerido'),
    pais: Yup.string().required('Requerido'),
    ciudad: Yup.string().required('Requerido'),
    celular: Yup.string().required('Requerido'),
    genero: Yup.string().required('Requerido'),
  });

  const handleSubmit = async (values, { setSubmitting, setErrors }) => {
    try {
      const payload = {
        email: values.email,
        nombre_completo: values.nombre_completo,
        password: values.password,
        password2: values.confirmPassword,      // aseguramos enviar password2
        numero_documento: values.numero_documento,
        fecha_nacimiento: values.fecha_nacimiento,
        pais: values.pais,
        ciudad: values.ciudad,
        celular: values.celular,
        genero: values.genero,
      };

      console.log('Payload enviado:', payload);

      await axios.post('http://localhost:8000/api/register/', payload);
      alert('Registro exitoso');
      navigate('/login');
    } catch (error) {
      console.error('Error de registro:', error.response?.data);

      // Errores específicos de validación (puedes añadir más campos si es necesario)
      if (error.response?.data) {
        const data = error.response.data;
        if (data.email) {
          setErrors({ email: data.email[0] });
        }
        if (data.numero_documento) {
          setErrors({ numero_documento: data.numero_documento[0] });
        }
      } else {
        alert('Error en el registro. Intenta nuevamente.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="p-4">
            <h3 className="text-center mb-4">Registro</h3>
            <Formik
              initialValues={initialValues}
              validationSchema={validationSchema}
              onSubmit={handleSubmit}
            >
              {({ isSubmitting }) => (
                <Form>
                  <Row>
                    <Col md={6}>
                      <label>Nombre completo</label>
                      <Field className="form-control" name="nombre_completo" />
                      <ErrorMessage name="nombre_completo" component="div" className="text-danger" />

                      <label className="mt-2">Correo</label>
                      <Field className="form-control" name="email" type="email" />
                      <ErrorMessage name="email" component="div" className="text-danger" />

                      <label className="mt-2">Contraseña</label>
                      <Field className="form-control" name="password" type="password" />
                      <ErrorMessage name="password" component="div" className="text-danger" />

                      <label className="mt-2">Confirmar contraseña</label>
                      <Field className="form-control" name="confirmPassword" type="password" />
                      <ErrorMessage name="confirmPassword" component="div" className="text-danger" />

                      <label className="mt-2">Número de documento</label>
                      <Field className="form-control" name="numero_documento" />
                      <ErrorMessage name="numero_documento" component="div" className="text-danger" />
                    </Col>

                    <Col md={6}>
                      <label>Fecha de nacimiento</label>
                      <Field className="form-control" name="fecha_nacimiento" type="date" />
                      <ErrorMessage name="fecha_nacimiento" component="div" className="text-danger" />

                      <label className="mt-2">País</label>
                      <Field className="form-control" name="pais" />
                      <ErrorMessage name="pais" component="div" className="text-danger" />

                      <label className="mt-2">Ciudad</label>
                      <Field className="form-control" name="ciudad" />
                      <ErrorMessage name="ciudad" component="div" className="text-danger" />

                      <label className="mt-2">Celular</label>
                      <Field className="form-control" name="celular" />
                      <ErrorMessage name="celular" component="div" className="text-danger" />

                      <label className="mt-2">Género</label>
                      <Field as="select" className="form-control" name="genero">
                        <option value="">Selecciona</option>
                        <option value="M">Masculino</option>
                        <option value="F">Femenino</option>
                        <option value="O">Otro</option>
                      </Field>
                      <ErrorMessage name="genero" component="div" className="text-danger" />
                    </Col>
                  </Row>
                  <Button
                    className="mt-4 w-100"
                    type="submit"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Registrando...' : 'Registrarse'}
                  </Button>
                </Form>
              )}
            </Formik>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Registro;





