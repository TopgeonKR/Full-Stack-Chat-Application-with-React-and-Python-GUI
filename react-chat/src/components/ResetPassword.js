import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function ResetPassword() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleReset = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:5000/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, new_password: newPassword }),
    });

    const result = await response.json();
    if (response.ok) {
      setMessage("Password reset successfully!");
    } else {
      setMessage(result.message || "Password reset failed");
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <form onSubmit={handleReset}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Current Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
        <button type="submit">Reset</button>
      </form>
      <p>{message}</p>
      <button onClick={() => navigate("/")}>Go Back to Main</button>
    </div>
  );
}

export default ResetPassword;
