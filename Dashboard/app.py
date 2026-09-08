from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

st.set_page_config(
    page_title="AI Jobs & Salaries — Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f172a;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f1f5f9 !important;
    font-weight: 600;
}
[data-testid="stSidebar"] .stMultiSelect > div,
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stSlider {
    background: transparent;
}
[data-testid="stSidebar"] hr {
    border-color: #1e293b;
}

/* Remove default streamlit padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Page header */
.page-header {
    padding: 1.5rem 0 1rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
.page-header p {
    color: #64748b;
    margin: 0.25rem 0 0 0;
    font-size: 0.9rem;
}

/* KPI cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s;
}
.kpi-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
}
.kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
}
.kpi-delta {
    font-size: 0.78rem;
    font-weight: 500;
    color: #22c55e;
}
.kpi-delta.neg {
    color: #ef4444;
}
.kpi-accent {
    width: 3px;
    height: 100%;
    border-radius: 4px;
    position: absolute;
    left: 0;
    top: 0;
}

/* Section headers */
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.01em;
}
.section-subtitle {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0 0 1rem 0;
}

/* Insight box */
.insight-box {
    background: #f0f9ff;
    border-left: 3px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    margin-top: 0.75rem;
    font-size: 0.82rem;
    color: #0f172a;
    line-height: 1.55;
}
.insight-box strong {
    color: #1d4ed8;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 2rem 0;
}

/* Tab styling */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 2px;
    background: #f8fafc;
    border-radius: 8px;
    padding: 4px;
    border: 1px solid #e2e8f0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-weight: 500;
    font-size: 0.85rem;
    color: #475569;
    border-radius: 6px;
    padding: 0.5rem 1.25rem;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important;
    color: #0f172a !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Table styling */
.dataframe {
    font-size: 0.82rem !important;
}

/* Sidebar section header */
.sidebar-section {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569 !important;
    margin: 1.25rem 0 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Color palette ────────────────────────────────────────────────────────────
COLORS = {
    "primary":   "#2563eb",
    "secondary": "#7c3aed",
    "accent":    "#0ea5e9",
    "warning":   "#f59e0b",
    "danger":    "#ef4444",
    "success":   "#22c55e",
    "neutral":   "#64748b",
}

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font=dict(family="Inter, sans-serif", color="#0f172a", size=12),
        xaxis=dict(gridcolor="#e2e8f0", zerolinecolor="#e2e8f0", linecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#e2e8f0", zerolinecolor="#e2e8f0", linecolor="#e2e8f0"),
        legend=dict(bgcolor="white", bordercolor="#e2e8f0", borderwidth=1),
        margin=dict(t=20, b=40, l=40, r=20),
        colorway=["#2563eb", "#7c3aed", "#0ea5e9", "#f59e0b", "#ef4444",
                  "#22c55e", "#f97316", "#ec4899", "#14b8a6", "#8b5cf6"],
    )
)

QUAL_PALETTE = ["#2563eb", "#7c3aed", "#0ea5e9", "#f59e0b", "#ef4444",
                "#22c55e", "#f97316", "#ec4899", "#14b8a6", "#8b5cf6"]

def apply_template(fig):
    fig.update_layout(PLOTLY_TEMPLATE["layout"])
    fig.layout.title = None
    return fig

def fmt_k(val):
    if val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif val >= 1000:
        return f"${val/1000:.0f}K"
    return f"${val:.0f}"

# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    candidate_paths = [
        Path("Dataset/ai_jobs_salaries_clean.csv"),
        Path("../Dataset/ai_jobs_salaries_clean.csv"),
        Path(__file__).resolve().parent.parent / "Dataset" / "ai_jobs_salaries_clean.csv",
        Path(__file__).resolve().parent / "Dataset" / "ai_jobs_salaries_clean.csv",
    ]
    for p in candidate_paths:
        if p.exists():
            df = pd.read_csv(p)
            df["work_year"] = df["work_year"].astype(int)
            return df
    raise FileNotFoundError("Dataset/ai_jobs_salaries_clean.csv could not be found.")

with st.spinner("Loading data..."):
    df_raw = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## AI Jobs & Salaries")
    st.markdown("**Analytics Dashboard**  \n`2020 – 2025  |  71,913 records`")
    st.markdown("---")

    st.markdown('<p class="sidebar-section">Filters</p>', unsafe_allow_html=True)

    year_range = st.slider(
        "Year Range",
        min_value=int(df_raw["work_year"].min()),
        max_value=int(df_raw["work_year"].max()),
        value=(int(df_raw["work_year"].min()), int(df_raw["work_year"].max())),
    )

    all_exp = sorted(df_raw["experience_level_label"].unique().tolist())
    sel_exp = st.multiselect("Experience Level", all_exp, default=all_exp)

    all_modes = sorted(df_raw["work_mode"].unique().tolist())
    sel_mode = st.multiselect("Work Mode", all_modes, default=all_modes)

    all_sizes = sorted(df_raw["company_size"].unique().tolist())
    size_map = {"S": "Small", "M": "Medium", "L": "Large"}
    sel_size = st.multiselect(
        "Company Size",
        options=all_sizes,
        format_func=lambda x: size_map.get(x, x),
        default=all_sizes,
    )

    all_roles = sorted(df_raw["role_family"].unique().tolist())
    sel_roles = st.multiselect("Role Family", all_roles, default=all_roles)

    top20_countries = df_raw["company_location"].value_counts().head(20).index.tolist()
    sel_countries = st.multiselect(
        "Company Country (Top 20)",
        options=top20_countries,
        default=top20_countries,
    )

    exclude_outliers = st.checkbox("Exclude Salary Outliers", value=True)

    st.markdown("---")
    st.caption("Built with Streamlit & Plotly")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
