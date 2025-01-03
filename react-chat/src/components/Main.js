import React from "react";
import { Link } from "react-router-dom";

function Main() {
    return (
        <div>
            <h1>Welcome to the Chat App</h1>
            <Link to="/register">Register</Link> | <Link to="/login">Login</Link> |{" "}
            <Link to="/delete-user">Delete User</Link> |{" "}
            <Link to="/reset-password">Reset Password</Link> |{" "}
            <Link to="/userlist">User List</Link>
        </div>
    );
}

export default Main;
