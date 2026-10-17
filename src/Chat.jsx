import { useState } from "react";

export default function Chat({ userEmail }) {
  const [message, setMessage] = useState("");
  const [replies, setReplies] = useState([]);

  async function send() {
    console.log("user message from", userEmail, message);
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: userEmail, message }),
    });
    const data = await res.json();
    setReplies([...replies, { you: message, bot: data.reply }]);
    setMessage("");
  }

  return (
    <div className="chat-window">
      {replies.map((r, i) => (
        <div key={i}>
          <p>You: {r.you}</p>
          <p>Bot: {r.bot}</p>
        </div>
      ))}
      <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type your question" />
      <button onClick={send}>Send</button>
    </div>
  );
}