df = df[
    df["work_year"].between(year_range[0], year_range[1]) &
    df["experience_level_label"].isin(sel_exp) &
    df["work_mode"].isin(sel_mode) &
    df["company_size"].isin(sel_size) &
    df["role_family"].isin(sel_roles) &
    df["company_location"].isin(sel_countries)
]
if exclude_outliers:
    df = df[df["salary_outlier_flag"] == False]

total_filtered = len(df)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>AI Jobs & Salaries — Analytics Dashboard</h1>
    <p>Comprehensive analysis of AI/ML industry compensation trends, 2020–2025</p>
</div>
""", unsafe_allow_html=True)

if total_filtered == 0:
    st.warning("No records match your current filter selection. Please adjust the sidebar filters.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
median_sal   = df["salary_in_usd"].median()
mean_sal     = df["salary_in_usd"].mean()
max_sal      = df["salary_in_usd"].max()
unique_titles = df["job_title"].nunique()
unique_countries = df["company_location"].nunique()
pct_remote   = (df["work_mode"] == "Remote").mean() * 100

prev_year = df[df["work_year"] == (year_range[1] - 1)]["salary_in_usd"].median() if year_range[1] > year_range[0] else None
curr_year = df[df["work_year"] == year_range[1]]["salary_in_usd"].median()
yoy_growth = ((curr_year - prev_year) / prev_year * 100) if prev_year and prev_year > 0 else None

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Records</div>
    <div class="kpi-value">{total_filtered:,}</div>
    <div class="kpi-delta">after filters applied</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Median Salary</div>
    <div class="kpi-value">{fmt_k(median_sal)}</div>
    <div class="kpi-delta">{"YoY +{:.1f}%".format(yoy_growth) if yoy_growth and yoy_growth >= 0 else ("YoY {:.1f}%".format(yoy_growth) if yoy_growth else "")}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Average Salary</div>
    <div class="kpi-value">{fmt_k(mean_sal)}</div>
    <div class="kpi-delta">mean across all records</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Unique Roles</div>
    <div class="kpi-value">{unique_titles:,}</div>
    <div class="kpi-delta">across {unique_countries} countries</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Remote Share</div>
    <div class="kpi-value">{pct_remote:.1f}%</div>
    <div class="kpi-delta">fully remote positions</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Market Overview",
    "Salary Analysis",
    "Geographic",
    "Trends Over Time",
    "Role Deep Dive",
])

exp_order = ["Entry-level", "Mid-level", "Senior-level", "Executive-level"]
exp_colors = {
    "Entry-level":     QUAL_PALETTE[2],
    "Mid-level":       QUAL_PALETTE[0],
    "Senior-level":    QUAL_PALETTE[1],
    "Executive-level": QUAL_PALETTE[4],
}

# ═══════════════════════════════════════════════════════════════════════
# TAB 1 — Market Overview
# ═══════════════════════════════════════════════════════════════════════
with tabs[0]:
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<p class="section-title">Salary Distribution</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Distribution of salaries (USD) across all filtered records</p>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df["salary_in_usd"],
            nbinsx=80,
            marker_color=COLORS["primary"],
            opacity=0.85,
            name="Salary (USD)",
        ))
        fig.add_vline(x=median_sal, line_dash="dash", line_color=COLORS["warning"],
                      annotation_text=f"Median: {fmt_k(median_sal)}", annotation_position="top right",
                      annotation_font_color=COLORS["warning"])
        fig.add_vline(x=mean_sal, line_dash="dot", line_color=COLORS["danger"],
                      annotation_text=f"Mean: {fmt_k(mean_sal)}", annotation_position="top left",
                      annotation_font_color=COLORS["danger"])
        fig.update_layout(
            height=340,
            xaxis_title="Annual Salary (USD)",
            yaxis_title="Number of Records",
            showlegend=False,
            xaxis_tickformat="$,.0f",
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> The salary distribution is right-skewed — the majority of AI professionals earn
        between $80K–$160K USD, while a long tail extends toward $300K+ for specialized and executive roles.
        The gap between the mean and median (~10–15%) confirms the pull from high-paying outlier positions.
        </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<p class="section-title">Records per Year</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Volume of job records in the dataset by year</p>', unsafe_allow_html=True)

        year_counts = df["work_year"].value_counts().sort_index().reset_index()
        year_counts.columns = ["Year", "Count"]

        fig2 = go.Figure()
        bar_colors = [COLORS["primary"] if y < year_range[1] else COLORS["accent"]
                      for y in year_counts["Year"]]
        fig2.add_trace(go.Bar(
            x=year_counts["Year"].astype(str),
            y=year_counts["Count"],
            marker_color=bar_colors,
            text=year_counts["Count"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig2.update_layout(
            height=340,
            xaxis_title="Year",
            yaxis_title="Records",
            showlegend=False,
            yaxis_showgrid=True,
        )
        apply_template(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> AI job postings grew dramatically from 2020 to 2025,
        with the steepest acceleration from 2022 onward — coinciding with the mainstream
        adoption of large language models and generative AI in enterprise settings.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4, gap="large")

    with col_a:
        st.markdown('<p class="section-title">Experience Level</p>', unsafe_allow_html=True)
        vc = df["experience_level_label"].value_counts()
        fig = go.Figure(go.Pie(
            labels=vc.index, values=vc.values,
            hole=0.55,
            marker_colors=[exp_colors.get(l, "#888") for l in vc.index],
            textinfo="label+percent",
            textfont_size=11,
        ))
        apply_template(fig)
        fig.update_layout(height=270, showlegend=False, margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">Work Mode</p>', unsafe_allow_html=True)
        vc2 = df["work_mode"].value_counts()
        mode_colors = {"Remote": COLORS["success"], "Hybrid": COLORS["primary"], "On-site": COLORS["secondary"]}
        fig = go.Figure(go.Pie(
            labels=vc2.index, values=vc2.values,
            hole=0.55,
            marker_colors=[mode_colors.get(l, "#888") for l in vc2.index],
            textinfo="label+percent",
            textfont_size=11,
        ))
        apply_template(fig)
        fig.update_layout(height=270, showlegend=False, margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_c:
        st.markdown('<p class="section-title">Employment Type</p>', unsafe_allow_html=True)
        vc3 = df["employment_type_label"].value_counts()
        fig = go.Figure(go.Pie(
            labels=vc3.index, values=vc3.values,
            hole=0.55,
            marker_colors=QUAL_PALETTE[:len(vc3)],
            textinfo="label+percent",
            textfont_size=11,
        ))
        apply_template(fig)
        fig.update_layout(height=270, showlegend=False, margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.markdown('<p class="section-title">Company Size</p>', unsafe_allow_html=True)
        vc4 = df["company_size"].value_counts()
        size_label_map = {"S": "Small", "M": "Medium", "L": "Large"}
        vc4.index = [size_label_map.get(i, i) for i in vc4.index]
        fig = go.Figure(go.Pie(
            labels=vc4.index, values=vc4.values,
            hole=0.55,
            marker_colors=[COLORS["accent"], COLORS["primary"], COLORS["secondary"]],
            textinfo="label+percent",
            textfont_size=11,
        ))
        apply_template(fig)
        fig.update_layout(height=270, showlegend=False, margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 2 — Salary Analysis
# ═══════════════════════════════════════════════════════════════════════
with tabs[1]:
    # Row 1: By Experience + By Work Mode
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="section-title">Salary by Experience Level</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Distribution of annual salary (USD) across experience tiers</p>', unsafe_allow_html=True)

        df_exp = df[df["experience_level_label"].isin(exp_order)]
        fig = go.Figure()
        for level in exp_order:
            sub = df_exp[df_exp["experience_level_label"] == level]["salary_in_usd"]
            if len(sub) == 0:
                continue
            fig.add_trace(go.Box(
                y=sub,
                name=level,
                marker_color=exp_colors.get(level, "#888"),
                boxmean="sd",
                showlegend=False,
                line_width=1.5,
            ))
        fig.update_layout(
            height=380,
            yaxis_title="Annual Salary (USD)",
            yaxis_tickformat="$,.0f",
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        exp_stats = df.groupby("experience_level_label")["salary_in_usd"].agg(["median", "mean", "count"])
        exp_stats = exp_stats.reindex([e for e in exp_order if e in exp_stats.index])
        exp_stats.columns = ["Median ($)", "Mean ($)", "Count"]
        exp_stats["Median ($)"] = exp_stats["Median ($)"].apply(lambda x: f"${x:,.0f}")
        exp_stats["Mean ($)"]   = exp_stats["Mean ($)"].apply(lambda x: f"${x:,.0f}")
        exp_stats["Count"]      = exp_stats["Count"].apply(lambda x: f"{x:,}")
        st.dataframe(exp_stats, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Experience level is the single strongest predictor of salary.
        Executive-level professionals earn 2–3x the median salary of entry-level peers.
        Senior-level roles show the widest interquartile range — reflecting high variability
        in specialization and domain demand.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-title">Salary by Work Mode</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">How remote, hybrid, and on-site arrangements affect compensation</p>', unsafe_allow_html=True)

        mode_order = ["On-site", "Hybrid", "Remote"]
        mode_colors_list = [mode_colors.get(m, "#888") for m in mode_order if m in df["work_mode"].unique()]
        df_mode = df[df["work_mode"].isin(mode_order)]

        fig = go.Figure()
        for m in mode_order:
            sub = df_mode[df_mode["work_mode"] == m]["salary_in_usd"]
            if len(sub) == 0:
                continue
            fig.add_trace(go.Violin(
                y=sub,
                name=m,
                box_visible=True,
                meanline_visible=True,
                fillcolor=mode_colors.get(m, "#888"),
                opacity=0.7,
                line_color=mode_colors.get(m, "#888"),
                showlegend=False,
            ))
        fig.update_layout(
            height=380,
            yaxis_title="Annual Salary (USD)",
            yaxis_tickformat="$,.0f",
            violingap=0.2,
            violinmode="overlay",
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        mode_stats = df[df["work_mode"].isin(mode_order)].groupby("work_mode")["salary_in_usd"].agg(["median", "count"])
        mode_stats = mode_stats.reindex([m for m in mode_order if m in mode_stats.index])
        mode_stats.columns = ["Median Salary ($)", "Records"]
        mode_stats["Median Salary ($)"] = mode_stats["Median Salary ($)"].apply(lambda x: f"${x:,.0f}")
        mode_stats["Records"] = mode_stats["Records"].apply(lambda x: f"{x:,}")
        st.dataframe(mode_stats, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Remote and on-site roles offer comparable median compensation —
        contradicting the assumption that remote work always trades lower pay for flexibility.
        Hybrid positions tend to have a slightly wider salary spread, often indicating mid-career
        professionals negotiating flexible arrangements with established employers.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Row 2: By Role Family + Top Job Titles
    col3, col4 = st.columns([3, 2], gap="large")

    with col3:
        st.markdown('<p class="section-title">Median Salary by Role Family</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Ranked by median annual salary (USD), with IQR as error bars</p>', unsafe_allow_html=True)

        role_stats = (
            df.groupby("role_family")["salary_in_usd"]
            .agg(
                median="median",
                q25=lambda x: x.quantile(0.25),
                q75=lambda x: x.quantile(0.75),
                count="count",
            )
            .sort_values("median", ascending=True)
            .reset_index()
        )

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=role_stats["median"],
            y=role_stats["role_family"],
            orientation="h",
            marker_color=COLORS["primary"],
            error_x=dict(
                type="data",
                symmetric=False,
                array=(role_stats["q75"] - role_stats["median"]).tolist(),
                arrayminus=(role_stats["median"] - role_stats["q25"]).tolist(),
                color=COLORS["warning"],
                thickness=2,
                width=5,
            ),
            text=[f"{fmt_k(v)}  (n={int(c):,})" for v, c in zip(role_stats["median"], role_stats["count"])],
            textposition="outside",
            textfont=dict(size=10, color="#64748b"),
        ))
        fig.update_layout(
            height=420,
            xaxis_title="Median Salary (USD)",
            xaxis_tickformat="$,.0f",
            yaxis_title=None,
            showlegend=False,
            xaxis_range=[0, role_stats["q75"].max() * 1.4],
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> AI Architect and Research Scientist roles command premium salaries
        ($160K+ median), reflecting their strategic and research-intensive nature.
        Traditional roles like Data Analyst remain valuable but fall below the AI-native average,
        with a ~$30–50K gap vs. AI-specific engineering positions.
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown('<p class="section-title">Top 15 Highest-Paying Titles</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Minimum 10 records required for inclusion</p>', unsafe_allow_html=True)

        top_titles = (
            df.groupby("job_title")["salary_in_usd"]
            .agg(median="median", count="count")
            .query("count >= 10")
            .sort_values("median", ascending=False)
            .head(15)
            .reset_index()
        )

        fig = go.Figure(go.Bar(
            y=top_titles["job_title"][::-1],
            x=top_titles["median"][::-1],
            orientation="h",
            marker_color=px.colors.sequential.Blues_r[:len(top_titles)],
            text=[fmt_k(v) for v in top_titles["median"][::-1]],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(
            height=420,
            xaxis_title="Median Salary (USD)",
            xaxis_tickformat="$,.0f",
            yaxis_title=None,
            showlegend=False,
            xaxis_range=[0, top_titles["median"].max() * 1.3],
            yaxis_tickfont=dict(size=10),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Row 3: Salary by Company Size + Heatmap Role x Experience
    col5, col6 = st.columns(2, gap="large")

    with col5:
        st.markdown('<p class="section-title">Salary by Company Size</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Small vs Medium vs Large company compensation comparison</p>', unsafe_allow_html=True)

        df_sz = df.copy()
        df_sz["Size Label"] = df_sz["company_size"].map({"S": "Small", "M": "Medium", "L": "Large"})
        sz_order = ["Small", "Medium", "Large"]
        sz_colors = {"Small": COLORS["accent"], "Medium": COLORS["primary"], "Large": COLORS["secondary"]}

        fig = go.Figure()
        for s in sz_order:
            sub = df_sz[df_sz["Size Label"] == s]["salary_in_usd"]
            if len(sub) == 0:
                continue
            fig.add_trace(go.Box(
                y=sub, name=s,
                marker_color=sz_colors[s],
                boxmean="sd",
                showlegend=False,
                line_width=1.5,
            ))
        fig.update_layout(
            height=350,
            yaxis_title="Annual Salary (USD)",
            yaxis_tickformat="$,.0f",
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Large companies offer the highest ceiling salaries, but medium-sized
        companies are highly competitive — often within $5–10K of large company medians —
        while typically offering faster career progression and broader responsibilities.
        </div>""", unsafe_allow_html=True)

    with col6:
        st.markdown('<p class="section-title">Salary Heatmap — Role x Experience</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Median salary (K USD) by role family and experience level</p>', unsafe_allow_html=True)

        _avail_exp = [e for e in exp_order if e in df["experience_level_label"].unique()]
        pivot = (
            df.pivot_table(
                index="role_family",
                columns="experience_level_label",
                values="salary_in_usd",
                aggfunc="median",
            )
            .reindex(columns=_avail_exp)
        )
        _sort_col = "Senior-level" if "Senior-level" in pivot.columns else (pivot.columns[-1] if len(pivot.columns) > 0 else None)
        if _sort_col:
            pivot = pivot.sort_values(_sort_col, ascending=False, na_position="last")
        pivot = pivot / 1000

        _text = [
            [f"{val:.0f}K" if pd.notna(val) else "" for val in row]
            for row in pivot.values
        ]
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale="Blues",
            text=_text,
            texttemplate="%{text}",
            textfont=dict(size=11),
            showscale=True,
            colorbar=dict(title="Salary (K USD)", thickness=12),
        ))
        fig.update_layout(
            height=350,
            xaxis_title=None,
            yaxis_title=None,
            yaxis_tickfont=dict(size=10),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> The heatmap reveals that the salary premium from moving
        from Mid-level to Senior-level is consistently large (~$30–50K) across all role families.
        AI Architect and Research Scientist show the steepest experience gradient,
        suggesting these roles reward depth of expertise most heavily.
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 3 — Geographic Analysis
# ═══════════════════════════════════════════════════════════════════════
with tabs[2]:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p class="section-title">Job Volume by Country</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Number of records per company location (Top 15)</p>', unsafe_allow_html=True)

        country_counts = df["company_location"].value_counts().head(15).reset_index()
        country_counts.columns = ["Country", "Records"]

        fig = go.Figure(go.Bar(
            x=country_counts["Records"][::-1],
            y=country_counts["Country"][::-1],
            orientation="h",
            marker=dict(
                color=country_counts["Records"][::-1],
                colorscale="Blues",
                showscale=False,
            ),
            text=country_counts["Records"][::-1].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig.update_layout(
            height=430,
            xaxis_title="Number of Records",
            yaxis_title=None,
            showlegend=False,
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> The United States dominates AI hiring by a large margin —
        accounting for the majority of records in this dataset. However, Canada, the UK,
        and Germany represent the next wave of significant AI talent markets,
        reflecting increased enterprise AI investment in those regions.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-title">Median Salary by Country</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Countries with at least 30 records in the filtered dataset</p>', unsafe_allow_html=True)

        geo_sal = (
            df.groupby("company_location")
            .agg(median=("salary_in_usd", "median"), count=("salary_in_usd", "count"))
            .query("count >= 30")
            .sort_values("median", ascending=True)
            .tail(15)
            .reset_index()
        )

        fig = go.Figure(go.Bar(
            x=geo_sal["median"],
            y=geo_sal["company_location"],
            orientation="h",
            marker=dict(
                color=geo_sal["median"],
                colorscale="RdYlGn",
                showscale=True,
                colorbar=dict(title="Median $", thickness=12),
            ),
            text=[fmt_k(v) for v in geo_sal["median"]],
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig.update_layout(
            height=430,
            xaxis_title="Median Salary (USD)",
            xaxis_tickformat="$,.0f",
            yaxis_title=None,
            showlegend=False,
            xaxis_range=[0, geo_sal["median"].max() * 1.3],
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> The US offers the highest absolute salaries, but when adjusted
        for purchasing power, European markets (Netherlands, Germany, Switzerland) offer
        highly competitive compensation. Emerging markets like India show lower USD salaries
        but are rapidly growing in AI talent production.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown('<p class="section-title">Remote Work Adoption by Country</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Average remote ratio per company country (Top 15 by volume)</p>', unsafe_allow_html=True)

        top15_c = df["company_location"].value_counts().head(15).index
        remote_c = (
            df[df["company_location"].isin(top15_c)]
            .groupby("company_location")["remote_ratio"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        remote_c.columns = ["Country", "Avg Remote Ratio"]

        bar_colors_r = [
            COLORS["success"] if v >= 60 else (COLORS["primary"] if v >= 30 else COLORS["danger"])
            for v in remote_c["Avg Remote Ratio"]
        ]
        avg_line = remote_c["Avg Remote Ratio"].mean()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=remote_c["Country"],
            y=remote_c["Avg Remote Ratio"],
            marker_color=bar_colors_r,
            text=remote_c["Avg Remote Ratio"].apply(lambda x: f"{x:.0f}"),
            textposition="outside",
            textfont=dict(size=10),
            showlegend=False,
        ))
        fig.add_hline(y=avg_line, line_dash="dash", line_color=COLORS["warning"],
                      annotation_text=f"Avg: {avg_line:.0f}", annotation_position="top right")
        fig.update_layout(
            height=370,
            xaxis_title="Country",
            yaxis_title="Avg Remote Ratio (0–100)",
            yaxis_range=[0, 110],
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<p class="section-title">Country Profile Summary</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Key metrics for the top hiring countries</p>', unsafe_allow_html=True)

        country_profile = (
            df[df["company_location"].isin(top15_c)]
            .groupby("company_location")
            .agg(
                Records=("salary_in_usd", "count"),
                Median_Salary=("salary_in_usd", "median"),
                Avg_Remote=("remote_ratio", "mean"),
                Pct_Senior=("experience_level", lambda x: (x == "SE").mean() * 100),
            )
            .sort_values("Records", ascending=False)
            .reset_index()
        )
        country_profile.columns = ["Country", "Records", "Median Salary", "Remote Ratio", "% Senior-level"]
        country_profile["Median Salary"] = country_profile["Median Salary"].apply(lambda x: f"${x:,.0f}")
        country_profile["Remote Ratio"]  = country_profile["Remote Ratio"].apply(lambda x: f"{x:.0f}")
        country_profile["% Senior-level"] = country_profile["% Senior-level"].apply(lambda x: f"{x:.0f}%")
        country_profile["Records"]       = country_profile["Records"].apply(lambda x: f"{x:,}")

        st.dataframe(country_profile, use_container_width=True, height=370)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Countries like Lithuania and Latvia appear in the Top 15
        due to the emergence of European AI hubs and outsourcing destinations.
        The US leads in both volume and salary, but shows below-average remote ratios
        compared to European counterparts — suggesting more in-office culture in US AI companies.
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 4 — Trends Over Time
# ═══════════════════════════════════════════════════════════════════════
with tabs[3]:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<p class="section-title">Salary Trend Over Time</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Median and mean salary evolution from 2020 to 2025</p>', unsafe_allow_html=True)

        salary_trend = (
            df.groupby("work_year")["salary_in_usd"]
            .agg(median="median", mean="mean", q25=lambda x: x.quantile(0.25),
                 q75=lambda x: x.quantile(0.75), count="count")
            .reset_index()
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=salary_trend["work_year"], y=salary_trend["q75"],
            fill=None, mode="lines", line_color="rgba(37,99,235,0.0)", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=salary_trend["work_year"], y=salary_trend["q25"],
            fill="tonexty", mode="lines", line_color="rgba(37,99,235,0.0)",
            fillcolor="rgba(37,99,235,0.1)", name="IQR Band", showlegend=True,
        ))
        fig.add_trace(go.Scatter(
            x=salary_trend["work_year"], y=salary_trend["median"],
            mode="lines+markers+text",
            line=dict(color=COLORS["primary"], width=3),
            marker=dict(size=8, color=COLORS["primary"]),
            name="Median Salary",
            text=[fmt_k(v) for v in salary_trend["median"]],
            textposition="top center",
            textfont=dict(size=10, color=COLORS["primary"]),
        ))
        fig.add_trace(go.Scatter(
            x=salary_trend["work_year"], y=salary_trend["mean"],
            mode="lines+markers",
            line=dict(color=COLORS["warning"], width=2, dash="dash"),
            marker=dict(size=6, color=COLORS["warning"]),
            name="Mean Salary",
        ))
        fig.update_layout(
            height=380,
            xaxis_title="Year",
            yaxis_title="Salary (USD)",
            yaxis_tickformat="$,.0f",
            legend=dict(orientation="h", y=-0.15),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Median AI salaries increased substantially from 2020 to 2025,
        with the sharpest growth occurring from 2022 to 2023 — aligning with the generative AI boom
        and intense competition for AI engineering talent. The widening IQR band indicates increasing
        salary inequality within the AI workforce over time.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-title">Year-over-Year Salary Growth</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Percentage change in median salary per year</p>', unsafe_allow_html=True)

        yoy = salary_trend[["work_year", "median"]].copy()
        yoy["yoy_pct"] = yoy["median"].pct_change() * 100

        yoy_plot = yoy.dropna(subset=["yoy_pct"])
        bar_colors_yoy = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in yoy_plot["yoy_pct"]]

        fig = go.Figure(go.Bar(
            x=yoy_plot["work_year"].astype(str),
            y=yoy_plot["yoy_pct"],
            marker_color=bar_colors_yoy,
            text=yoy_plot["yoy_pct"].apply(lambda x: f"+{x:.1f}%" if x >= 0 else f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(size=12, color="#0f172a"),
        ))
        fig.add_hline(y=0, line_color="#94a3b8", line_width=1)
        fig.update_layout(
            height=380,
            xaxis_title="Year",
            yaxis_title="YoY Growth (%)",
            showlegend=False,
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            yoy_plot[["work_year", "median", "yoy_pct"]].rename(columns={
                "work_year": "Year", "median": "Median Salary", "yoy_pct": "YoY Growth (%)"
            }).assign(
                **{
                    "Median Salary": lambda d: d["Median Salary"].apply(lambda x: f"${x:,.0f}"),
                    "YoY Growth (%)": lambda d: d["YoY Growth (%)"].apply(lambda x: f"+{x:.1f}%" if x >= 0 else f"{x:.1f}%"),
                }
            ).set_index("Year"),
            use_container_width=True,
        )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown('<p class="section-title">Salary Trend by Experience Level</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Has the experience-salary gap been widening or narrowing?</p>', unsafe_allow_html=True)

        exp_time = (
            df.groupby(["work_year", "experience_level_label"])["salary_in_usd"]
            .median()
            .reset_index()
        )

        fig = go.Figure()
        for level in exp_order:
            sub = exp_time[exp_time["experience_level_label"] == level]
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub["work_year"], y=sub["salary_in_usd"],
                mode="lines+markers",
                line=dict(color=exp_colors.get(level, "#888"), width=2.5),
                marker=dict(size=7),
                name=level,
                fill="tonexty" if level == "Entry-level" else None,
                fillcolor="rgba(14,165,233,0.05)",
            ))
        fig.update_layout(
            height=360,
            xaxis_title="Year",
            yaxis_title="Median Salary (USD)",
            yaxis_tickformat="$,.0f",
            legend=dict(orientation="h", y=-0.18),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> The salary gap between experience levels has been widening
        over time, particularly since 2022. This suggests that AI expertise at senior and
        executive levels is becoming increasingly scarce relative to demand —
        a classic supply-side constraint driving compensation inflation at the top.
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown('<p class="section-title">Remote Work Trend Over Time</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Proportion of remote vs hybrid vs on-site by year</p>', unsafe_allow_html=True)

        mode_year = (
            df.groupby(["work_year", "work_mode"])
            .size()
            .reset_index(name="count")
        )
        mode_year_pct = mode_year.copy()
        totals = mode_year_pct.groupby("work_year")["count"].transform("sum")
        mode_year_pct["pct"] = mode_year_pct["count"] / totals * 100

        fig = go.Figure()
        for mode in ["On-site", "Hybrid", "Remote"]:
            sub = mode_year_pct[mode_year_pct["work_mode"] == mode]
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub["work_year"], y=sub["pct"],
                stackgroup="one",
                mode="lines",
                name=mode,
                fillcolor=dict(Remote=COLORS["success"], Hybrid=COLORS["primary"], **{"On-site": COLORS["secondary"]}).get(mode, "#888"),
                line=dict(width=0),
            ))
        fig.update_layout(
            height=360,
            xaxis_title="Year",
            yaxis_title="Share (%)",
            yaxis_range=[0, 100],
            legend=dict(orientation="h", y=-0.18),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Remote work saw its peak adoption during 2021–2022, driven by
        pandemic-era norms. Since 2023, there has been a visible shift back toward on-site and
        hybrid arrangements as large tech companies issued return-to-office mandates —
        a trend that is reshaping salary geography and talent mobility.
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# TAB 5 — Role Deep Dive
# ═══════════════════════════════════════════════════════════════════════
with tabs[4]:
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.markdown('<p class="section-title">Role Family Volume</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Total records per role family in the filtered dataset</p>', unsafe_allow_html=True)

        role_vol = df["role_family"].value_counts().reset_index()
        role_vol.columns = ["Role Family", "Count"]

        fig = go.Figure(go.Bar(
            x=role_vol["Count"][::-1],
            y=role_vol["Role Family"][::-1],
            orientation="h",
            marker=dict(
                color=role_vol["Count"][::-1],
                colorscale="Blues",
                showscale=False,
            ),
            text=role_vol["Count"][::-1].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(
            height=420,
            xaxis_title="Number of Records",
            yaxis_title=None,
            showlegend=False,
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Role Family Market Share Over Time</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">How the composition of AI jobs has shifted year by year</p>', unsafe_allow_html=True)

        top_roles_list = df["role_family"].value_counts().head(8).index.tolist()
        role_share = (
            df[df["role_family"].isin(top_roles_list)]
            .groupby(["work_year", "role_family"])
            .size()
            .unstack(fill_value=0)
        )
        role_share_pct = role_share.div(role_share.sum(axis=1), axis=0) * 100

        fig = go.Figure()
        for i, role in enumerate(role_share_pct.columns):
            fig.add_trace(go.Scatter(
                x=role_share_pct.index.tolist(),
                y=role_share_pct[role].tolist(),
                stackgroup="one",
                name=role,
                mode="lines",
                fillcolor=QUAL_PALETTE[i % len(QUAL_PALETTE)],
                line=dict(width=0),
            ))
        fig.update_layout(
            height=420,
            xaxis_title="Year",
            yaxis_title="Share (%)",
            yaxis_range=[0, 100],
            legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown('<p class="section-title">Salary Growth Rate by Role Family</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">CAGR of median salary from first to last available year per role</p>', unsafe_allow_html=True)

        role_cagr_data = []
        for role in df["role_family"].unique():
            sub = df[df["role_family"] == role].groupby("work_year")["salary_in_usd"].median()
            if len(sub) >= 2:
                years = sub.index.tolist()
                n = years[-1] - years[0]
                if n > 0 and sub.iloc[0] > 0:
                    cagr = ((sub.iloc[-1] / sub.iloc[0]) ** (1 / n) - 1) * 100
                    role_cagr_data.append({"Role Family": role, "CAGR (%)": cagr,
                                            "Start Salary": sub.iloc[0], "End Salary": sub.iloc[-1]})
        cagr_df = pd.DataFrame(role_cagr_data).sort_values("CAGR (%)", ascending=True)

        bar_colors_cagr = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in cagr_df["CAGR (%)"]]
        fig = go.Figure(go.Bar(
            x=cagr_df["CAGR (%)"],
            y=cagr_df["Role Family"],
            orientation="h",
            marker_color=bar_colors_cagr,
            text=cagr_df["CAGR (%)"].apply(lambda x: f"+{x:.1f}%" if x >= 0 else f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.add_vline(x=0, line_color="#94a3b8", line_width=1)
        fig.update_layout(
            height=380,
            xaxis_title="CAGR (%)",
            yaxis_title=None,
            showlegend=False,
        )
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> AI-specific role families (AI Engineer, AI Architect, NLP)
        show the highest salary CAGR, with some exceeding 10% annually. This outpaces traditional
        tech salary growth (~3–5% annually) by a significant margin, confirming that AI specialization
        commands an accelerating wage premium.
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown('<p class="section-title">Role Family Statistics Table</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Comprehensive breakdown of salary metrics per role family</p>', unsafe_allow_html=True)

        role_full = (
            df.groupby("role_family")["salary_in_usd"]
            .agg(
                Count="count",
                Min="min",
                P25=lambda x: x.quantile(0.25),
                Median="median",
                P75=lambda x: x.quantile(0.75),
                Max="max",
            )
            .sort_values("Median", ascending=False)
            .reset_index()
        )
        for col_name in ["Min", "P25", "Median", "P75", "Max"]:
            role_full[col_name] = role_full[col_name].apply(lambda x: f"${x:,.0f}")
        role_full["Count"] = role_full["Count"].apply(lambda x: f"{x:,}")
        role_full.columns = ["Role Family", "Records", "Min", "P25", "Median", "P75", "Max"]
        st.dataframe(role_full.set_index("Role Family"), use_container_width=True, height=380)

        st.markdown("""
        <div class="insight-box">
        <strong>Key Insight:</strong> Role families like "Other / Unclassified" have a high record count
        but wide salary dispersion — indicating heterogeneous job titles that haven't been standardized.
        Research Scientist and AI Architect show the highest median-to-P75 compression,
        suggesting most earners cluster near the top of their range.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Statistical test section
    st.markdown('<p class="section-title">Statistical Validation — ANOVA by Experience Level</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">One-way ANOVA to test whether salary differences across experience levels are statistically significant</p>', unsafe_allow_html=True)

    groups = [
        df[df["experience_level_label"] == lvl]["salary_in_usd"].dropna().values
        for lvl in exp_order if lvl in df["experience_level_label"].unique()
    ]
    if len(groups) >= 2:
        f_stat, p_value = stats.f_oneway(*groups)
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("F-statistic", f"{f_stat:,.2f}")
        with col_stat2:
            st.metric("p-value", f"{p_value:.2e}")
        with col_stat3:
            sig = "Statistically Significant" if p_value < 0.05 else "Not Significant"
            st.metric("Result", sig)

        if p_value < 0.05:
            st.markdown("""
            <div class="insight-box">
            <strong>Result:</strong> The ANOVA confirms statistically significant salary differences across experience levels
            (p &lt; 0.05). This means the observed salary gaps between Entry, Mid, Senior, and Executive levels
            are not due to random chance — they reflect real, structural differences in compensation driven by
            seniority, responsibility, and market demand.
            </div>""", unsafe_allow_html=True)
