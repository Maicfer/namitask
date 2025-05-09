import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Login from "../components/Login";
import { AuthContext } from "../context/AuthContext";
import { BrowserRouter } from "react-router-dom";

describe("Login Component", () => {
  it("muestra campos de email y contraseña", () => {
    render(
      <BrowserRouter>
        <AuthContext.Provider value={{ loginUser: jest.fn() }}>
          <Login />
        </AuthContext.Provider>
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/Correo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Contraseña/i)).toBeInTheDocument();
  });

  it("muestra error si se envía sin datos", async () => {
    render(
      <BrowserRouter>
        <AuthContext.Provider value={{ loginUser: jest.fn() }}>
          <Login />
        </AuthContext.Provider>
      </BrowserRouter>
    );

    const button = screen.getByRole("button", { name: /ingresar/i });
    fireEvent.click(button);

    expect(await screen.findAllByText("Requerido")).toHaveLength(2);
  });
});

