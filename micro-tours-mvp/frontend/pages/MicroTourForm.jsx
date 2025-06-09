import React, { useState } from "react";

export default function MicroTourForm() {
  const [placeId, setPlaceId] = useState("");
  const [category, setCategory] = useState("cafe");
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("/generate_microtour", {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-api-key": "changeme" }, // Replace with your real API key
        body: JSON.stringify({ place_id: placeId, category, city }),
      });
      const data = await res.json();
      if (!data.success) setError(data.error || "Unknown error");
      else setResult(data);
    } catch (err) {
      setError("Network error");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Micro-Tours Darija</h1>
      <form onSubmit={handleSubmit}>
        <label>Place ID:</label>
        <input value={placeId} onChange={e => setPlaceId(e.target.value)} required />
        <label>Category:</label>
        <select value={category} onChange={e => setCategory(e.target.value)}>
          <option value="cafe">مقهى</option>
          <option value="monument">معلمة</option>
          <option value="souk">سوق</option>
          <option value="garden">حديقة</option>
        </select>
        <label>City:</label>
        <input value={city} onChange={e => setCity(e.target.value)} placeholder="طنجة" />
        <button className="button" type="submit" disabled={loading}>
          {loading ? "...جاري التوليد" : "توليد الجولة"}
        </button>
      </form>
      {error && <div style={{color: 'red', marginTop: '1em'}}>{error}</div>}
      {result && (
        <div style={{marginTop: '2em'}}>
          <h2>تم توليد الجولة بنجاح!</h2>
          <pre style={{background:'#f4f4f4', padding:'1em', borderRadius:'6px'}}>{JSON.stringify(result, null, 2)}</pre>
          {result.landing_page && (
            <a href={result.landing_page} target="_blank" rel="noopener noreferrer" className="button" style={{marginTop: '1em'}}>عرض الصفحة</a>
          )}
        </div>
      )}
    </div>
  );
}
