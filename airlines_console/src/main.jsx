import React from "react";
import ReactDOM from "react-dom/client"; // React 18
import UploadPDF from "./UploadPDF.jsx";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <UploadPDF />
  </React.StrictMode>
);
