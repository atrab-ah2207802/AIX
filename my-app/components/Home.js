"use client";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import FileUploader from "./FileUploader";

export default function Home() {
  const { t } = useTranslation();

  useEffect(() => {
    const handleMouseMove = (e) => {
      const x = e.clientX / window.innerWidth;
      const y = e.clientY / window.innerHeight;
      document.body.style.backgroundPosition = `${x * 100}% ${y * 100}%`;
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div>
      <div className="overlay"></div>

      <main className="main-section">
        <div className="intro">
          <h2>{t("hero_title")}</h2>
          <p>{t("hero_text")}</p>
          <FileUploader />
        </div>
      </main>

      <section className="about">
        <h3>{t("about_title")}</h3>
        <p>{t("about_text")}</p>
      </section>
    </div>
  );
}
