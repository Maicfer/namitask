import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { authTokens, user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [perfil, setPerfil] = useState(null);
  const [fotoPreview, setFotoPreview] = useState(null);
  const [form, setForm] = useState({
    nombre_completo: "",
    celular: "",
    ciudad: "",
    pais: "",
    genero: "",
  });
  const [foto, setFoto] = useState(null);

  useEffect(() => {
    if (!authTokens) {
      navigate("/login");
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/profile/", {
          headers: { Authorization: `Bearer ${authTokens.access}` },
        });
        setPerfil(response.data);
        setForm({
          nombre_completo: response.data.nombre_completo || "",
          celular: response.data.celular || "",
          ciudad: response.data.ciudad || "",
          pais: response.data.pais || "",
          genero: response.data.genero || "",
        });
        setFotoPreview(response.data.foto || null);
      } catch (error) {
        console.error("Error al cargar perfil:", error);
      }
    };

    fetchProfile();
  }, [authTokens, navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFotoChange = (e) => {
    const file = e.target.files[0];
    setFoto(file);
    setFotoPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      formData.append(key, value);
    });
    if (foto) {
      formData.append("foto", foto);
    }

    try {
      await axios.put("http://localhost:8000/api/profile/", formData, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
          "Content-Type": "multipart/form-data",
        },
      });
      alert("Perfil actualizado correctamente.");
    } catch (error) {
      console.error("Error al actualizar perfil:", error);
      alert("Error al actualizar perfil.");
    }
  };

  if (!perfil) return <div className="text-center mt-8">Cargando perfil...</div>;

  return (
    <div className="min-h-screen p-8 bg-gray-100 pt-24">
      <div className="max-w-xl mx-auto bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-center text-indigo-700 mb-4">Mi Perfil</h2>

        {fotoPreview && (
          <div className="text-center mb-4">
            <img
              src={`http://localhost:8000${fotoPreview}`}
              alt="Foto de perfil"
              className="w-32 h-32 mx-auto rounded-full object-cover"
            />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="nombre_completo"
            placeholder="Nombre completo"
            value={form.nombre_completo}
            onChange={handleChange}
            className="form-control"
          />
          <input
            type="text"
            name="celular"
            placeholder="Celular"
            value={form.celular}
            onChange={handleChange}
            className="form-control"
          />
          <input
            type="text"
            name="ciudad"
            placeholder="Ciudad"
            value={form.ciudad}
            onChange={handleChange}
            className="form-control"
          />
          <input
            type="text"
            name="pais"
            placeholder="País"
            value={form.pais}
            onChange={handleChange}
            className="form-control"
          />
          <select
            name="genero"
            value={form.genero}
            onChange={handleChange}
            className="form-control"
          >
            <option value="">Selecciona género</option>
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
            <option value="O">Otro</option>
          </select>
          <input type="file" onChange={handleFotoChange} className="form-control" />

          <div className="flex justify-between mt-6 flex-wrap gap-3">
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              Guardar cambios
            </button>

            <button
              type="button"
              onClick={() => navigate("/dashboard")}
              className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
            >
              Ir al Dashboard
            </button>

            <button
              type="button"
              onClick={() => navigate("/cambiar-password")}
              className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded"
            >
              Cambiar contraseña
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Profile;






