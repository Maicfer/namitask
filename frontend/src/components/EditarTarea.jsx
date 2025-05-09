import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";

const EditarTarea = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { authTokens } = useContext(AuthContext);
  const [tarea, setTarea] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTarea = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/tareas/${id}/`, {
          headers: { Authorization: `Bearer ${authTokens.access}` },
        });
        setTarea(response.data);
      } catch (err) {
        setError("No se pudo cargar la tarea.");
      } finally {
        setLoading(false);
      }
    };
    fetchTarea();
  }, [id]);

  const handleChange = (e) => {
    setTarea({ ...tarea, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const payload = {
        titulo: tarea.titulo,
        descripcion: tarea.descripcion,
        estado: tarea.estado,
        prioridad: tarea.prioridad,
        fecha_limite: tarea.fecha_limite,
        etiquetas_ids: tarea.etiquetas?.map(et => et.id) || []
      };

      await axios.put(`http://localhost:8000/api/tareas/${id}/`, payload, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
          "Content-Type": "application/json",
        },
      });

      alert("Tarea actualizada correctamente.");
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Error al actualizar la tarea.");
    }
  };

  if (loading) return <p className="text-center">Cargando tarea...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4 text-center">Editar Tarea</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="titulo"
          value={tarea.titulo}
          onChange={handleChange}
          placeholder="Título"
          className="w-full border px-3 py-2 rounded"
          required
        />
        <textarea
          name="descripcion"
          value={tarea.descripcion}
          onChange={handleChange}
          placeholder="Descripción"
          className="w-full border px-3 py-2 rounded"
        />
        <select
          name="estado"
          value={tarea.estado}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="pendiente">Pendiente</option>
          <option value="en_progreso">En Progreso</option>
          <option value="completada">Completada</option>
        </select>
        <select
          name="prioridad"
          value={tarea.prioridad}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
        </select>
        <input
          type="date"
          name="fecha_limite"
          value={tarea.fecha_limite || ""}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
        >
          Guardar Cambios
        </button>
      </form>
    </div>
  );
};

export default EditarTarea;
