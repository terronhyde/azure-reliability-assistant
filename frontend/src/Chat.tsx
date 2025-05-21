import React, { useState } from "react";

const Chat: React.FC = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) throw new Error("Failed to get response");
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="w-full max-w-lg bg-white rounded-xl shadow-lg p-8 flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-2 text-gray-800">
          Azure Reliability Assistant
        </h1>
        <p className="mb-8 text-gray-500 text-center">
          Welcome! Ask any question about your documents below.
        </p>
        <form
          onSubmit={handleAsk}
          className="w-full flex flex-col items-center"
        >
          <textarea
            className="w-full border border-gray-300 rounded-lg p-3 mb-4 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="Type your question here..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
            rows={2}
            style={{ minHeight: 48 }}
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            disabled={loading || !query.trim()}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>
        {answer && (
          <div className="mt-8 w-full p-4 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 whitespace-pre-line">
            <strong>Answer:</strong>
            <div>{answer}</div>
          </div>
        )}
        {error && <div className="mt-4 text-red-500">{error}</div>}
      </div>
    </div>
  );
};

export default Chat;
