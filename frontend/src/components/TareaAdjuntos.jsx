import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";

const TareaAdjuntos = ({ tareaId }) => {
  const { authTokens } = useContext(AuthContext);
  const [adjuntos, setAdjuntos] = useState([]);
  const [archivo, setArchivo] = useState(null);
  const [error, setError] = useState("");

  // Cargar adjuntos de la tarea
  const fetchAdjuntos = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/adjuntos/?tarea=${tareaId}`, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
        },
      });
      setAdjuntos(res.data);
    } catch (err) {
      console.error("Error al cargar adjuntos:", err);
    }
  };

  useEffect(() => {
    fetchAdjuntos();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!archivo) {
      setError("No hay archivos adjuntos");
      return;
    }

    const formData = new FormData();
    formData.append("archivo", archivo);
    formData.append("tarea", tareaId);

    try {
      await axios.post("http://localhost:8000/api/adjuntos/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${authTokens.access}`,
        },
      });
      setArchivo(null);
      setError("");
      fetchAdjuntos();
    } catch (err) {
      console.error("Error al subir adjunto:", err);
      setError("Error al subir el archivo.");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/adjuntos/${id}/`, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
        },
      });
      fetchAdjuntos();
    } catch (err) {
      console.error("Error al eliminar adjunto:", err);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleUpload} className="space-y-2">
        <input
          type="file"
          onChange={(e) => setArchivo(e.target.files[0])}
          className="block w-full text-sm text-gray-600"
        />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button
          type="submit"
          className="px-4 py-1 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Subir archivo
        </button>
      </form>

      <ul className="mt-4 space-y-2">
        {adjuntos.map((item) => (
          <li key={item.id} className="border p-2 rounded flex justify-between items-center">
            <a
              href={`http://localhost:8000${item.archivo}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline"
            >
              {item.archivo.split("/").pop()}
            </a>
            <button
              onClick={() => handleDelete(item.id)}
              className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-xs"
            >
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TareaAdjuntos;
