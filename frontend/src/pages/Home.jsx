// src/pages/Home.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);

  // Логин
  const navigate = useNavigate(); // сверху в компоненте, импортируем из react-router-dom

  const handleLogin = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/users/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Login failed");

      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      setUser({ email });
      alert("Logged in!");

      navigate("/anime"); // Переходим на страницу аниме
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Login / Register</h1>

      {!user && (
        <>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ marginBottom: "10px", display: "block" }}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ marginBottom: "10px", display: "block" }}
          />
          <button onClick={handleLogin}>Login</button>
        </>
      )}

      {user && (
        <>
          <p>Welcome, {user.email}</p>
          <button onClick={() => navigate("/anime")}>Go to Anime List</button>
        </>
      )}
    </div>
  );
}
