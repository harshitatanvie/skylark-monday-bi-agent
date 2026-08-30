# Skylark Drones — Monday.com Business Intelligence Agent

An AI-powered, production-quality Business Intelligence Agent built for founders and executives to query live sales pipelines, revenue metrics, work order execution, operational performance, and cross-board intelligence using natural language.

---

## 📌 Overview

This project is a full-stack evaluation prototype for the **Full Stack Developer** position at **Skylark Drones**. It bridges real-time Monday.com board data (Deals & Work Orders) with a deterministic business intelligence calculation engine and a conversational executive interface.

### Key Highlights
- **Zero Hallucination Metrics**: Financial totals, counts, averages, and status metrics are calculated deterministically in Python/Pandas—never fabricated by the LLM.
- **Messy Data Resilience**: Handles missing dates, varied sector spellings (`Energy`, `infra`, `AGRI-TECH`), dirty currency values (`₹2.5 Cr`, `₹75,00,000`), and incomplete records with explicit Data Quality transparency.
- **Dual Mode Execution**: Runs out-of-the-box in **Demo Mode** with realistic messy datasets or integrates directly with live **Monday.com GraphQL APIs**.
- **Modern Executive UI**: Sleek React + Vite + Tailwind CSS dashboard with Recharts visualizations, interactive KPI cards, Data Quality drawer, step-by-step loading state, and 1-click **Leadership Update** generation.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        React + Vite Frontend                           │
│   (Conversational Dashboard, KPI Cards, Recharts Visuals, DQ Drawer)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTP / JSON API
┌──────────────────────────────────▼─────────────────────────────────────┐
│                        FastAPI Backend Service                         │
│ ┌───────────────────┐ ┌─────────────────────┐ ┌──────────────────────┐ │
│ │ Router (/chat,    │ │ Intent Classifier & │ │ Deterministic        │ │
│ │ /leadership, etc) │ │ LLM Synthesizer     │ │ BI Engine (Pandas)   │ │
│ └─────────┬─────────┘ └──────────┬──────────┘ └──────────┬───────────┘ │
│           │                      │                       │             │
│ ┌─────────▼──────────────────────▼───────────────────────▼───────────┐ │
│ │                Data Normalization & Resilience Layer              │ │
│ │ (Dirty text/date parser, Sector/Status normalizer, DQ metrics)    │ │
│ └────────────────────────────────┬───────────────────────────────────┘ │
│                                  │                                     │
│ ┌────────────────────────────────▼───────────────────────────────────┐ │
│ │                     Monday.com GraphQL Service                     │ │
│ │  (Read-only GraphQL API, Pagination, Fallback test dataset loader)  │ │
│ └────────────────────────────────┬───────────────────────────────────┘ │
└──────────────────────────────────┼─────────────────────────────────────┘
                                   │ GraphQL Queries
┌──────────────────────────────────▼─────────────────────────────────────┐
│                        Monday.com GraphQL API                          │
│               (Deals Board ID & Work Orders Board ID)                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Recharts, Lucide Icons, React Markdown.
- **Backend**: Python 3.14 / 3.11+, FastAPI, Pydantic v2, Pandas, Uvicorn, Pytest.
- **AI Agent**: OpenAI API (`gpt-4o-mini`) + Deterministic Rule & Intent Extractor.
- **Integration**: Monday.com GraphQL API v2 (`https://api.monday.com/v2`).

---

## 📂 Project Structure

```
skylark-monday-bi-agent/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI app entry point & CORS
│   │   ├── config.py                   # Environment settings & validation
│   │   ├── routes/
│   │   │   ├── chat.py                 # POST /api/chat
│   │   │   ├── leadership.py           # POST /api/leadership-update
│   │   │   ├── metrics.py              # GET /api/metrics/* & /api/data-quality
│   │   │   └── health.py               # GET /health & /api/monday/status
│   │   ├── services/
│   │   │   ├── monday_service.py       # Monday GraphQL client & pagination
│   │   │   ├── analytics_service.py    # Deterministic BI metrics engine
│   │   │   └── ai_service.py           # Intent parsing & insight synthesizer
│   │   ├── data/
│   │   │   ├── normalizer.py           # Sector, date, currency normalizer
│   │   │   ├── validators.py           # Data quality health score builder
│   │   │   ├── schemas.py              # Pydantic data schemas
│   │   │   └── mock_fixtures.py        # Messy mock dataset for Demo Mode
│   │   └── utils/
│   │       ├── currency.py             # INR currency formatting utilities
│   │       └── logger.py               # Structured logger
│   ├── tests/
│   │   ├── test_normalizer.py          # Normalizer unit tests
│   │   ├── test_analytics.py           # BI calculation unit tests
│   │   └── test_api.py                 # FastAPI router integration tests
│   ├── pytest.ini                      # Pytest config
│   └── requirements.txt                # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/                   # ChatFeed, MessageItem, LoadingSteps
│   │   │   ├── Dashboard/              # KPICard, AnalyticsChart, DataQualityDrawer
│   │   │   ├── Layout/                 # Header, Sidebar, ConfigModal
│   │   │   └── Leadership/             # LeadershipModal
│   │   ├── services/
│   │   │   └── api.ts                  # Axios client
│   │   ├── types/
│   │   │   └── index.ts                # TypeScript interfaces
│   │   ├── App.tsx                     # Main dashboard orchestration
│   │   ├── main.tsx                    # React entry point
│   │   └── index.css                   # Tailwind styles & Markdown rules
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docs/
│   └── decision-log.md                 # Technical decision log
├── .env.example
├── .gitignore
└── README.md
```

