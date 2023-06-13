import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import liff from "@line/liff";
import { liffId } from "./secret";
import "../src/index.css";
import { Helmet, HelmetProvider } from "react-helmet-async";

liff.init({ liffId: liffId })
    .then(() => {
        const root = ReactDOM.createRoot(
            document.getElementById("root") as HTMLElement
        );
        root.render(
            <React.StrictMode>
                <HelmetProvider>
                    <Helmet>
                        <link
                            rel="stylesheet"
                            href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@40,400,0,0"
                        />
                    </Helmet>
                    <App />
                </HelmetProvider>
            </React.StrictMode>
        );
    })
    .catch((e) => {
        alert(`LIFF error: ${e.message}`);
    });
