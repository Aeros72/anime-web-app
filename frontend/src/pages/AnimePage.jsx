// src/pages/AnimePage.jsx
import { useEffect, useState } from "react";

export default function AnimePage() {
  const [animeList, setAnimeList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // =========================
  // FETCH ANIME
  // =========================
  const fetchAnime = (page = 1) => {
    const token = localStorage.getItem("access");
    if (!token) {
      alert("Please login first");
      return;
    }

    fetch(`http://127.0.0.1:8000/api/anime/?page=${page}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("API response:", data); // для дебага
        setAnimeList(data.results); // подстраховка: если data.results undefined, можно написать data.results ?? data
        setCurrentPage(page);
        setTotalPages(Math.ceil(data.count / 20)); // считаем кол-во страниц
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchAnime(1); // загружаем первую страницу при монтировании
  }, []);

  // =========================
  // RENDER
  // =========================
  return (
    <div style={{ padding: "20px" }}>
      <h1>Anime List</h1>

      {animeList.map((anime) => (
        <div key={anime.id} style={{ marginBottom: "20px" }}>
          <h3>{anime.title}</h3>
          <img src={anime.image} width="150" alt={anime.title} />
          <p>Score: {anime.score}</p>
          <p>Episodes: {anime.episodes}</p>
          <p>Year: {anime.release_year}</p>
          <p>Status: {anime.status}</p>
          <p>
            Genres:{" "}
            {anime.genres && anime.genres.length > 0
              ? anime.genres.map((g) => g.name).join(", ")
              : "—"}
          </p>
          <p>{anime.description || "No description"}</p>
        </div>
      ))}

      {/* =========================
          PAGINATION BUTTONS
      ========================= */}
      <div style={{ marginTop: "20px" }}>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => fetchAnime(page)}
            style={{
              margin: "0 5px",
              fontWeight: page === currentPage ? "bold" : "normal",
            }}
          >
            {page}
          </button>
        ))}
      </div>
    </div>
  );
}