---

## 🛠️ Monday.com Setup Instructions

To connect the application to your live Monday.com workspace:

1. **Log in to Monday.com**: Create a free or trial Monday.com account if needed.
2. **Create Deals Board**:
   - Create a main board named `Deals`.
   - Add columns:
     - `Deal Size` / `Amount` (Numbers or Text)
     - `Sector` (Dropdown or Text)
     - `Stage` / `Status` (Status column with values like `Closed Won`, `Proposal Sent`, `Negotiation`, `Qualified Lead`, `Closed Lost`)
     - `Expected Close Date` (Date column)
3. **Create Work Orders Board**:
   - Create a board named `Work Orders`.
   - Add columns:
     - `Contract Value` (Numbers or Text)
     - `Sector` (Dropdown or Text)
     - `Status` (Status column with values like `In Progress`, `Delayed`, `Completed`, `On Hold`)
     - `Target Completion Date` (Date column)
     - `Start Date` (Date column)
4. **Obtain API Token**:
   - Go to **Avatar (Bottom Left) → Administration → API**.
   - Copy your **Personal API Token**.
5. **Obtain Board IDs**:
   - Open your `Work Orders` board in browser. The URL will contain `monday.com/boards/123456789`. Copy `123456789`.
   - Open your `Deals` board and copy its ID.
6. **Configure Environment Variables**:
   - Set `MONDAY_API_TOKEN`, `MONDAY_WORK_ORDERS_BOARD_ID`, and `MONDAY_DEALS_BOARD_ID` in `backend/.env`.

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` in your project root:

```env
# Monday.com API Credentials
MONDAY_API_TOKEN=your_monday_api_token_here
MONDAY_WORK_ORDERS_BOARD_ID=123456789
MONDAY_DEALS_BOARD_ID=987654321

# OpenAI API Key (Optional - rule-based fallback used if missing)
OPENAI_API_KEY=sk-your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Server Settings
PORT=8000
HOST=0.0.0.0
DEMO_MODE=true

# Frontend Environment
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🚀 Running Locally

### 1. Start Backend Server
```bash
# From workspace root:
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
Backend will start at `http://localhost:8000`. You can test endpoints via Swagger docs at `http://localhost:8000/docs`.

### 2. Start Frontend Server
```bash
# From workspace root:
cd frontend
npm run dev
```
Frontend will start at `http://localhost:5173`.

---

## 🧪 Running Automated Tests

The test suite validates data normalization, date parsing, BI analytics calculations, and FastAPI router endpoints.

```bash
# Run pytest suite from workspace root:
$env:PYTHONPATH="backend"
python -m pytest backend/tests -v
```

---

## 🤖 AI Agent Architecture

1. **Query Intent Classification**: The agent parses questions to detect metric targets (Pipeline, Won Revenue, Sector Comparison, Operational Delays, Ambiguity).
2. **Ambiguous Query Handling**: If a prompt like `"How is the pipeline doing?"` lacks specificity, the agent returns interactive choice chips to ask for clarification.
3. **Deterministic Analytics Execution**: Executes Python functions in `analytics_service.py` to calculate exact financial sums, averages, win rates, and sector counts.
4. **Data Quality Transparency**: Generates complete statistics on missing dates, unparsed amounts, and data health scores.
5. **Grounded Insight Synthesis**: Passes calculated numerical results into the LLM to format executive insights without allowing metric fabrication.

---

## 📊 Sample Queries to Try

- `"How is our pipeline looking this quarter?"`
- `"Which sector has the strongest pipeline?"`
- `"How much revenue have we won?"`
- `"Which projects are delayed?"`
- `"Compare Energy and Infrastructure sectors."`
- `"How is the pipeline doing?"` *(Triggers interactive clarification)*
- Click **"Leadership Update"** button in header to generate a full executive update.

---

## 🚢 Deployment Guide

### Frontend (Vercel)
1. Import repository into Vercel.
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Set Environment Variable: `VITE_API_BASE_URL=https://your-backend-service.onrender.com`

### Backend (Render / Railway)
1. Create a Python Web Service on Render / Railway.
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set Environment Variables: `MONDAY_API_TOKEN`, `MONDAY_WORK_ORDERS_BOARD_ID`, `MONDAY_DEALS_BOARD_ID`, `OPENAI_API_KEY`.

---

## 📝 AI Tools Disclosure
Assisted by Gemini 3.6 Flash for rapid architectural prototyping, TypeScript type generation, and documentation drafting. All core BI analytics, normalization logic, and test suites were strictly verified against actual execution outputs.
