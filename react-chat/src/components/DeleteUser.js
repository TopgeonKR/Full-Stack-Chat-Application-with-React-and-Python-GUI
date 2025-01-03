import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function DeleteUser() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleDelete = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:5000/delete-user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (response.ok) {
      setMessage("User deleted successfully!");
    } else {
      setMessage(result.message || "Deletion failed");
    }
  };

  return (
    <div>
      <h2>Delete User</h2>
      <form onSubmit={handleDelete}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Delete</button>
      </form>
      <p>{message}</p>
      <button onClick={() => navigate("/")}>Go Back to Main</button>
    </div>
  );
}

export default DeleteUser;
