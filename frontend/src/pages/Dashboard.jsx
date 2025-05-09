import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen pt-24 p-8 bg-gray-100">
      <div className="max-w-xl mx-auto bg-white rounded-xl p-6 shadow-lg text-center space-y-4">
        <h1 className="text-2xl font-bold text-indigo-700">
          Bienvenido, {user?.nombre_completo || "Usuario"}
        </h1>
        <p className="text-gray-600">Correo: {user?.email}</p>

        <div className="flex justify-center gap-4 mt-4 flex-wrap">
          <button
            onClick={() => navigate("/profile")}
            className="px-4 py-2 border border-indigo-700 text-indigo-700 rounded hover:bg-indigo-700 hover:text-white"
          >
            Mi Perfil
          </button>
          <button
            onClick={() => navigate("/tablero")}
            className="px-4 py-2 border border-indigo-700 text-indigo-700 rounded hover:bg-indigo-700 hover:text-white"
          >
            Ir al Tablero
          </button>
          <button
            onClick={logoutUser}
            className="px-4 py-2 border border-red-500 text-red-500 rounded hover:bg-red-500 hover:text-white"
          >
            Cerrar sesión
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;







