import React, { useState, useCallback } from "react";
import "./App.css";
import UploadBar from "./components/UploadBar";
import PdfStage from "./components/PdfStage";
import SnippetList from "./components/SnippetList";
import InsightBulb from "./components/InsightBulb";
import AudioPanel from "./components/AudioPanel";
import Toast from "./components/Toast";
import {
  uploadFiles,
  getSnippets,
  getInsights,
  extractHeadings,
  createPodcast,
} from "./api";

const BACKEND = process.env.REACT_APP_BACKEND || "http://localhost:8000";

function App() {
  const [files, setFiles] = useState([]);
  const [currentUrl, setCurrentUrl] = useState("");
  const [currentName, setCurrentName] = useState("");
  const [headings, setHeadings] = useState([]);
  const [snippets, setSnippets] = useState([]);
  const [insights, setInsights] = useState(null);
  const [podcastUrl, setPodcastUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [backendOk, setBackendOk] = useState(null);
  const [toast, setToast] = useState("");
  const useEmbed = Boolean(
    process.env.REACT_APP_ADOBE_EMBED_API_KEY &&
    process.env.REACT_APP_ADOBE_EMBED_API_KEY !== "YOUR_CLIENT_ID"
  );

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(""), 4000);
  };

  const checkBackend = async () => {
    try {
      const res = await fetch(`${BACKEND}/health`);
      const data = await res.json();
      setBackendOk(data.status === "healthy");
    } catch {
      setBackendOk(false);
    }
  };

  React.useEffect(() => {
    checkBackend();
  }, []);

  const handleUpload = async (fileList) => {
    try {
      const result = await uploadFiles(fileList);
      if (!result.files?.length) {
        showToast("No PDF files uploaded.");
        return;
      }
      setFiles(result.files);
      const first = result.files[0];
      setCurrentUrl(first.url);
      setCurrentName(first.name);
      showToast(`Uploaded ${result.count} PDF(s).`);
    } catch (err) {
      console.error(err);
      showToast("Upload failed. Is the backend running on port 8000?");
    }
  };

  const handleExtractHeadings = async () => {
    if (!files.length) {
      showToast("Upload a PDF first.");
      return;
    }
    setBusy(true);
    try {
      const blob = await fetch(currentUrl).then((r) => r.blob());
      const file = new File([blob], currentName || "document.pdf", {
        type: "application/pdf",
      });
      const data = await extractHeadings(file);
      if (data.success) {
        setHeadings(data.headings || []);
        showToast(`Found ${(data.headings || []).length} headings.`);
      } else {
        showToast(data.error || "Heading extraction failed.");
      }
    } catch (err) {
      console.error(err);
      showToast("Could not extract headings.");
    } finally {
      setBusy(false);
    }
  };

  const handleSelection = useCallback(
    async (selection) => {
      if (!selection?.trim()) return;
      setBusy(true);
      try {
        const snippetRes = await getSnippets(selection);
        const list = snippetRes.snippets || [];
        setSnippets(list);

        const insightRes = await getInsights(selection, list);
        setInsights(insightRes.insights || insightRes);
      } catch (err) {
        console.error(err);
        showToast("Could not analyze selection.");
      } finally {
        setBusy(false);
      }
    },
    []
  );

  const handleCreatePodcast = async () => {
    setBusy(true);
    try {
      const result = await createPodcast("", insights, snippets);
      if (result.url) setPodcastUrl(result.url);
      else showToast(result.message || "Podcast API not configured.");
    } catch (err) {
      console.error(err);
      showToast("Podcast creation failed.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Adobe Hackathon — Document Intelligence</h1>
        <p className="subtitle">
          Upload PDFs, extract structure, and get persona-based insights
        </p>
        <p className="status-line">
          Backend:{" "}
          {backendOk === null
            ? "checking..."
            : backendOk
            ? "connected"
            : "offline — run python backend/app.py"}
        </p>
      </header>

      <UploadBar onUpload={handleUpload} />

      {files.length > 0 && (
        <div className="card file-picker">
          <label>Open document: </label>
          <select
            value={currentUrl}
            onChange={(e) => {
              const f = files.find((x) => x.url === e.target.value);
              setCurrentUrl(e.target.value);
              setCurrentName(f?.name || "");
            }}
          >
            {files.map((f) => (
              <option key={f.id} value={f.url}>
                {f.name}
              </option>
            ))}
          </select>
          <button onClick={handleExtractHeadings} disabled={busy}>
            Extract headings (Round 1A)
          </button>
        </div>
      )}

      {currentUrl && (
        <div className="pdf-wrapper card">
          {useEmbed ? (
            <PdfStage currentUrl={currentUrl} onSelection={handleSelection} />
          ) : (
            <iframe
              title="PDF viewer"
              src={currentUrl}
              className="pdf-iframe"
            />
          )}
          {!useEmbed && (
            <p className="hint">
              Select text using Round 1B: paste a passage below, or add an Adobe
              Embed API key in .env for in-PDF selection.
            </p>
          )}
          {!useEmbed && (
            <textarea
              className="selection-input"
              placeholder="Paste highlighted text here to find related sections..."
              rows={3}
              onBlur={(e) => {
                if (e.target.value.trim()) handleSelection(e.target.value);
              }}
            />
          )}
        </div>
      )}

      {headings.length > 0 && (
        <div className="card">
          <h3>Document outline</h3>
          <ul>
            {headings.map((h, i) => (
              <li key={i}>
                <strong>{h.level}</strong> p{h.page + 1}: {h.text}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid-2">
        <SnippetList items={snippets} />
        <div>
          <InsightBulb insights={insights} />
          <AudioPanel
            url={podcastUrl}
            onCreate={handleCreatePodcast}
            busy={busy}
          />
        </div>
      </div>

      {toast && <Toast message={toast} />}
    </div>
  );
}

export default App;
