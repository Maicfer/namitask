import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const estados = ['pendiente', 'en_progreso', 'completada'];
const etiquetasEstados = {
  pendiente: 'Pendiente 🟡',
  en_progreso: 'En Progreso 🔵',
  completada: 'Completada ✅',
};

const TableroKanban = () => {
  const { authTokens } = useContext(AuthContext);
  const [tareas, setTareas] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTareas = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/tareas/', {
          headers: {
            Authorization: `Bearer ${authTokens.access}`,
          },
        });
        setTareas(res.data);
      } catch (err) {
        console.error('Error al cargar tareas:', err);
      }
    };
    fetchTareas();
  }, []);

  return (
    <div className="p-6 min-h-screen bg-gray-100">
      <h2 className="text-3xl font-bold text-center text-indigo-700 mb-6">Tablero de Tareas</h2>
      <div className="flex justify-center gap-4 overflow-auto">
        {estados.map((estado) => (
          <div
            key={estado}
            className="w-80 bg-white rounded-lg shadow p-4 space-y-4 border border-gray-200"
          >
            <h3 className="text-lg font-semibold text-center text-indigo-600">
              {etiquetasEstados[estado]}
            </h3>
            {tareas
              .filter((t) => t.estado === estado)
              .map((tarea) => (
                <div
                  key={tarea.id}
                  className="bg-gray-50 p-3 rounded shadow hover:bg-gray-100 cursor-pointer"
                  onClick={() => navigate(`/tareas/${tarea.id}`)}
                >
                  <h4 className="font-bold text-sm">{tarea.titulo}</h4>
                  <p className="text-xs text-gray-500">
                    Prioridad: {tarea.prioridad} <br />
                    Límite: {tarea.fecha_limite || 'Sin fecha'}
                  </p>

                  {/* Etiquetas visuales */}
                  {tarea.etiquetas?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {tarea.etiquetas.map((et) => (
                        <span
                          key={et.id}
                          className="text-xs bg-indigo-500 text-white px-2 py-1 rounded-full"
                        >
                          {et.nombre}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TableroKanban;

