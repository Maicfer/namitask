import React, { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import TareaAdjuntos from "./TareaAdjuntos";
import { AuthContext } from "../context/AuthContext";

const TareaDetalle = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { authTokens } = useContext(AuthContext);

  const [tarea, setTarea] = useState(null);
  const [historial, setHistorial] = useState([]);
  const [checklist, setChecklist] = useState([]);
  const [error, setError] = useState("");

  const fetchTarea = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/tareas/${id}/`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      });
      setTarea(res.data);
      setChecklist(res.data.checklist); // importante
    } catch (err) {
      setError("No se pudo cargar la tarea.");
    }
  };

  const fetchHistorial = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/actividad/?tarea=${id}`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      });
      setHistorial(res.data);
    } catch (err) {
      console.error("Error al cargar historial:", err);
    }
  };

  const toggleChecklistItem = async (itemId, completado) => {
    try {
      await axios.patch(
        `http://localhost:8000/api/checklistitems/${itemId}/`,
        { completado: !completado },
        { headers: { Authorization: `Bearer ${authTokens.access}` } }
      );
      fetchTarea(); // recargar checklist
    } catch (err) {
      console.error("Error actualizando checklist", err);
    }
  };

  useEffect(() => {
    fetchTarea();
    fetchHistorial();
  }, [id]);

  if (error) return <p className="text-center text-red-600">{error}</p>;
  if (!tarea) return <p className="text-center">Cargando tarea...</p>;

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded shadow space-y-4">
      <h2 className="text-2xl font-bold text-indigo-700 text-center">Detalle de la Tarea</h2>

      <div className="space-y-1">
        <p><strong>Título:</strong> {tarea.titulo}</p>
        <p><strong>Descripción:</strong> {tarea.descripcion || "No asignada"}</p>
        <p><strong>Estado:</strong> {tarea.estado}</p>
        <p><strong>Prioridad:</strong> {tarea.prioridad}</p>
        <p><strong>Fecha límite:</strong> {tarea.fecha_limite || "No definida"}</p>
      </div>

      {/* Checklist */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold">Checklist</h3>
        {!checklist || checklist.length === 0 ? (
          <p className="text-gray-500">Sin subtareas.</p>
        ) : (
          <ul className="space-y-2">
            {checklist.map(item => (
              <li key={item.id} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={item.completado}
                  onChange={() => toggleChecklistItem(item.id, item.completado)}
                />
                <span className={item.completado ? "line-through text-gray-400" : ""}>
                  {item.nombre}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Adjuntos */}
      <TareaAdjuntos tareaId={id} />

      {/* Historial */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold mb-2">Historial de actividad</h3>
        {historial.length === 0 ? (
          <p className="text-gray-500">Sin registros aún.</p>
        ) : (
          <ul className="space-y-2">
            {historial.map((item) => (
              <li key={item.id} className="border-l-4 border-indigo-500 pl-3 text-sm">
                <p>{item.descripcion}</p>
                <p className="text-xs text-gray-400">{new Date(item.fecha).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Botones */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => navigate(`/tareas/${id}/editar`)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Editar tarea
        </button>
        <button
          onClick={() => navigate("/dashboard")}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
        >
          Volver al dashboard
        </button>
      </div>
    </div>
  );
};

export default TareaDetalle;


