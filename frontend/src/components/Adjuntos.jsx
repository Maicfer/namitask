import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Adjuntos = ({ tareaId }) => {
  const [adjuntos, setAdjuntos] = useState([]);
  const [archivo, setArchivo] = useState(null);
  const [descripcion, setDescripcion] = useState('');

  const token = JSON.parse(localStorage.getItem('authTokens'))?.access;

  const fetchAdjuntos = async () => {
    const res = await axios.get(`http://localhost:8000/api/adjuntos/?tarea=${tareaId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setAdjuntos(res.data);
  };

  useEffect(() => {
    fetchAdjuntos();
  }, [tareaId]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!archivo) return;

    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('descripcion', descripcion);
    formData.append('tarea', tareaId);

    await axios.post('http://localhost:8000/api/adjuntos/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    setArchivo(null);
    setDescripcion('');
    fetchAdjuntos();
  };

  return (
    <div className="p-4 border rounded bg-white shadow">
      <h4 className="text-lg font-semibold mb-2">Archivos adjuntos</h4>

      <form onSubmit={handleUpload} className="mb-4">
        <input type="file" onChange={(e) => setArchivo(e.target.files[0])} className="mb-2" />
        <input
          type="text"
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          placeholder="Descripción"
          className="form-control mb-2"
        />
        <button type="submit" className="btn btn-primary">Subir</button>
      </form>

      <ul className="list-disc list-inside">
        {adjuntos.map((a) => (
          <li key={a.id}>
            <a href={`http://localhost:8000${a.archivo}`} target="_blank" rel="noopener noreferrer">
              {a.descripcion || 'Archivo sin descripción'}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Adjuntos;
