import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./components/Main";
import Register from "./components/Register";
import Login from "./components/Login";
import ChatRoom from "./components/ChatRoom";
import UserList from "./components/UserList";
import DeleteUser from "./components/DeleteUser"; // 추가
import ResetPassword from "./components/ResetPassword"; // 추가

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/chatroom" element={<ChatRoom />} />
        <Route path="/userlist" element={<UserList />} />
        <Route path="/delete-user" element={<DeleteUser />} /> {/* 추가 */}
        <Route path="/reset-password" element={<ResetPassword />} /> {/* 추가 */}
      </Routes>
    </Router>
  );
}

export default App;
