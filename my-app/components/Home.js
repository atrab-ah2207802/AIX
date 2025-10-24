"use client";
import React, { useEffect } from "react";
import FileUploader from "./FileUploader";      

export default function Home() {
  // Dynamic background movement
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

      <header className="navbar">
        <h1 className="logo">AI Contract Insight</h1>
      </header>

      <main className="main-section">
        <div className="intro">
          <h2>Transform How You Understand Contracts</h2>
          <p>
            Upload or paste your legal documents to get instant, AI-driven insights —
            clause detection, risk assessment, and key obligation summaries.
          </p>
            <div className="features-list mt-90"></div>

          <FileUploader></FileUploader>
        </div>
      </main>

      <section className="about">
        <h3>About the Platform</h3>
        <p>
          This platform leverages advanced AI models to analyze legal contracts in real time.
          It identifies crucial clauses, highlights potential risks, and summarizes obligations,
          making complex agreements easier to understand for individuals and organizations alike.
        </p>
      </section>
    </div>
  );
}
