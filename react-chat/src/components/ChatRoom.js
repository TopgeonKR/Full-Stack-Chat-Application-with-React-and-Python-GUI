import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import { useNavigate } from "react-router-dom";

const socket = io("http://127.0.0.1:5000");

function ChatRoom() {
  const [username, setUsername] = useState(""); // 로그인한 사용자 이름
  const [messages, setMessages] = useState([]); // 기존 채팅 메시지
  const [message, setMessage] = useState(""); // 현재 입력 중인 메시지
  const navigate = useNavigate(); // 페이지 이동을 위한 네비게이션

  // 채팅 데이터 가져오기
  useEffect(() => {
    // Fetch chat data with credentials
    fetch("http://127.0.0.1:5000/chat", {
      method: "GET",
      credentials: "include", // 쿠키 포함
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          console.error(data.error);
        } else {
          setUsername(data.username); // 로그인한 사용자 이름 설정
          setMessages(data.messages); // 기존 채팅 기록 설정
        }
      })
      .catch((error) => console.error("Error fetching chat data:", error));

  }, [navigate]);

  // 새 메시지 수신 시 처리
  useEffect(() => {
    socket.on("receive_message", (newMessage) => {
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    });

    return () => socket.off("receive_message");
  }, []);

  // 메시지 보내기
  const sendMessage = () => {
    if (message.trim()) {
      socket.emit("send_message", { message });
      setMessage(""); // 입력 창 초기화
    }
  };

  return (
    <div>
      <h2>Chat Room</h2>
      <p>Logged in as: <strong>{username}</strong></p>
      <div>
        {messages.map((msg, index) => (
          <p key={index}>
            <strong>{msg.username}</strong>: {msg.message}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message"
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatRoom;
