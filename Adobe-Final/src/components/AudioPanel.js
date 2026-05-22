import React from "react";

export default function AudioPanel({ url, onCreate, busy }) {
  return (
    <div className="card">
      <button onClick={onCreate} disabled={busy}>
        {busy ? "Synthesizing…" : "Create Podcast"}
      </button>
      {url && <audio controls src={url} />}
    </div>
  );
}
