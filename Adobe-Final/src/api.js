const BASE_URL = process.env.REACT_APP_BACKEND || "http://localhost:8000";
const API_BASE = `${BASE_URL}/api`;

// Original extractHeadings function
export async function extractHeadings(file) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${BASE_URL}/extract-headings`, {
    method: "POST",
    body: fd,
  });
  return res.json();
}

// File upload function
export async function uploadFiles(files) {
  const fd = new FormData();
  for (const f of files) fd.append("files", f);
  const res = await fetch(`${API_BASE}/upload`, { 
    method: "POST", 
    body: fd 
  });
  return res.json();
}

// Get snippets function
export async function getSnippets(selection) {
  const res = await fetch(`${API_BASE}/select`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ selection }),
  });
  return res.json();
}

// Consolidated getInsights function (handles both FormData and JSON variants)
export async function getInsights(selectionOrText, documentsOrSnippets) {
  // Check if this is the original FormData version (selectedText, documents)
  if (typeof selectionOrText === "string" && Array.isArray(documentsOrSnippets)) {
    const fd = new FormData();
    fd.append("selected_text", selectionOrText);
    fd.append("documents", documentsOrSnippets.join(","));
    const res = await fetch(`${BASE_URL}/insights`, {
      method: "POST",
      body: fd,
    });
    return res.json();
  }
  // Otherwise use the JSON version (selection, snippets)
  else {
    const res = await fetch(`${API_BASE}/insights`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        selection: selectionOrText, 
        snippets: documentsOrSnippets 
      }),
    });
    return res.json();
  }
}

export async function createPodcast(selection, insights, snippets) {
  const res = await fetch(`${API_BASE}/podcast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ selection, insights, snippets }),
  });
  return res.json();
}