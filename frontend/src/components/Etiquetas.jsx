import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';

const Etiquetas = () => {
  const { authTokens } = useContext(AuthContext);
  const [etiquetas, setEtiquetas] = useState([]);
  const [nombre, setNombre] = useState('');
  const [color, setColor] = useState('');

  const fetchEtiquetas = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/etiquetas/', {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      });
      setEtiquetas(res.data);
    } catch (err) {
      console.error("Error al cargar etiquetas:", err);
    }
  };

  const crearEtiqueta = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        'http://localhost:8000/api/etiquetas/',
        { nombre, color },
        { headers: { Authorization: `Bearer ${authTokens.access}` } }
      );
      setNombre('');
      setColor('');
      fetchEtiquetas();
    } catch (err) {
      console.error("Error al crear etiqueta:", err);
    }
  };

  const eliminarEtiqueta = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/etiquetas/${id}/`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      });
      fetchEtiquetas();
    } catch (err) {
      console.error("Error al eliminar etiqueta:", err);
    }
  };

  useEffect(() => {
    fetchEtiquetas();
  }, []);

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow mt-10">
      <h2 className="text-xl font-bold mb-4 text-indigo-600">Gestión de Etiquetas</h2>

      <form onSubmit={crearEtiqueta} className="space-y-2 mb-6">
        <input
          type="text"
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        />
        <input
          type="text"
          placeholder="Color (ej: rojo)"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          className="w-full border px-3 py-2 rounded"
        />
        <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
          Crear Etiqueta
        </button>
      </form>

      <ul className="space-y-2">
        {etiquetas.map((etiqueta) => (
          <li key={etiqueta.id} className="flex justify-between items-center border p-2 rounded">
            <span className="font-semibold" style={{ color: etiqueta.color }}>{etiqueta.nombre}</span>
            <button
              onClick={() => eliminarEtiqueta(etiqueta.id)}
              className="text-red-600 hover:underline text-sm"
            >
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Etiquetas;
