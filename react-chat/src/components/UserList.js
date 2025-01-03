import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function UserList() {
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch("http://127.0.0.1:5000/userlist");
      const result = await response.json();
      setUsers(result.users);
    };
    fetchUsers();
  }, []);

  return (
    <div>
      <h2>User List</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.username}</li>
        ))}
      </ul>
      <button onClick={() => navigate("/")}>Go Back to Main</button>
    </div>
  );
}

export default UserList;
