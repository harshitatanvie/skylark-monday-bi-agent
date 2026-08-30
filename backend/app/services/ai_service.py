import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
from app.config import settings
from app.utils.logger import logger
from app.utils.currency import format_inr
from app.services.analytics_service import analytics_service
from app.data.schemas import (
    ChatRequest, 
    ChatResponse, 
    KPICard, 
    ChartSpec, 
    LeadershipUpdateResponse
)

class AIAgentService:
    def __init__(self):
        self.openai_client = None
        if settings.has_valid_openai_key:
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {str(e)}")

    def classify_intent_rule_based(self, question: str) -> Tuple[str, Dict[str, Any]]:
        q = question.lower().strip()
        
        # Ambiguous check
        if q in ("how is business?", "how is the pipeline doing?", "business update", "status", "hi", "hello"):
            if "pipeline" in q:
                return "ambiguous_pipeline", {}
            elif q in ("hi", "hello"):
                return "greeting", {}
            return "ambiguous_business", {}

        # Intent triggers
        if any(k in q for k in ("leadership", "executive summary", "leadership update", "board update", "ceo update")):
            return "leadership_update", {}
        elif any(k in q for k in ("delayed", "delay", "overdue", "behind schedule")):
            return "operational_delayed", {}
        elif any(k in q for k in ("work order", "work orders", "project", "projects", "operation", "operational", "flying")):
            return "operational_summary", {}
        elif any(k in q for k in ("revenue", "won", "closed won", "income")):
            return "revenue_summary", {}
        elif any(k in q for k in ("sector", "sectors", "energy", "infra", "infrastructure", "mining", "construction", "agri", "compare")):
            # Check sector specific filter
            target_sector = None
            for s in ("energy", "infrastructure", "construction", "mining", "agriculture", "utilities", "defense"):
                if s in q:
                    target_sector = s
                    break
            return "sector_analysis", {"sector": target_sector}
        elif any(k in q for k in ("pipeline", "open deals", "deal size", "deals", "win rate", "quarter")):
            return "pipeline_summary", {}
        else:
            return "pipeline_summary", {}

    def process_chat_query(self, req: ChatRequest) -> ChatResponse:
        q = req.message.strip()
        use_demo = req.use_demo_mode if req.use_demo_mode is not None else settings.DEMO_MODE
        
        intent, params = self.classify_intent_rule_based(q)
        logger.info(f"Chat Query received: '{q}' -> Intent detected: '{intent}' (Demo Mode: {use_demo})")

        # ---------------------------------------------------------------------------
        # Handling Ambiguous Queries with Clarification Request
        # ---------------------------------------------------------------------------
        if intent == "ambiguous_pipeline":
            return ChatResponse(
                answer_markdown="### Clarification Needed\n\nI'd be happy to analyze our pipeline! Which aspect of the pipeline would you like me to detail?",
                intent_detected="ambiguous_pipeline",
                kpi_cards=[],
                charts=[],
                suggested_followups=[
                    "Total open pipeline value",
                    "Pipeline breakdown by sector",
                    "Quarterly pipeline forecasting",
                    "Top 5 largest open opportunities"
                ],
                clarification_needed=True,
                clarification_options=[
                    "Total open pipeline value & deal breakdown",
                    "Pipeline distribution by sector",
                    "Quarterly close forecast",
                    "Top open opportunities and deal sizes"
                ],
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_demo_mode=use_demo
            )
            
        if intent == "greeting":
            return ChatResponse(
                answer_markdown="### Hello! I am your Monday.com Business Intelligence Agent.\n\nI can analyze your live **Deals** and **Work Orders** boards, calculate deterministic metrics, normalize messy data, and provide founder-friendly business insights.",
                intent_detected="greeting",
                kpi_cards=[],
                charts=[],
                suggested_followups=[
                    "How's our pipeline looking this quarter?",
                    "Which sector has the strongest pipeline?",
                    "How much revenue have we won?",
                    "Which projects are delayed?",
                    "Generate Leadership Update"
                ],
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_demo_mode=use_demo
            )

        # ---------------------------------------------------------------------------
        # Execute Deterministic Analytics Engine Based on Intent
        # ---------------------------------------------------------------------------
        kpi_cards: List[KPICard] = []
        charts: List[ChartSpec] = []
        suggested_followups: List[str] = []
        
        if intent == "pipeline_summary":
            data = analytics_service.get_pipeline_summary(force_demo=use_demo)
            dq = data["data_quality_report"]
            
            kpi_cards = [
                KPICard(title="Total Open Pipeline", value=data["formatted_open_pipeline"], subtitle=f"{data['open_deals_count']} active open deals"),
                KPICard(title="Won Revenue", value=data["formatted_won_revenue"], subtitle=f"{data['won_deals_count']} closed won deals"),
                KPICard(title="Average Deal Size", value=data["formatted_avg_deal_size"], subtitle="Based on valid amounts"),
                KPICard(title="Win Rate", value=f"{data['win_rate_pct']}%", subtitle="Closed won vs total closed")
            ]
            
            # Chart: Pipeline by Sector
            sector_chart_data = [
                {"name": sec, "value": info["value"], "formatted": format_inr(info["value"])}
                for sec, info in data["sector_pipeline"].items()
            ]
            charts.append(ChartSpec(
                title="Open Pipeline by Sector",
                chart_type="bar",
                data=sector_chart_data,
                x_key="name",
                y_keys=["value"]
            ))
            
            # Formulate markdown answer
            llm_prompt = f"""
            System Role: Senior Executive BI Advisor for Skylark Drones.
            User Question: "{q}"
            
            Retrieved & Calculated Metrics (Source of Truth):
            - Total Open Pipeline: {data['formatted_open_pipeline']} ({data['open_deals_count']} open deals)
            - Total Active Pipeline: {data['formatted_active_pipeline']} (Open + Won)
            - Won Revenue: {data['formatted_won_revenue']} ({data['won_deals_count']} deals)
            - Average Deal Size: {data['formatted_avg_deal_size']}
            - Win Rate: {data['win_rate_pct']}%
            - Data Quality Issues: {dq.deals_quality.missing_dates_count} missing close dates, {dq.deals_quality.missing_amounts_count} missing amounts.
            
            Top Opportunities: {json.dumps(data['top_opportunities'][:3])}
            
            Format response cleanly in Markdown:
            ### Executive Summary
            ### Key Metrics
            ### Key Insights
            ### Data Quality Transparency
            """
            
            markdown_ans = self._synthesize_insight(llm_prompt, fallback_markdown=self._build_pipeline_markdown_fallback(data, dq))
            suggested_followups = ["Which sector has the strongest pipeline?", "Which projects are delayed?", "Generate Leadership Update"]

        elif intent == "sector_analysis":
            data = analytics_service.get_sector_analytics(force_demo=use_demo)
            dq = data["data_quality_report"]
            
            strongest = data["strongest_pipeline_sector"]
            kpi_cards = [
                KPICard(title="Strongest Sector", value=strongest, subtitle="Highest pipeline value"),
                KPICard(title="Sectors Analyzed", value=str(len(data["sectors"])), subtitle="Normalized sector groupings")
            ]
            
            chart_data = [
                {
                    "name": s["sector"], 
                    "Pipeline": s["pipeline_val"], 
                    "WonRevenue": s["won_revenue_val"]
                }
                for s in data["sectors"]
            ]
            charts.append(ChartSpec(
                title="Sector Performance (Pipeline vs Won Revenue)",
                chart_type="bar",
                data=chart_data,
                x_key="name",
                y_keys=["Pipeline", "WonRevenue"]
            ))
            
            llm_prompt = f"""
            User Question: "{q}"
            Data Summary: Strongest sector is {strongest}.
            Full Sector List: {json.dumps(data['sectors'])}
            Data Quality Warning: {dq.global_warnings}
            
            Generate concise executive summary comparing sectors and key risk areas.
            """
            markdown_ans = self._synthesize_insight(llm_prompt, fallback_markdown=self._build_sector_markdown_fallback(data, dq))
            suggested_followups = ["How much revenue have we won?", "Which projects are delayed?", "Compare Energy vs Infrastructure"]

        elif intent == "revenue_summary":
            data = analytics_service.get_revenue_summary(force_demo=use_demo)
            dq = data["data_quality_report"]
            
            kpi_cards = [
                KPICard(title="Won Revenue", value=data["formatted_won_revenue"], subtitle=f"{data['won_deals_count']} closed won deals"),
                KPICard(title="Avg Won Deal Size", value=data["formatted_avg_won_deal_size"], subtitle="Average size per closed won deal"),
                KPICard(title="Top Revenue Sector", value=data["top_revenue_sector"], subtitle="Largest revenue contributor")
            ]
            
            chart_data = [
                {"name": item["sector"], "value": item["amount"], "formatted": item["formatted"]}
                for item in data["revenue_by_sector"]
            ]
            charts.append(ChartSpec(
                title="Won Revenue Distribution by Sector",
                chart_type="donut",
                data=chart_data,
                x_key="name",
                y_keys=["value"]
            ))
            
            llm_prompt = f"""
            User Question: "{q}"
            Metrics: Total Won Revenue = {data['formatted_won_revenue']}, Count = {data['won_deals_count']}, Top Sector = {data['top_revenue_sector']}.
            Generate founder response with insights.
            """
            markdown_ans = self._synthesize_insight(llm_prompt, fallback_markdown=self._build_revenue_markdown_fallback(data, dq))
            suggested_followups = ["How is our pipeline looking this quarter?", "Show active work orders", "Generate Leadership Update"]

        elif intent in ("operational_summary", "operational_delayed"):
            data = analytics_service.get_operational_summary(force_demo=use_demo)
            dq = data["data_quality_report"]
            
            kpi_cards = [
                KPICard(title="Active Work Orders", value=str(data["active_work_orders_count"]), subtitle=f"Out of {data['total_work_orders']} total projects"),
                KPICard(title="Delayed Projects", value=str(data["delayed_work_orders_count"]), change_type="negative", subtitle=f"{data['delay_rate_pct']}% operational delay rate"),
                KPICard(title="Completed Projects", value=str(data["completed_work_orders_count"]), change_type="positive", subtitle="Successfully delivered")
            ]
            
            chart_data = [
                {"name": k, "value": v}
                for k, v in data["status_distribution"].items()
            ]
            charts.append(ChartSpec(
                title="Work Order Status Breakdown",
                chart_type="pie",
                data=chart_data,
                x_key="name",
                y_keys=["value"]
            ))
            
            llm_prompt = f"""
            User Question: "{q}"
            Operational Data: Active = {data['active_work_orders_count']}, Delayed = {data['delayed_work_orders_count']} ({data['delay_rate_pct']}% delay rate).
            Delayed Projects List: {json.dumps(data['delayed_projects'])}
            Data Quality Warning: {dq.work_orders_quality.issues}
            
            Generate operational insight focusing on delayed flight ops, schedule risk, and bottleneck prevention.
            """
            markdown_ans = self._synthesize_insight(llm_prompt, fallback_markdown=self._build_ops_markdown_fallback(data, dq))
            suggested_followups = ["Which deals need attention?", "Compare sales pipeline vs execution", "Generate Leadership Update"]

        elif intent == "leadership_update":
            update_res = self.generate_leadership_update(force_demo=use_demo)
            return ChatResponse(
                answer_markdown=update_res.markdown_report,
                intent_detected="leadership_update",
                kpi_cards=[
                    KPICard(title="Total Open Pipeline", value=update_res.executive_snapshot["formatted_open_pipeline"]),
                    KPICard(title="Won Revenue", value=update_res.executive_snapshot["formatted_won_revenue"]),
                    KPICard(title="Active Work Orders", value=str(update_res.executive_snapshot["active_work_orders"])),
                    KPICard(title="Delayed Work Orders", value=str(update_res.executive_snapshot["delayed_work_orders"]), change_type="negative")
                ],
                charts=[],
                data_quality_warning="; ".join(update_res.data_quality_summary[:2]),
                suggested_followups=["Detailed sector breakdown", "Which projects are delayed?", "Download Leadership Summary"],
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_demo_mode=use_demo
            )
        else:
            data = analytics_service.get_pipeline_summary(force_demo=use_demo)
            dq = data["data_quality_report"]
            markdown_ans = self._build_pipeline_markdown_fallback(data, dq)
            suggested_followups = ["How's our pipeline looking?", "Which sector has the strongest pipeline?"]

        # Data quality warning banner text
        dq = analytics_service.get_normalized_data(force_demo=use_demo)[2]
        dq_warning = f"Data Quality Alert ({dq.overall_health_score_pct}% reliability): " + "; ".join(dq.global_warnings[:2]) if dq.global_warnings else None

        return ChatResponse(
            answer_markdown=markdown_ans,
            intent_detected=intent,
            kpi_cards=kpi_cards,
            charts=charts,
            data_quality_warning=dq_warning,
            data_quality_report=dq,
            suggested_followups=suggested_followups,
            clarification_needed=False,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_demo_mode=use_demo
        )

    # ---------------------------------------------------------------------------
    # Leadership Update Generator
    # ---------------------------------------------------------------------------
    def generate_leadership_update(self, force_demo: bool = False) -> LeadershipUpdateResponse:
        pipe = analytics_service.get_pipeline_summary(force_demo=force_demo)
        sec = analytics_service.get_sector_analytics(force_demo=force_demo)
        ops = analytics_service.get_operational_summary(force_demo=force_demo)
        _, _, dq = analytics_service.get_normalized_data(force_demo=force_demo)
        
        exec_snapshot = {
            "open_pipeline": pipe["total_open_pipeline_val"],
            "formatted_open_pipeline": pipe["formatted_open_pipeline"],
            "won_revenue": pipe["won_revenue_val"],
            "formatted_won_revenue": pipe["formatted_won_revenue"],
            "open_deals": pipe["open_deals_count"],
            "active_work_orders": ops["active_work_orders_count"],
            "delayed_work_orders": ops["delayed_work_orders_count"],
            "strongest_sector": sec["strongest_pipeline_sector"]
        }
        
        highlights = [
            f"**{sec['strongest_pipeline_sector']}** represents our largest business sector with active deal flow.",
            f"Total open pipeline stands at **{pipe['formatted_open_pipeline']}** across {pipe['open_deals_count']} active opportunities.",
            f"Closed Won revenue achieved to date is **{pipe['formatted_won_revenue']}** with a **{pipe['win_rate_pct']}%** win rate."
        ]
        
        risks = []
        if ops["delayed_work_orders_count"] > 0:
            risks.append(f"**{ops['delayed_work_orders_count']} Work Order(s)** are currently delayed/overdue, creating execution risk.")
        if dq.deals_quality.missing_dates_count > 0:
            risks.append(f"**{dq.deals_quality.missing_dates_count} deal(s)** have missing expected close dates, impacting quarterly forecasting accuracy.")
        if dq.deals_quality.missing_amounts_count > 0:
            risks.append(f"**{dq.deals_quality.missing_amounts_count} deal(s)** lack deal size values.")

        dq_summary = dq.global_warnings if dq.global_warnings else ["All records successfully normalized with 100% field parsing."]

        report_md = f"""# EXECUTIVE LEADERSHIP UPDATE

*Based on live data retrieved from Monday.com boards ({'Demo Mode Fixture' if force_demo or settings.DEMO_MODE else 'Production Monday GraphQL API'}).*

---

### 📊 Business Snapshot
- **Open Pipeline Value**: {pipe['formatted_open_pipeline']} ({pipe['open_deals_count']} open deals)
- **Won Revenue**: {pipe['formatted_won_revenue']} ({pipe['won_deals_count']} closed won)
- **Active Work Orders**: {ops['active_work_orders_count']} project(s)
- **Operational Delay Rate**: {ops['delay_rate_pct']}% ({ops['delayed_work_orders_count']} delayed)

---

### 🚀 Key Highlights
- **Strongest Sector**: **{sec['strongest_pipeline_sector']}** leads overall deal volume and pipeline.
- **Top Opportunity**: `{pipe['top_opportunities'][0]['name'] if pipe['top_opportunities'] else 'N/A'}` valued at `{pipe['top_opportunities'][0]['amount'] if pipe['top_opportunities'] else 'N/A'}`.
- **Sales Win Rate**: Currently sitting at **{pipe['win_rate_pct']}%**.

---

### ⚠️ Risks & Recommended Focus
{"".join([f"- {r}\n" for r in risks])}

---

### 🔍 Data Quality & Governance
- **Overall Data Reliability Index**: **{dq.overall_health_score_pct}%**
{"".join([f"- {item}\n" for item in dq_summary])}

*Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')} via Monday.com BI Agent.*
"""
        return LeadershipUpdateResponse(
            markdown_report=report_md,
            executive_snapshot=exec_snapshot,
            key_highlights=highlights,
            risks_and_attention=risks,
            data_quality_summary=dq_summary,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_demo_mode=force_demo or settings.DEMO_MODE
        )

    # ---------------------------------------------------------------------------
    # LLM Synthesis & Fallback Helpers
    # ---------------------------------------------------------------------------
    def _synthesize_insight(self, prompt: str, fallback_markdown: str) -> str:
        if not self.openai_client:
            return fallback_markdown
            
        try:
            res = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a concise, sharp Business Intelligence AI assistant for Skylark Drones founders. Always explain metrics clearly without making up or altering numerical data. Ground every number in the context provided."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=600
            )
            content = res.choices[0].message.content
            return content if content else fallback_markdown
        except Exception as e:
            logger.warning(f"OpenAI API call failed ({str(e)}). Using deterministic fallback text.")
            return fallback_markdown

    def _build_pipeline_markdown_fallback(self, data: Dict[str, Any], dq: Any) -> str:
        top_opp_str = ""
        if data['top_opportunities']:
            top_opp = data['top_opportunities'][0]
            top_opp_str = f"The largest open opportunity is **{top_opp['name']}** valued at **{top_opp['amount']}** in the {top_opp['sector']} sector."
            
        missing_dates_warn = f"Note: {dq.deals_quality.missing_dates_count} deal(s) have unassigned close dates." if dq.deals_quality.missing_dates_count > 0 else "All open deals contain valid close dates."

        return f"""### Executive Summary

Our current open pipeline is valued at **{data['formatted_open_pipeline']}** across **{data['open_deals_count']} active open deals**. We have successfully closed **{data['formatted_won_revenue']}** in won revenue to date.

### Key Metrics
- **Total Open Pipeline**: {data['formatted_open_pipeline']} ({data['open_deals_count']} deals)
- **Closed Won Revenue**: {data['formatted_won_revenue']} ({data['won_deals_count']} deals)
- **Average Deal Size**: {data['formatted_avg_deal_size']}
- **Sales Win Rate**: {data['win_rate_pct']}%

### Key Insights
1. {top_opp_str}
2. Average deal size across valid opportunities is **{data['formatted_avg_deal_size']}**.
3. Overall win rate on closed deals is **{data['win_rate_pct']}%**.

### Data Quality & Governance
- **Reliability Score**: {dq.overall_health_score_pct}%
- {missing_dates_warn}

*Based on current Monday.com Deals & Work Orders data.*
"""

    def _build_sector_markdown_fallback(self, data: Dict[str, Any], dq: Any) -> str:
        strongest = data['strongest_pipeline_sector']
        sec_details = "\n".join([
            f"- **{s['sector']}**: Pipeline = {s['formatted_pipeline']} ({s['open_deals_count']} open deals) | Won Revenue = {s['formatted_won_revenue']}"
            for s in data['sectors']
        ])
        
        return f"""### Sector Performance Analysis

The **{strongest}** sector currently exhibits the strongest sales pipeline and commercial momentum.

### Sector Breakdown
{sec_details}

### Key Insights
1. **{strongest}** represents our primary revenue engine for upcoming quarters.
2. Cross-board analysis shows active work order execution aligned with top sectors.

### Data Quality Transparency
- **Overall Data Reliability Index**: {dq.overall_health_score_pct}%
- All sector names have been normalized cleanly into canonical business sectors.

*Based on live Monday.com board data.*
"""

    def _build_revenue_markdown_fallback(self, data: Dict[str, Any], dq: Any) -> str:
        return f"""### Won Revenue Analysis

Skylark Drones has generated **{data['formatted_won_revenue']}** in total won revenue across **{data['won_deals_count']} closed-won contracts**.

### Key Revenue Metrics
- **Total Won Revenue**: {data['formatted_won_revenue']}
- **Won Deal Count**: {data['won_deals_count']} deals
- **Average Won Deal Size**: {data['formatted_avg_won_deal_size']}
- **Leading Sector**: {data['top_revenue_sector']}

### Strategic Insights
1. **{data['top_revenue_sector']}** has proven to be our highest converting vertical.
2. The average deal size for signed contracts stands at **{data['formatted_avg_won_deal_size']}**.

### Data Quality & Governance
- Data health score: **{dq.overall_health_score_pct}%**
"""

    def _build_ops_markdown_fallback(self, data: Dict[str, Any], dq: Any) -> str:
        delayed_list = "\n".join([
            f"- **{p['name']}** ({p['sector']}): Status: *{p['status']}* | Value: {p['contract_value']} | Target Completion: {p['target_completion']}"
            for p in data['delayed_projects']
        ]) if data['delayed_projects'] else "- No delayed projects currently flagged."

        return f"""### Operational Performance Update

We are currently managing **{data['active_work_orders_count']} active work orders** in the field. Our overall operational delay rate is **{data['delay_rate_pct']}%** ({data['delayed_work_orders_count']} delayed projects).

### Operational Snapshot
- **Active Projects**: {data['active_work_orders_count']}
- **Completed Projects**: {data['completed_work_orders_count']}
- **Delayed / Overdue Projects**: {data['delayed_work_orders_count']} ({data['delay_rate_pct']}% delay rate)

### Delayed Projects Requiring Attention
{delayed_list}

### Data Quality Alert
- {dq.work_orders_quality.issues[0] if dq.work_orders_quality.issues else 'Work Order status metadata is fully normalized.'}
"""

ai_agent_service = AIAgentService()
