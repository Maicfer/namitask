import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div
        className="flex items-center cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        <img
          src="/logo.png"
          alt="Logo"
          className="h-8 w-8 mr-2"
        />
        <span className="text-xl font-semibold text-indigo-700">NamiTask</span>
      </div>

      <div className="space-x-4 text-indigo-700">
        {!user ? (
          <>
            <Link to="/login" className="hover:underline">Iniciar sesión</Link>
            <Link to="/registro" className="hover:underline">Registrarse</Link>
          </>
        ) : (
          <>
            <Link to="/dashboard" className="hover:underline">Inicio</Link>
            <Link to="/crear-tarea" className="hover:underline">Crear tarea</Link>
            <Link to="/etiquetas" className="hover:underline">Etiquetas</Link>
            <button
              onClick={logoutUser}
              className="ml-2 px-3 py-1 border border-indigo-700 text-indigo-700 rounded hover:bg-indigo-700 hover:text-white transition"
            >
              Cerrar sesión
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;

