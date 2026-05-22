import React, { useRef, useState } from "react";

export default function UploadBar({ onUpload }) {
  const ref = useRef();
  const [busy, setBusy] = useState(false);

  async function handleClick() {
    const files = ref.current.files;
    if (!files.length) return;
    setBusy(true);
    await onUpload(files);
    setBusy(false);
  }

  return (
    <div className="card upload-bar">
      <input ref={ref} type="file" multiple accept="application/pdf" />
      <button onClick={handleClick} disabled={busy}>
        {busy ? "Uploading…" : "Upload PDFs"}
      </button>
    </div>
  );
}
