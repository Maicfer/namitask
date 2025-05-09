import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from "./components/Navbar";
import Registro from './components/Registro';
import Login from './components/Login';
import Dashboard from './pages/Dashboard';
import { AuthContext } from './context/AuthContext';
import Profile from './components/Profile';
import CambiarPassword from "./components/CambiarPassword"; 
import TareaDetalle from './components/TareaDetalle';
import EditarTarea from './components/EditarTarea';
import Etiquetas from './components/Etiquetas';
import TableroKanban from './components/TableroKanban';
import CrearTarea from "./components/CrearTarea"; 
import RutaPrivada from './components/RutaPrivada';

const App = () => {
  const { user } = useContext(AuthContext);

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />

        <Route path="/profile" element={<RutaPrivada><Profile /></RutaPrivada>} />
        <Route path="/cambiar-password" element={<RutaPrivada><CambiarPassword /></RutaPrivada>} />
        <Route path="/dashboard" element={<RutaPrivada><Dashboard /></RutaPrivada>} />
        <Route path="/crear-tarea" element={<RutaPrivada><CrearTarea /></RutaPrivada>} />
        <Route path="/tareas/:id" element={<RutaPrivada><TareaDetalle /></RutaPrivada>} />
        <Route path="/tareas/:id/editar" element={<RutaPrivada><EditarTarea /></RutaPrivada>} />
        <Route path="/etiquetas" element={<RutaPrivada><Etiquetas /></RutaPrivada>} />
        <Route path="/tablero" element={<RutaPrivada><TableroKanban /></RutaPrivada>} />
      </Routes>
    </>
  );
};

export default App;





