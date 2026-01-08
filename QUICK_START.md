# 🚀 Quick Start Guide

This guide helps you run the **Consumer Card Spend Analytics** project locally with minimal setup.

---

## 📋 Prerequisites
Ensure the following are installed on your system:

- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

---

## 📁 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Abhinav-1710/consumer-card-spend-analytics.git
cd consumer-card-spend-analytics

Backend Setup
cd backend
python -m venv venv

Activate virtual environment:

Windows:
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

Install Backend Dependencies
pip install -r requirements.txt

Start Backend Server
uvicorn app.main:app --reload

Backend will be available at:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

Frontend Setup (React)

install Frontend Dependencies

Open a new terminal:
cd frontend
npm install

Start Frontend Application:
npm run dev

Frontend will be available at:
http://localhost:5173
