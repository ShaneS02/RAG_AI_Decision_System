import { useState } from "react";
import QueryForm from "./components/QueryForm";
import ResponseViewer from "./components/ResponseViewer";

export default function App() {
  const [response, setResponse] = useState(null);

  const handleQuerySubmit = async (query) => {
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: query }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: err.message });
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", fontFamily: "sans-serif" }}>
      <h1>Query AI</h1>
      <QueryForm onSubmit={handleQuerySubmit} />
      <ResponseViewer response={response} />
    </div>
  );
}
