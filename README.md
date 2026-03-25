# Riba de Rivers 🌊

A high-performance, Full-Stack vacation rental platform built with **Vanilla JavaScript** and **Flask**, designed for seamless user experience and robust booking management.

![Status](https://img.shields.io/badge/Status-Active-success)
![Vanilla JS](https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow)
![Backend](https://img.shields.io/badge/Backend-Flask-lightgrey)

## 🚀 Overview
Riba de Rivers is a professional-grade web application for managing vacation rentals. Unlike standard template-based sites, this project focuses on **software engineering fundamentals**, featuring a custom-built internationalization engine, a real-time pricing logic, and secure payment integrations.

## 🛠️ Key Technical Features

### 1. Modular Vanilla JS Architecture
The application follows a **page-scoped modular pattern**. Each page manages its own state and logic independently, ensuring high performance and low bundle sizes by avoiding heavy frontend frameworks.

### 2. Custom i18n Engine (ES/EN/FR)
Engineered a trilingual system using **i18next**:
- **Zero-latency translations:** Inline resource bundles for instant switching.
- **Persistence:** User language preference is stored via `localStorage`.
- **Locale-aware formatting:** Dynamic date formatting using the `Intl.DateTimeFormat` API.

### 3. Dynamic Pricing & Resilient Data Layer
Developed a real-time pricing engine that calculates:
- **Base nightly rates:** Fetched from the **Hosthub API**.
- **Conditional fees:** Automated calculation for cleaning, pets, and extra guests.
- **Resilience:** Implemented a TTL-based caching strategy with stale-data fallback to ensure the app remains functional even during API downtime.

### 4. Secure Booking Pipeline
Integrated a full-stack payment flow:
- **Stripe Checkout:** Secure handling of financial transactions.
- **Server-side Validation:** Prices are recalculated and validated on the backend (Flask) to prevent client-side tampering.

### 5. Geospatial & Media Experience
- **MapLibre GL:** WebGL-based vector map rendering for precise property location.
- **Fancybox v5:** Grouped media gallery with lazy-loaded assets for optimized Core Web Vitals.

## 💻 Tech Stack
- **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3, MapLibre GL, Fancybox, i18next.
- **Backend:** Python (Flask).
- **APIs/Tools:** Stripe, Hosthub, Git/GitHub, Vercel.

## 🎓 Academic Context
This project serves as a practical application of the computer science fundamentals (algorithms, data structures, and memory management) mastered during **Harvard's CS50x**.

---
*Developed by Andres Rios — [LinkedIn](https://linkedin.com/in/andres-rios-55325a66)*