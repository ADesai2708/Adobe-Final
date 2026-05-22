export function renderPDF({ containerId, url, fileName, adobeKey }) {
  return new Promise((resolve, reject) => {
    if (!window.AdobeDC) return reject(new Error("Adobe SDK not loaded"));
    const view = new window.AdobeDC.View({
      clientId: adobeKey,
      divId: containerId,
    });
    const preview = view.previewFile(
      { content: { location: { url } }, metaData: { fileName } },
      { embedMode: "FULL_WINDOW" }
    );
    preview.then((viewer) => resolve(viewer));
  });
}
