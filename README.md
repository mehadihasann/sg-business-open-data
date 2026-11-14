# 📈 Singapore's Business Formation Trends
### An Empirical Analysis of ACRA Data (1990–2025)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg)

## 📌 Executive Summary
Understanding the shifting dynamics of a nation's business landscape is crucial for strategic decision-making. This project serves as an **interactive business intelligence dashboard** that analyzes over three decades of business registration data from the Accounting and Corporate Regulatory Authority (ACRA) of Singapore. 

By examining historical trends, this tool identifies which industries are expanding, which are contracting, and provides actionable insights into long-term economic resilience.

## 💡 Business Problem & Objectives
The Singaporean economy is highly dynamic, constantly pivoting towards new technologies and services. However, traditional sectors (like Food & Beverage and Retail) remain vital. 

**The objective of this analysis is to answer:**
1. Which industries have demonstrated the highest Compound Annual Growth Rate (CAGR) over the last 30 years?
2. Which sectors experienced the most severe single-year contractions, such as during economic downturns?
3. How does the volume of business formations differ between high-growth sectors and legacy industries?

## 🛠️ Technical Architecture & Methodology
This project demonstrates a complete, end-to-end data pipeline:

* **1. Data Ingestion:** Connected securely to the `data.gov.sg` API (using environment variables for API key management) to extract the raw "Formation of All Business Entities" dataset.
* **2. Data Wrangling:** Utilized **Pandas** to reshape the data from a "wide" format (years as columns) to a "long" format, clean missing values, and normalize industry names.
* **3. Database Management:** Loaded the cleaned dataset into a local **SQLite** database (`business_data.db`). This ensures fast querying and prevents API rate limits for public users.
* **4. Business Intelligence Engine:** Built custom Python functions to dynamically calculate:
   * **CAGR (Compound Annual Growth Rate):** To measure long-term growth.
   * **Year-over-Year (YoY) Deltas:** To identify market surges and contractions.
* **5. Interactive Dashboard:** Developed with **Streamlit** and **Plotly** for a responsive, modern user experience.

## 🚀 Key Features of the Dashboard
* **Dynamic Filtering:** Users can select custom year ranges and multiselect specific industries to compare.
* **KPI Summary Cards:** Instantly view total registration volumes, latest year performance, and total growth metrics.
* **Line Chart Analysis:** Track historical trends with hover-enabled, unified Plotly tooltips.
* **Automated Market Intelligence:** The dashboard dynamically reads the data to generate written insights, automatically highlighting the "Market Volume Leader," the "Largest Surge," and the "Sharpest Contraction."

## 🌐 Live Demo
*(Link will be added here after Streamlit deployment)*

## 📊 Data Source & Acknowledgements
* Data provided by the **Accounting and Corporate Regulatory Authority (ACRA)** and compiled by the **Singapore Department of Statistics (SingStat)**.
* Retrieved via the open data platform: [data.gov.sg](https://data.gov.sg).

---
*Developed as part of a Master's Application Portfolio for Digital Business & AI Management.*
