// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AnimePage from "./pages/AnimePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />       {/* Домашняя страница */}
        <Route path="/anime" element={<AnimePage />} />  {/* Страница со списком аниме */}
      </Routes>
    </Router>
  );
}

export default App;
