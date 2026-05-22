import React from "react";

export default function SnippetList({ items }) {
  if (!items?.length) return <div className="card">No connections yet.</div>;
  return (
    <div className="card">
      <h3>Related Sections</h3>
      <ul className="snippet-list">
        {items.map((s, i) => (
          <li key={i}>
            <strong>{s.section_heading}</strong> · {s.doc_title} p{s.page}
            <p>{s.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
