# Technical Decision Log: Monday.com Business Intelligence Agent

*Author: Full-Stack AI Engineer Candidate*  
*Project: Skylark Drones - Monday.com Business Intelligence Agent Evaluation*

---

## 1. Key Assumptions
- **Monday.com Board Schema Flexibility**: Board structures on Monday.com vary between workspaces. Column IDs can differ while titles remain conceptually fixed (e.g., "Deal Size", "Contract Value", "Stage", "Expected Close Date"). We assumed a dynamic title-based mapping layer with fallbacks.
- **Read-Only Operation Guarantee**: The BI Agent operates exclusively in read-only mode to prevent accidental mutation of active enterprise sales or operational records.
- **Dual Mode Requirement**: Evaluators may test the prototype without active Monday.com API keys or board IDs. An instant Demo Mode backed by authentic messy test dataset is provided so the app runs out of the box without setup friction.

---

## 2. Architecture & Tech Stack Rationale
We selected a clean decoupled 3-tier architecture: **React + Vite (Frontend) → FastAPI (Backend Router & BI Engine) → Monday.com GraphQL API / LLM**.

### Why FastAPI?
- **High Performance & Async IO**: Python is the industry standard for analytics (Pandas, Pydantic) and AI integration. FastAPI provides lightweight, asynchronous request handling with zero-overhead OpenAPI schema validation.
- **Data Model Integrity**: Native integration with Pydantic ensures strong typing across data normalization and API payloads.

### Why React + Vite + Tailwind CSS?
- **Executive BI Aesthetics**: React enables immediate UI state reactivity (step-by-step query loading indicators, Recharts visual rendering, sliding drawer overlays).
- **Lightweight Bundling**: Vite delivers sub-second hot reloading during development and compact production assets (built clean in <4s).

---

## 3. Monday.com GraphQL API vs MCP
- We directly implemented Monday.com's official GraphQL v2 API (`boards(ids: [...]) { items_page { cursor items ... } }`).
- Direct GraphQL integration guarantees fine-grained control over pagination (`cursor`), query payload size, field filtering, and rate limits without relying on intermediate protocols or external runtime dependencies.

---

## 4. Messy Data Resilience Strategy
Raw enterprise data in Monday.com is inherently dirty. We built a multi-stage normalization pipeline in `backend/app/data/normalizer.py`:
1. **Sector Normalization**: Variations like `"Energy"`, `"energy"`, `" ENERGY "`, `"energy sector"`, `"Solar / Energy"` are mapped deterministically via keyword matching to canonical sectors (`Energy`, `Infrastructure`, `Construction`, `Mining`, `Agriculture`, `Utilities`, `Defense`).
2. **Multi-Format Safe Date Parser**: Parses `YYYY-MM-DD`, `DD/MM/YYYY`, `DD-Mon-YYYY`, `MMM DD, YYYY`, and ISO strings. If unparseable (e.g., `"TBD"`, `"N/A"`), the system logs a data quality flag, assigns `None`, and avoids crashing.
3. **Monetary Amount Cleaning**: Extracts numbers from mixed currency formats (`₹2,50,00,000`, `₹1.8 Cr`, `₹75 Lakhs`).
4. **Data Quality Transparency**: Aggregates health metrics into a `DataQualityReport` (health score %, count of unparsed dates, missing amounts, unmapped sectors). Every answer explicitly informs the user if metrics are affected by missing values.

---

## 5. Zero-Hallucination AI Agent Pipeline
To ensure 100% numerical correctness:
- **LLMs are NEVER allowed to perform mathematical calculations**.
- Query processing follows a structured pipeline:
  ```
  User Question ──► Intent & Tool Selection ──► Python/Pandas BI Engine ──► Structured Output + Data Quality ──► LLM Insight Synthesis ──► UI Response
  ```
- All totals, averages, counts, win rates, and delay percentages are calculated deterministically in `analytics_service.py`.
- Grounded numerical context is injected into the LLM prompt solely for executive summarization, nuance highlighting, and risk identification.

---

## 6. Interpretation of "Leadership Update"
We implemented the optional requirement as a dedicated, high-impact executive feature. It synthesizes cross-board metrics (Open Pipeline, Won Revenue, Active Work Orders, Delayed Work Orders, Strongest Sector, Data Reliability) into a structured 1-page markdown report formatted specifically for CEO/Founder review or board meeting distribution.

---

## 7. Security & Performance Decisions
- **Credential Protection**: API tokens (`MONDAY_API_TOKEN`, `OPENAI_API_KEY`) are kept strictly on the backend. No secrets are exposed to the browser client.
- **Lightweight Caching**: Board data is cached in memory during active query processing to eliminate redundant GraphQL calls while maintaining Monday.com as the live source of truth.

---

## 8. Trade-offs & Future Improvements
- **Write Actions**: Current implementation is strictly read-only as required. Future versions could support draft creation of follow-up tasks on Monday.com.
- **LLM Provider Flexibility**: Built with OpenAI `gpt-4o-mini` with rule-based fallback. Could be extended to support Anthropic Claude or local Ollama instances.
- **Advanced Forecasting**: Current quarterly forecasting relies on expected close dates. Machine learning deal-velocity scoring could enhance forecast precision.
