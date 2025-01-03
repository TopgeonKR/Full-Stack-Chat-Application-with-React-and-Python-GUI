import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Include cookies for session
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration successful! Redirecting to login...");
        setTimeout(() => navigate("/login"), 2000); // Redirect to login page after 2 seconds
      } else {
        setError(data.error || "Registration failed. Please try again.");
      }
    } catch (err) {
      console.error("Error during registration:", err);
      setError("Unable to connect to the server. Please try again later.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Register</h2>
      <form
        onSubmit={handleRegister}
        style={{ display: "inline-block", marginTop: "20px" }}
      >
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ marginBottom: "10px", width: "200px", padding: "10px" }}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ marginBottom: "10px", width: "200px", padding: "10px" }}
          />
        </div>
        <div>
          <button type="submit" style={{ padding: "10px 20px" }}>
            Register
          </button>
        </div>
      </form>
      {message && <p style={{ marginTop: "20px", color: "green" }}>{message}</p>}
      {error && <p style={{ marginTop: "20px", color: "red" }}>{error}</p>}
      <button
        onClick={() => navigate("/")}
        style={{ marginTop: "10px", padding: "10px 20px" }}
      >
        Go Back to Main
      </button>
    </div>
  );
}

export default Register;
