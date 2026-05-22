import React, { useEffect } from "react";
import { renderPDF } from "../lib/adobeEmbed";

export default function PdfStage({ currentUrl, onSelection }) {
  useEffect(() => {
    if (!currentUrl) return;
    renderPDF({
      containerId: "pdf-stage",
      url: currentUrl,
      fileName: currentUrl.split("/").pop(),
      adobeKey: process.env.REACT_APP_ADOBE_EMBED_API_KEY,
    }).then((viewer) => {
      viewer.getAPIs().then((api) => {
        api.enableTextSelection(true);
        api.registerCallback(
          window.AdobeDC.View.Enum.CallbackType.TEXT_SELECTED,
          (e) => {
            const selected = (e.data?.selections || [])
              .map((s) => s.text)
              .join(" ");
            if (selected) onSelection(selected);
          },
          {}
        );
      });
    });
  }, [currentUrl]);

  return <div id="pdf-stage" className="pdf-container" />;
}
