"""
Smart Inventory & Expiry Manager - Main Streamlit Application
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom

A modern, SaaS-grade Inventory & Expiry Management dashboard designed for small businesses
and educational algorithm demonstration.
"""

import time
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import algorithms
import inventory
import storage

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & REFINED SAAS DESIGN SYSTEM
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Smart Inventory & Expiry Manager | Team Axiom",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Design System (Dark Navy & Teal/Cyan identity with subtle accents)
st.markdown("""
<style>
    /* Google Font import for modern SaaS typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global App Background and Typography */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #0F172A;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Top Header & Header decorations */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar Theme: Deep Navy (#090E17) with refined subtle borders */
    section[data-testid="stSidebar"] {
        background-color: #090E17 !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #F1F5F9 !important;
    }
    
    /* Navigation Radio Items inside Sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        background: transparent;
        gap: 6px;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 8px 14px;
        border-radius: 8px;
        transition: all 0.15s ease-in-out;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: rgba(6, 182, 212, 0.12);
        border-color: rgba(6, 182, 212, 0.35);
        color: #38BDF8 !important;
    }

    /* Modern SaaS Page Header Banner */
    .page-header-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .page-header-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .page-header-desc {
        font-size: 0.88rem;
        color: #64748B;
        margin: 4px 0 0 0;
    }
    .page-header-badge {
        background: #F0FDFA;
        border: 1px solid #99F6E4;
        color: #0D9488;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Premium Metric Card */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(15, 23, 42, 0.08);
    }
    .kpi-accent-bar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .kpi-subtitle {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Urgent Operations Command Center */
    .urgent-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        margin-bottom: 24px;
    }
    .urgent-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 14px;
    }
    .urgent-item {
        background: #F8FAFC;
        border-radius: 8px;
        padding: 12px 16px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .urgent-item:last-child {
        margin-bottom: 0;
    }

    /* Refined Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .pill-expired {
        background-color: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
    }
    .pill-today {
        background-color: #FFFBEB;
        color: #D97706;
        border: 1px solid #FDE68A;
    }
    .pill-soon {
        background-color: #FFF7ED;
        color: #EA580C;
        border: 1px solid #FFEDD5;
    }
    .pill-safe {
        background-color: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
    }
    .pill-none {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }
    .pill-lowstock {
        background-color: #ECFEFF;
        color: #0891B2;
        border: 1px solid #CFFAFE;
    }

    .pill-critical {
        background-color: #DC2626;
        color: #FFFFFF;
    }
    .pill-high {
        background-color: #EA580C;
        color: #FFFFFF;
    }
    .pill-medium {
        background-color: #D97706;
        color: #FFFFFF;
    }
    .pill-low {
        background-color: #059669;
        color: #FFFFFF;
    }

    /* Algorithm Card & Code Block Styling */
    .algo-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        margin-bottom: 16px;
    }
    .algo-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .algo-pill {
        background: #0891B2;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Streamlit Component Tweaks */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.15s ease;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. PERSISTENCE LAYER & HASH TABLE GENERATION
# -----------------------------------------------------------------------------

storage.init_db()

# Auto-seed database if empty on initial launch
if len(storage.get_all_products()) == 0:
    inventory.seed_or_reset_demo_data()


def build_hash_table(products: List[Dict[str, Any]]) -> algorithms.ChainedHashTable:
    """Instantiates and populates the custom ChainedHashTable indexed by SKU."""
    ht = algorithms.ChainedHashTable(initial_capacity=max(16, len(products) * 2))
    for p in products:
        ht.put(p["id"], p)
    return ht


# -----------------------------------------------------------------------------
# 3. SIDEBAR: BRANDING & CONTROLS
# -----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; background: rgba(6, 182, 212, 0.15); border-radius: 10px; border: 1px solid rgba(6, 182, 212, 0.35); font-size: 1.6rem; margin-bottom: 8px;">
            📦
        </div>
        <h2 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">Axiom Inventory</h2>
        <p style="margin: 2px 0 0 0; font-size: 0.78rem; color: #06B6D4; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Smart Expiry Manager</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 10px 12px; border-radius: 8px; margin-bottom: 14px; font-size: 0.78rem; line-height: 1.45;">
        <div style="color: #94A3B8;">🎓 <strong>Course:</strong> Intro to Algorithms</div>
        <div style="color: #94A3B8;">👩‍🏫 <strong>Instructor:</strong> Dr. Fatma Talaat</div>
        <div style="color: #06B6D4;">⚡ <strong>Team:</strong> Axiom</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 4px; letter-spacing: 0.06em;'>Platform Navigation</p>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📦 Product Catalog",
            "⏰ Expiration Alerts",
            "⚠️ Low-Stock & Reorder",
            "🎯 Priority Action Matrix",
            "🔬 Algorithm Lab",
            "📑 Inventory Reports",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("<p style='font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 4px; letter-spacing: 0.06em;'>Urgency Configuration</p>", unsafe_allow_html=True)
    warning_days = st.slider("Expiration Warning (Days)", min_value=1, max_value=30, value=7, help="Products expiring within this timeframe trigger amber alerts.")
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 4px; letter-spacing: 0.06em;'>Storage Management</p>", unsafe_allow_html=True)
    if st.button("🔄 Restore Demo Data", use_container_width=True, help="Resets SQLite database to 20 realistic products with dates relative to today."):
        count = inventory.seed_or_reset_demo_data()
        st.success(f"Restored {count} demo products relative to today!")
        st.rerun()

    st.markdown("""
    <div style="margin-top: 24px; padding: 10px; background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.15); border-radius: 8px; text-align: center;">
        <span style="display: inline-block; width: 6px; height: 6px; background-color: #10B981; border-radius: 50%; margin-right: 4px;"></span>
        <span style="font-size: 0.72rem; color: #E2E8F0; font-weight: 500;">SQLite Connected | O(1) Ready</span>
    </div>
    """, unsafe_allow_html=True)


# Load fresh inventory data & build custom Hash Table
all_products = inventory.get_enriched_inventory(warning_days=warning_days)
product_hash_table = build_hash_table(all_products)

# Helper function for rendering consistent page headers
def render_page_header(title: str, description: str, icon: str, badge_text: Optional[str] = None):
    badge_html = f'<div class="page-header-badge"><span>●</span> {badge_text}</div>' if badge_text else ""
    st.markdown(f"""
    <div class="page-header-container">
        <div>
            <h1 class="page-header-title"><span>{icon}</span> {title}</h1>
            <p class="page-header-desc">{description}</p>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. VIEW: EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------

if page == "📊 Dashboard":
    render_page_header(
        title="Executive Inventory Dashboard",
        description="Comprehensive real-time overview of inventory valuation, perishability risks, and stock health.",
        icon="📊",
        badge_text=f"Live Date: {date.today().strftime('%b %d, %Y')}"
    )

    # Compute KPI metrics
    total_skus = len(all_products)
    total_units = sum(p["quantity"] for p in all_products)
    total_valuation = sum(p["total_stock_value"] for p in all_products)
    expired_products = [p for p in all_products if p["expiry_status_key"] == "EXPIRED"]
    expiring_today_products = [p for p in all_products if p["expiry_status_key"] == "EXPIRING_TODAY"]
    expiring_soon_products = [p for p in all_products if p["expiry_status_key"] == "EXPIRING_SOON"]
    low_stock_products = [p for p in all_products if p["reorder"]["needs_reorder"]]
    out_of_stock_products = [p for p in all_products if p["quantity"] <= 0]

    # Primary KPI Cards (6-column responsive SaaS layout)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #0284C7;"></div>
            <div class="kpi-title">Active SKUs</div>
            <div class="kpi-value">{total_skus}</div>
            <div class="kpi-subtitle">Catalog items</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #0D9488;"></div>
            <div class="kpi-title">Units in Stock</div>
            <div class="kpi-value">{total_units:,}</div>
            <div class="kpi-subtitle">Physical volume</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #14B8A6;"></div>
            <div class="kpi-title">Stock Valuation</div>
            <div class="kpi-value">${total_valuation:,.2f}</div>
            <div class="kpi-subtitle">Total inventory worth</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #EF4444;"></div>
            <div class="kpi-title" style="color: #DC2626;">Expired Items</div>
            <div class="kpi-value" style="color: #DC2626;">{len(expired_products)}</div>
            <div class="kpi-subtitle" style="color: #EF4444;">Immediate disposal</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #F59E0B;"></div>
            <div class="kpi-title" style="color: #D97706;">Expiring Soon</div>
            <div class="kpi-value" style="color: #D97706;">{len(expiring_today_products) + len(expiring_soon_products)}</div>
            <div class="kpi-subtitle" style="color: #D97706;">Within {warning_days} days</div>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background: #06B6D4;"></div>
            <div class="kpi-title" style="color: #0891B2;">Low / Depleted</div>
            <div class="kpi-value" style="color: #0891B2;">{len(low_stock_products)}</div>
            <div class="kpi-subtitle" style="color: #0891B2;">Require restocking</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 🚨 URGENT OPERATIONS COMMAND CENTER (Highlights specific products needing immediate action)
    st.markdown("""
    <div class="urgent-panel">
        <div class="urgent-header">
            <span>🚨</span>
            <span>Immediate Operational Attention Required</span>
            <span style="font-size: 0.75rem; font-weight: 500; color: #64748B; margin-left: auto;">Prioritized by spoilage risk & supply deficit</span>
        </div>
    """, unsafe_allow_html=True)

    urgent_actions = []
    # Collect expired items
    for p in expired_products:
        urgent_actions.append({
            "badge": '<span class="status-pill pill-expired">EXPIRED</span>',
            "name": f"<strong>{p['name']}</strong> ({p['id']})",
            "detail": f"Overdue by {abs(p['days_until_expiry'])} days | In stock: {p['quantity']} units | Loss risk: <strong>${p['total_stock_value']:.2f}</strong>",
            "action": "Immediate write-off / disposal required"
        })
    # Collect expiring today items
    for p in expiring_today_products:
        urgent_actions.append({
            "badge": '<span class="status-pill pill-today">EXPIRES TODAY</span>',
            "name": f"<strong>{p['name']}</strong> ({p['id']})",
            "detail": f"Expires today | In stock: {p['quantity']} units | Price: ${p['unit_price']:.2f}",
            "action": "Flash discount or promotional clearance"
        })
    # Collect out-of-stock items
    for p in out_of_stock_products:
        urgent_actions.append({
            "badge": '<span class="status-pill pill-lowstock">STOCK DEPLETED</span>',
            "name": f"<strong>{p['name']}</strong> ({p['id']})",
            "detail": f"0 units available | Threshold: {p['min_threshold']} units | Suggested order: {p['reorder']['suggested_units']} units",
            "action": "Submit emergency PO to supplier"
        })

    if not urgent_actions:
        st.markdown("""
        <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px 16px; color: #166534; font-size: 0.88rem;">
            ✅ <strong>All Clear:</strong> No expired products, imminent expirations, or depleted stock levels detected.
        </div>
        """, unsafe_allow_html=True)
    else:
        for action in urgent_actions[:4]:  # Show top 4 most critical
            st.markdown(f"""
            <div class="urgent-item">
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    {action['badge']}
                    <span style="font-size: 0.9rem; color: #0F172A;">{action['name']}</span>
                    <span style="font-size: 0.82rem; color: #64748B;">{action['detail']}</span>
                </div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #0E7490; background: #ECFEFF; padding: 4px 10px; border-radius: 6px; border: 1px solid #CFFAFE;">
                    👉 {action['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Visual Analytics Row
    chart_c1, chart_c2 = st.columns([1, 1])

    with chart_c1:
        st.subheader("Perishability Risk Timeline")
        status_counts = {
            "Expired (Critical)": len(expired_products),
            "Expiring Soon": len(expiring_today_products) + len(expiring_soon_products),
            "Safe Stock": sum(1 for p in all_products if p["expiry_status_key"] == "SAFE"),
            "Non-Perishable": sum(1 for p in all_products if p["expiry_status_key"] == "NO_EXPIRY"),
        }
        df_status = pd.DataFrame(list(status_counts.items()), columns=["Classification", "Count"])
        fig_donut = px.pie(
            df_status,
            names="Classification",
            values="Count",
            color="Classification",
            color_discrete_map={
                "Expired (Critical)": "#EF4444",
                "Expiring Soon": "#F59E0B",
                "Safe Stock": "#10B981",
                "Non-Perishable": "#64748B",
            },
            hole=0.55,
        )
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0F172A"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_c2:
        st.subheader("Stock Health Distribution")
        stock_counts = {
            "Optimal Stock": sum(1 for p in all_products if p["stock_status_key"] == "HEALTHY"),
            "Low Stock": sum(1 for p in all_products if p["stock_status_key"] == "LOW_STOCK"),
            "Depleted (0)": len(out_of_stock_products),
            "Overstocked": sum(1 for p in all_products if p["stock_status_key"] == "OVERSTOCKED"),
        }
        df_stock = pd.DataFrame(list(stock_counts.items()), columns=["Status", "SKU Count"])
        fig_bar = px.bar(
            df_stock,
            x="Status",
            y="SKU Count",
            color="Status",
            color_discrete_map={
                "Optimal Stock": "#10B981",
                "Low Stock": "#F59E0B",
                "Depleted (0)": "#EF4444",
                "Overstocked": "#06B6D4",
            },
        )
        fig_bar.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0F172A"),
            xaxis=dict(gridcolor="#E2E8F0"),
            yaxis=dict(gridcolor="#E2E8F0"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Category Valuation Overview
    st.subheader("Inventory Capital Allocation by Category")
    category_summary = []
    for cat in inventory.CATEGORIES:
        prods = [p for p in all_products if p["category"] == cat]
        if prods:
            units = sum(p["quantity"] for p in prods)
            val = sum(p["total_stock_value"] for p in prods)
            category_summary.append({"Category": cat, "Total Units": units, "Total Valuation ($)": val})

    if category_summary:
        df_cat = pd.DataFrame(category_summary)
        fig_cat = px.bar(
            df_cat,
            x="Category",
            y="Total Valuation ($)",
            text="Total Units",
            color="Total Valuation ($)",
            color_continuous_scale=["#CFFAFE", "#06B6D4", "#0891B2", "#0F172A"],
        )
        fig_cat.update_traces(texttemplate="%{text} units", textposition="outside")
        fig_cat.update_layout(
            margin=dict(t=20, b=10, l=10, r=10),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0F172A"),
            xaxis=dict(gridcolor="#E2E8F0"),
            yaxis=dict(gridcolor="#E2E8F0"),
        )
        st.plotly_chart(fig_cat, use_container_width=True)


# -----------------------------------------------------------------------------
# 5. VIEW: PRODUCT CATALOG & CRUD MANAGEMENT
# -----------------------------------------------------------------------------

elif page == "📦 Product Catalog":
    render_page_header(
        title="Product Catalog & Inventory Management",
        description="Filter products, trigger manual Merge Sort, and execute real-time SQLite database updates.",
        icon="📦",
        badge_text="Pure Python Algorithms"
    )

    # Search & Sorting Toolbelt
    st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: #334155; margin-bottom: 6px;'>1. Search Engine & Ordering Filter</p>", unsafe_allow_html=True)
    
    col_mode, col_query, col_cat, col_sort, col_order = st.columns([1.5, 2.2, 1.4, 1.8, 1])

    with col_mode:
        search_algo = st.selectbox(
            "Search Algorithm",
            ["Linear Search [O(n)]", "Hash Table Lookup [O(1)]"],
            index=0,
            help="Choose between sequential scan across all fields or instant hash table lookup by SKU."
        )

    with col_query:
        if "Linear" in search_algo:
            query = st.text_input("Search Keyword", placeholder="e.g. Milk, Greenfield, SKU-1001...")
        else:
            query = st.text_input("Exact Product SKU", placeholder="e.g. SKU-1001, SKU-1005...")

    with col_cat:
        category_options = ["All Categories"] + inventory.CATEGORIES
        selected_category = st.selectbox("Category", category_options)

    with col_sort:
        sort_field = st.selectbox(
            "Merge Sort Key",
            [
                "Expiration Date (Earliest First)",
                "Quantity (Lowest First)",
                "Unit Price (Lowest First)",
                "Product ID (SKU)",
                "Product Name",
                "Priority Score (Highest First)",
            ],
            index=0
        )

    with col_order:
        sort_order = st.radio("Order", ["Asc", "Desc"], horizontal=True)
        is_reverse = (sort_order == "Desc")

    # Apply category filtering
    items_pool = list(all_products)
    if selected_category != "All Categories":
        items_pool = [p for p in items_pool if p["category"] == selected_category]

    # Apply search algorithm
    if query.strip():
        if "Linear" in search_algo:
            q_clean = query.strip().lower()
            matched, num_comps = algorithms.linear_search(
                items_pool,
                lambda p: q_clean in p["id"].lower() or q_clean in p["name"].lower() or q_clean in p.get("supplier", "").lower()
            )
            items_pool = matched
            st.info(f"🔍 **Linear Search**: Evaluated {num_comps} items sequentially in O(n) time. Found {len(matched)} matching record(s).")
        else:
            target_sku = query.strip().upper()
            hash_match, hash_comps = product_hash_table.get_with_comparisons(target_sku)
            if hash_match and (selected_category == "All Categories" or hash_match.get("category") == selected_category):
                items_pool = [hash_match]
                st.success(f"⚡ **Hash Table O(1) Lookup**: Located **{hash_match['name']}** in just **{hash_comps} comparison(s)** via bucket hash indexing!")
            else:
                items_pool = []
                st.warning(f"Key '{target_sku}' not found in hash table under active category.")

    # Apply MANUAL Divide-and-Conquer Merge Sort
    if "Expiration Date" in sort_field:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["expiration_date"],
            reverse=is_reverse,
            missing_last=True
        )
    elif "Quantity" in sort_field:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["quantity"],
            reverse=is_reverse
        )
    elif "Unit Price" in sort_field:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["unit_price"],
            reverse=is_reverse
        )
    elif "Product ID" in sort_field:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["id"],
            reverse=is_reverse
        )
    elif "Priority Score" in sort_field:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["priority_score"],
            reverse=not is_reverse
        )
    else:
        sorted_catalog = algorithms.merge_sort(
            items_pool,
            key_func=lambda x: x["name"].lower(),
            reverse=is_reverse
        )

    # Render Catalog Table
    if not sorted_catalog:
        st.warning("No inventory records matched your current query and category criteria.")
    else:
        display_rows = []
        for p in sorted_catalog:
            exp_text = p["expiration_date"] if p["expiration_date"] else "Non-Perishable"
            days_str = f" ({p['days_until_expiry']}d)" if p["days_until_expiry"] is not None else ""
            display_rows.append({
                "SKU": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Stock Qty": p["quantity"],
                "Min Threshold": p["min_threshold"],
                "Unit Price ($)": f"${p['unit_price']:.2f}",
                "Valuation ($)": f"${p['total_stock_value']:.2f}",
                "Expiry Date": f"{exp_text}{days_str}",
                "Perishability": p["expiry_status_label"],
                "Stock Status": p["stock_status_label"],
                "Supplier": p.get("supplier", ""),
            })
        st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #0F172A;'>Database Operations (SQLite CRUD)</p>", unsafe_allow_html=True)

    tab_create, tab_modify, tab_remove = st.tabs(["➕ Add New Product", "✏️ Edit Product Details", "🗑️ Remove Product"])

    with tab_create:
        with st.form("form_create_product", clear_on_submit=True):
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                in_id = st.text_input("Product SKU / ID *", placeholder="e.g. SKU-1025").strip().upper()
                in_name = st.text_input("Product Name *", placeholder="e.g. Full Fat Milk 2L").strip()
            with fc2:
                in_cat = st.selectbox("Category *", inventory.CATEGORIES)
                in_supplier = st.text_input("Supplier Name", placeholder="e.g. Almarai, Nestle...")
            with fc3:
                in_price = st.number_input("Unit Price ($)", min_value=0.0, value=3.50, step=0.25)
                is_perishable = st.checkbox("Perishable Product (Has Expiry Date)", value=True)

            fc4, fc5 = st.columns(2)
            with fc4:
                in_qty = st.number_input("Initial Quantity *", min_value=0, value=15, step=1)
                in_thresh = st.number_input("Minimum Threshold *", min_value=0, value=8, step=1)
            with fc5:
                in_expiry = None
                if is_perishable:
                    in_exp_val = st.date_input("Expiration Date", value=date.today())
                    in_expiry = in_exp_val.strftime("%Y-%m-%d")

            btn_create = st.form_submit_button("Commit Product to Database", use_container_width=True, type="primary")
            if btn_create:
                if not in_id or not in_name:
                    st.error("Validation Error: Product SKU and Product Name are mandatory fields.")
                else:
                    try:
                        storage.add_product(storage.DEFAULT_DB_PATH, {
                            "id": in_id,
                            "name": in_name,
                            "category": in_cat,
                            "quantity": int(in_qty),
                            "min_threshold": int(in_thresh),
                            "expiration_date": in_expiry,
                            "unit_price": float(in_price),
                            "supplier": in_supplier,
                        })
                        st.success(f"Product '{in_name}' ({in_id}) stored successfully in SQLite database!")
                        st.rerun()
                    except ValueError as err:
                        st.error(f"Input Error: {err}")

    with tab_modify:
        sku_list = [p["id"] for p in all_products]
        if not sku_list:
            st.info("No products currently registered in database.")
        else:
            sel_sku = st.selectbox("Select SKU to Edit", sku_list, format_func=lambda x: f"{x} - {product_hash_table.get(x, {}).get('name', '')}")
            curr_item = product_hash_table.get(sel_sku)
            if curr_item:
                with st.form("form_edit_product"):
                    me1, me2 = st.columns(2)
                    with me1:
                        edit_name = st.text_input("Product Name", value=curr_item["name"])
                        cat_idx = inventory.CATEGORIES.index(curr_item["category"]) if curr_item["category"] in inventory.CATEGORIES else 0
                        edit_cat = st.selectbox("Category", inventory.CATEGORIES, index=cat_idx)
                        edit_supplier = st.text_input("Supplier", value=curr_item.get("supplier", ""))
                    with me2:
                        edit_qty = st.number_input("Quantity", min_value=0, value=int(curr_item["quantity"]), step=1)
                        edit_thresh = st.number_input("Min Threshold", min_value=0, value=int(curr_item["min_threshold"]), step=1)
                        edit_price = st.number_input("Unit Price ($)", min_value=0.0, value=float(curr_item.get("unit_price", 0.0)), step=0.25)

                    edit_perish = st.checkbox("Perishable Product", value=(curr_item["expiration_date"] is not None))
                    edit_expiry = None
                    if edit_perish:
                        parsed_dt = inventory.parse_date(curr_item["expiration_date"]) or date.today()
                        picked_dt = st.date_input("Expiration Date", value=parsed_dt)
                        edit_expiry = picked_dt.strftime("%Y-%m-%d")

                    btn_save = st.form_submit_button("Save Changes to Database", use_container_width=True, type="primary")
                    if btn_save:
                        try:
                            storage.update_product(storage.DEFAULT_DB_PATH, sel_sku, {
                                "name": edit_name,
                                "category": edit_cat,
                                "quantity": int(edit_qty),
                                "min_threshold": int(edit_thresh),
                                "expiration_date": edit_expiry,
                                "unit_price": float(edit_price),
                                "supplier": edit_supplier,
                            })
                            st.success(f"Product '{sel_sku}' successfully updated.")
                            st.rerun()
                        except Exception as err:
                            st.error(f"Update failed: {err}")

    with tab_remove:
        if not sku_list:
            st.info("No items in inventory.")
        else:
            del_sku = st.selectbox("Select SKU to Remove", sku_list, key="sel_del", format_func=lambda x: f"{x} - {product_hash_table.get(x, {}).get('name', '')}")
            del_item = product_hash_table.get(del_sku)
            if del_item:
                st.warning(f"Are you sure you want to permanently delete **{del_item['name']}** ({del_sku}) from persistent storage?")
                if st.button("🚨 Confirm Deletion", type="primary"):
                    storage.delete_product(storage.DEFAULT_DB_PATH, del_sku)
                    st.success(f"Product {del_sku} removed from SQLite.")
                    st.rerun()


# -----------------------------------------------------------------------------
# 6. VIEW: EXPIRATION ALERTS
# -----------------------------------------------------------------------------

elif page == "⏰ Expiration Alerts":
    render_page_header(
        title="Expiration Alerts & Spoilage Prevention",
        description=f"Active monitoring of perishables categorized by urgency threshold (Warning window: {warning_days} days).",
        icon="⏰",
        badge_text="Waste Reduction System"
    )

    # Segregate items by urgency using manual Merge Sort
    expired_list = algorithms.merge_sort(
        [p for p in all_products if p["expiry_status_key"] == "EXPIRED"],
        key_func=lambda x: x["days_until_expiry"]
    )
    today_list = [p for p in all_products if p["expiry_status_key"] == "EXPIRING_TODAY"]
    soon_list = algorithms.merge_sort(
        [p for p in all_products if p["expiry_status_key"] == "EXPIRING_SOON"],
        key_func=lambda x: x["days_until_expiry"]
    )
    safe_list = algorithms.merge_sort(
        [p for p in all_products if p["expiry_status_key"] == "SAFE"],
        key_func=lambda x: x["days_until_expiry"]
    )
    dry_list = [p for p in all_products if p["expiry_status_key"] == "NO_EXPIRY"]

    # Tabs with live counters
    et1, et2, et3, et4, et5 = st.tabs([
        f"🚨 Expired ({len(expired_list)})",
        f"⚡ Expiring Today ({len(today_list)})",
        f"⚠️ Expiring Soon ({len(soon_list)})",
        f"🛡️ Safe Shelf Life ({len(safe_list)})",
        f"📦 Non-Perishables ({len(dry_list)})",
    ])

    with et1:
        if not expired_list:
            st.success("✅ Zero expired items detected in current stock! Spoilage losses are at $0.00.")
        else:
            loss_total = sum(p["total_stock_value"] for p in expired_list)
            st.error(f"⚠️ **Action Required**: {len(expired_list)} product(s) have passed their expiration date. Total capital at loss risk: **${loss_total:.2f}**.")
            st.dataframe(pd.DataFrame([
                {
                    "SKU": p["id"],
                    "Product Name": p["name"],
                    "Category": p["category"],
                    "Quantity to Write-Off": p["quantity"],
                    "Expiration Date": p["expiration_date"],
                    "Overdue": f"{abs(p['days_until_expiry'])} days ago",
                    "Loss Valuation": f"${p['total_stock_value']:.2f}",
                    "Supplier": p.get("supplier", ""),
                }
                for p in expired_list
            ]), use_container_width=True, hide_index=True)

    with et2:
        if not today_list:
            st.info("No items reaching expiration date today.")
        else:
            st.warning("⚠️ **Clearance Opportunity**: These products expire today. Recommended operational action: apply immediate discount or donate.")
            st.dataframe(pd.DataFrame([
                {
                    "SKU": p["id"],
                    "Product Name": p["name"],
                    "Category": p["category"],
                    "Stock Qty": p["quantity"],
                    "Unit Price": f"${p['unit_price']:.2f}",
                    "Total Value": f"${p['total_stock_value']:.2f}",
                    "Supplier": p.get("supplier", ""),
                }
                for p in today_list
            ]), use_container_width=True, hide_index=True)

    with et3:
        if not soon_list:
            st.success(f"No products expiring within the next {warning_days} days.")
        else:
            st.dataframe(pd.DataFrame([
                {
                    "SKU": p["id"],
                    "Product Name": p["name"],
                    "Category": p["category"],
                    "Days Left": f"{p['days_until_expiry']} days",
                    "Units": p["quantity"],
                    "Expiration Date": p["expiration_date"],
                    "Valuation": f"${p['total_stock_value']:.2f}",
                }
                for p in soon_list
            ]), use_container_width=True, hide_index=True)

    with et4:
        st.dataframe(pd.DataFrame([
            {
                "SKU": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Days Remaining": f"{p['days_until_expiry']} days",
                "Units in Stock": p["quantity"],
                "Expiration Date": p["expiration_date"],
            }
            for p in safe_list
        ]), use_container_width=True, hide_index=True)

    with et5:
        st.dataframe(pd.DataFrame([
            {
                "SKU": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Units in Stock": p["quantity"],
                "Min Threshold": p["min_threshold"],
            }
            for p in dry_list
        ]), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# 7. VIEW: LOW-STOCK & REORDER STATION
# -----------------------------------------------------------------------------

elif page == "⚠️ Low-Stock & Reorder":
    render_page_header(
        title="Low-Stock Alerts & Restocking Center",
        description="Automated depletion detection with deterministic Economic Order Quantity (EOQ) replenishment recommendations.",
        icon="⚠️",
        badge_text="Automated EOQ Engine"
    )

    # Reorder Policy Banner
    st.markdown("""
    <div style="background: #FFFFFF; border-left: 4px solid #0891B2; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; padding: 14px 18px; border-radius: 10px; margin-bottom: 20px;">
        <div style="font-size: 0.9rem; font-weight: 700; color: #0891B2; margin-bottom: 4px;">Deterministic Reordering Math (سياسة إعادة الطلب)</div>
        <div style="font-size: 0.82rem; color: #475569; line-height: 1.5;">
            • Trigger Condition: <code>Quantity &le; Min Threshold</code><br>
            • Optimal Target: <code>2 &times; Min Threshold</code><br>
            • Suggested Order: <code>max(0, (2 &times; Min Threshold) - Quantity)</code><br>
            • Restock Capital Required: <code>Suggested Order &times; Unit Price</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter items needing reorder and sort by lowest stock first
    reorder_items = [p for p in all_products if p["reorder"]["needs_reorder"]]
    reorder_items = algorithms.merge_sort(reorder_items, key_func=lambda x: x["quantity"])

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.metric("SKUs Needing Reorder", len(reorder_items))
    with rc2:
        tot_units = sum(p["reorder"]["suggested_units"] for p in reorder_items)
        st.metric("Total Replenishment Units", tot_units)
    with rc3:
        tot_cost = sum(p["reorder"]["estimated_cost"] for p in reorder_items)
        st.metric("Estimated Restocking Cost", f"${tot_cost:,.2f}")

    if not reorder_items:
        st.success("All inventory stock levels meet or exceed minimum safety thresholds!")
    else:
        st.dataframe(pd.DataFrame([
            {
                "SKU": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Current Qty": p["quantity"],
                "Min Threshold": p["min_threshold"],
                "Suggested Order": f"{p['reorder']['suggested_units']} units",
                "Unit Price": f"${p['unit_price']:.2f}",
                "Restock Cost": f"${p['reorder']['estimated_cost']:.2f}",
                "Supplier": p.get("supplier", ""),
            }
            for p in reorder_items
        ]), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("<p style='font-size: 0.95rem; font-weight: 700; color: #0F172A;'>⚡ Quick Stock Receiving Station</p>", unsafe_allow_html=True)
    st.caption("Receive a supplier shipment or adjust on-hand inventory immediately without leaving this view.")

    if reorder_items:
        rq1, rq2, rq3 = st.columns([2, 1, 1])
        with rq1:
            restock_sku = st.selectbox(
                "Select Product to Restock",
                [p["id"] for p in reorder_items],
                format_func=lambda x: f"{x} - {product_hash_table.get(x, {}).get('name', '')} (Current: {product_hash_table.get(x, {}).get('quantity', 0)})"
            )
        target_item = product_hash_table.get(restock_sku)
        with rq2:
            suggested_def = target_item["reorder"]["suggested_units"] if target_item else 10
            received_qty = st.number_input("Units Received (+)", min_value=1, value=max(1, suggested_def), step=1)
        with rq3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("📥 Receive & Update SQLite", use_container_width=True, type="primary"):
                updated_stock = target_item["quantity"] + received_qty
                storage.update_product(storage.DEFAULT_DB_PATH, restock_sku, {
                    "name": target_item["name"],
                    "category": target_item["category"],
                    "quantity": updated_stock,
                    "min_threshold": target_item["min_threshold"],
                    "expiration_date": target_item["expiration_date"],
                    "unit_price": target_item["unit_price"],
                    "supplier": target_item.get("supplier", ""),
                })
                st.success(f"Stock for '{target_item['name']}' increased from {target_item['quantity']} -> {updated_stock} units.")
                st.rerun()


# -----------------------------------------------------------------------------
# 8. VIEW: PRIORITY ACTION MATRIX
# -----------------------------------------------------------------------------

elif page == "🎯 Priority Action Matrix":
    render_page_header(
        title="Algorithmic Priority Action Matrix",
        description="Multi-factor mathematical ranking algorithm scoring operational urgency across spoilage, shortages, and capital at risk.",
        icon="🎯",
        badge_text="Explainable Deterministic Scoring"
    )

    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px 18px; border-radius: 10px; margin-bottom: 20px; font-size: 0.84rem; line-height: 1.55;">
        <span style="font-weight: 700; color: #0F172A;">Multi-Factor Mathematical Formulation:</span><br>
        $$\\text{Priority Score} = \\text{Spoilage Risk (up to 80 pts)} + \\text{Stock Shortage Ratio (up to 35 pts)} + \\text{Capital at Risk (up to 15 pts)}$$
        <em>Tiers: <strong>CRITICAL</strong> (&ge; 70), <strong>HIGH</strong> (45–69), <strong>MEDIUM</strong> (20–44), <strong>LOW</strong> (&lt; 20). No black-box AI claims.</em>
    </div>
    """, unsafe_allow_html=True)

    # Sort all items by priority score descending via Merge Sort
    prioritized_list = algorithms.merge_sort(
        all_products,
        key_func=lambda x: x["priority_score"],
        reverse=True
    )

    filter_urgency = st.selectbox("Filter Tier", ["All Tiers", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    if filter_urgency != "All Tiers":
        prioritized_list = [p for p in prioritized_list if p["priority_urgency"] == filter_urgency]

    st.dataframe(pd.DataFrame([
        {
            "Urgency Tier": p["priority_urgency"],
            "Score": p["priority_score"],
            "SKU": p["id"],
            "Product Name": p["name"],
            "Stock Level": f"{p['quantity']} / {p['min_threshold']}",
            "Expiration": p["expiration_date"] if p["expiration_date"] else "No Expiry",
            "Urgency Rationale": p["priority_reason"],
        }
        for p in prioritized_list
    ]), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# 9. VIEW: ALGORITHM LAB (ACADEMIC SHOWCASE)
# -----------------------------------------------------------------------------

elif page == "🔬 Algorithm Lab":
    render_page_header(
        title="Algorithm Lab & Academic Showcase",
        description="Live demonstration of Divide-and-Conquer Merge Sort, Chained Hash Tables with collision resolution, and Linear Search.",
        icon="🔬",
        badge_text="Academic Rubric Compliant"
    )

    lab_tab1, lab_tab2, lab_tab3, lab_tab4 = st.tabs([
        "⚡ 1. Search Benchmark: O(n) vs O(1)",
        "🗄️ 2. Hash Table Inspector & Collisions",
        "🔀 3. Merge Sort Divide & Conquer Visualizer",
        "📈 4. Empirical Scaling Benchmark Suite",
    ])

    with lab_tab1:
        st.markdown("""
        <div class="algo-card">
            <div class="algo-card-title">
                <span>Linear Search $O(n)$ vs Chained Hash Table $O(1)$</span>
                <span class="algo-pill">SUHA: Average O(1)</span>
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin: 0;">
                Select any SKU to execute simultaneous searches. We count the exact number of key equality comparisons and measure elapsed CPU time via <code>time.perf_counter()</code>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        sku_choices = [p["id"] for p in all_products]
        sc1, sc2 = st.columns([2.5, 1])
        with sc1:
            picked_sku = st.selectbox("Select Target SKU to Search", sku_choices, index=min(len(sku_choices)-1, 15))
        with sc2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            trigger_comp = st.button("Execute Comparison", type="primary", use_container_width=True)

        if trigger_comp or picked_sku:
            # Measure Linear Search
            t_start_lin = time.perf_counter()
            lin_res, lin_comps = algorithms.linear_search_by_id(all_products, picked_sku)
            t_lin_us = (time.perf_counter() - t_start_lin) * 1e6

            # Measure Hash Table
            t_start_hash = time.perf_counter()
            hash_res, hash_comps = product_hash_table.get_with_comparisons(picked_sku)
            t_hash_us = (time.perf_counter() - t_start_hash) * 1e6

            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.markdown(f"""
                <div class="algo-card" style="border-top: 4px solid #64748B;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Sequential Linear Scan</div>
                    <div style="font-size: 1.7rem; font-weight: 800; color: #0F172A; margin: 4px 0;">{lin_comps} <span style="font-size: 0.9rem; font-weight: 500; color: #64748B;">comparisons</span></div>
                    <div style="font-size: 0.88rem; color: #0F172A;">CPU Latency: <strong>{t_lin_us:.2f} &micro;s</strong></div>
                    <div style="font-size: 0.78rem; color: #64748B; margin-top: 8px;">
                        • Theoretical Time: <code>O(n)</code><br>
                        • Must iterate index by index until key match.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with res_c2:
                st.markdown(f"""
                <div class="algo-card" style="border-top: 4px solid #0891B2;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #0891B2; text-transform: uppercase;">Chained Hash Table Lookup</div>
                    <div style="font-size: 1.7rem; font-weight: 800; color: #0891B2; margin: 4px 0;">{hash_comps} <span style="font-size: 0.9rem; font-weight: 500; color: #0891B2;">comparison</span></div>
                    <div style="font-size: 0.88rem; color: #0F172A;">CPU Latency: <strong>{t_hash_us:.2f} &micro;s</strong></div>
                    <div style="font-size: 0.78rem; color: #0891B2; margin-top: 8px;">
                        • Theoretical Time: <code>O(1)</code> under SUHA<br>
                        • Direct bucket hash index jump + head lookup.
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with lab_tab2:
        st.markdown("""
        <div class="algo-card">
            <div class="algo-card-title">
                <span>Custom Hash Table Architecture & Collision Analysis</span>
                <span class="algo-pill">Separate Chaining</span>
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin: 0;">
                Polynomial rolling hash function: <code>h(k) = (sum(ord(c) * 31^i)) mod capacity</code>. Collisions are handled via linked nodes in each bucket array slot. Automatic capacity doubling triggers when load factor <code>&alpha; > 0.75</code>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        ht_info = product_hash_table.get_stats()
        h1, h2, h3, h4 = st.columns(4)
        h1.metric("Bucket Capacity (m)", ht_info["capacity"])
        h2.metric("Stored Elements (n)", ht_info["size"])
        h3.metric("Load Factor (α = n/m)", ht_info["load_factor"])
        h4.metric("Collision Chains", ht_info["total_collisions"])

        st.markdown("<p style='font-size: 0.9rem; font-weight: 700; color: #0F172A; margin: 12px 0 6px 0;'>Live Bucket Memory Distribution</p>", unsafe_allow_html=True)
        chains = product_hash_table.get_chain_inspection()
        st.dataframe(pd.DataFrame([
            {
                "Bucket #": b["bucket_index"],
                "Chain Nodes": b["chain_length"],
                "Keys in Bucket": ", ".join(b["keys"]) if b["keys"] else "(empty)",
            }
            for b in chains
        ]), use_container_width=True, hide_index=True)

    with lab_tab3:
        st.markdown("""
        <div class="algo-card">
            <div class="algo-card-title">
                <span>Divide-and-Conquer Merge Sort Execution Trace</span>
                <span class="algo-pill">T(n) = 2T(n/2) + Θ(n) ⟹ Θ(n log n)</span>
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin: 0;">
                Merge Sort recursively halves the dataset until subarrays contain 1 item, then recombines them stably using two pointers. Auxiliary memory required: $O(n)$.
            </p>
        </div>
        """, unsafe_allow_html=True)

        subset_names = [p["name"] for p in all_products[:6]]
        sorted_output, trace = algorithms.merge_sort_with_trace(subset_names)

        st.markdown(f"**Sample Input (6 products):** `{subset_names}`")
        st.markdown(f"**Final Sorted Output:** `{sorted_output}`")
        st.markdown("<p style='font-size: 0.9rem; font-weight: 700; color: #0F172A; margin: 12px 0 6px 0;'>Step-by-Step Recursive State Progression</p>", unsafe_allow_html=True)

        for step in trace:
            if step["action"] == "DIVIDE":
                st.markdown(f"""
                <div style="background: #F8FAFC; border-left: 4px solid #64748B; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.84rem;">
                    <span style="font-weight: 700; color: #334155;">Step {step['step']} [DIVIDE]:</span> {step['description']}<br>
                    <span style="color: #64748B;">Left: <code>{step['left']}</code> | Right: <code>{step['right']}</code></span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #F0FDFA; border-left: 4px solid #0D9488; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.84rem;">
                    <span style="font-weight: 700; color: #0D9488;">Step {step['step']} [MERGE]:</span> {step['description']}
                </div>
                """, unsafe_allow_html=True)

    with lab_tab4:
        st.markdown("""
        <div class="algo-card">
            <div class="algo-card-title">
                <span>Empirical Scaling Benchmark Suite</span>
                <span class="algo-pill">N = 100 to 5,000</span>
            </div>
            <p style="color: #64748B; font-size: 0.85rem; margin: 0;">
                Benchmarking sequential search $O(n)$ against hash lookup $O(1)$ across progressively scaling synthetic datasets.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Run Synthetic Scaling Benchmark", type="primary"):
            sizes = [100, 500, 1000, 2500, 5000]
            lin_ms = []
            hash_ms = []

            with st.spinner("Executing benchmark across synthetic arrays..."):
                for n in sizes:
                    items = [{"id": f"SKU-{i:06d}", "val": i} for i in range(n)]
                    ht = algorithms.ChainedHashTable(initial_capacity=n * 2)
                    for itm in items:
                        ht.put(itm["id"], itm)

                    target = f"SKU-{n-1:06d}"  # worst-case target at tail

                    # Linear search
                    t0 = time.perf_counter()
                    algorithms.linear_search_by_id(items, target)
                    lin_ms.append((time.perf_counter() - t0) * 1e3)

                    # Hash lookup
                    t1 = time.perf_counter()
                    ht.get(target)
                    hash_ms.append((time.perf_counter() - t1) * 1e3)

            df_bench = pd.DataFrame({
                "Dataset Size (N)": sizes,
                "Linear Search O(n) [ms]": lin_ms,
                "Hash Table Lookup O(1) [ms]": hash_ms,
            })

            fig_bench = go.Figure()
            fig_bench.add_trace(go.Scatter(
                x=df_bench["Dataset Size (N)"],
                y=df_bench["Linear Search O(n) [ms]"],
                mode="lines+markers",
                name="Linear Search O(n)",
                line=dict(color="#EF4444", width=3)
            ))
            fig_bench.add_trace(go.Scatter(
                x=df_bench["Dataset Size (N)"],
                y=df_bench["Hash Table Lookup O(1) [ms]"],
                mode="lines+markers",
                name="Hash Table Lookup O(1)",
                line=dict(color="#06B6D4", width=3)
            ))
            fig_bench.update_layout(
                title="Empirical Lookup Latency vs Dataset Size (N)",
                xaxis_title="Input Size (N items)",
                yaxis_title="Latency (milliseconds)",
                margin=dict(t=40, b=20, l=10, r=10),
                height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", color="#0F172A"),
                xaxis=dict(gridcolor="#E2E8F0"),
                yaxis=dict(gridcolor="#E2E8F0"),
            )
            st.plotly_chart(fig_bench, use_container_width=True)
            st.dataframe(df_bench, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# 10. VIEW: INVENTORY REPORTS & CSV EXPORT
# -----------------------------------------------------------------------------

elif page == "📑 Inventory Reports":
    render_page_header(
        title="Inventory Reports & CSV Export",
        description="Generate formatted operational summaries and download sanitized CSV audits for external accounting.",
        icon="📑",
        badge_text="Sanitized Data Export"
    )

    selected_report = st.selectbox(
        "Select Report Template",
        [
            "Full Master Inventory",
            "Expired Products Report (Disposal Audit)",
            "Low-Stock Reorder Order Sheet",
            "Category Valuation Summary",
        ]
    )

    if selected_report == "Full Master Inventory":
        df_rep = pd.DataFrame([
            {
                "Product ID": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Quantity": p["quantity"],
                "Min Threshold": p["min_threshold"],
                "Unit Price ($)": p["unit_price"],
                "Total Valuation ($)": p["total_stock_value"],
                "Expiration Date": p["expiration_date"],
                "Perishability": p["expiry_status_label"],
                "Stock Status": p["stock_status_label"],
                "Supplier": p.get("supplier", ""),
            }
            for p in all_products
        ])
    elif selected_report == "Expired Products Report (Disposal Audit)":
        expired_only = [p for p in all_products if p["expiry_status_key"] == "EXPIRED"]
        df_rep = pd.DataFrame([
            {
                "Product ID": p["id"],
                "Product Name": p["name"],
                "Category": p["category"],
                "Units to Dispose": p["quantity"],
                "Expiration Date": p["expiration_date"],
                "Days Overdue": abs(p["days_until_expiry"]),
                "Financial Loss ($)": p["total_stock_value"],
                "Supplier": p.get("supplier", ""),
            }
            for p in expired_only
        ])
    elif selected_report == "Low-Stock Reorder Order Sheet":
        low_only = [p for p in all_products if p["reorder"]["needs_reorder"]]
        df_rep = pd.DataFrame([
            {
                "Product ID": p["id"],
                "Product Name": p["name"],
                "Supplier": p.get("supplier", ""),
                "Current Stock": p["quantity"],
                "Min Threshold": p["min_threshold"],
                "Suggested Order Units": p["reorder"]["suggested_units"],
                "Unit Price ($)": p["unit_price"],
                "Restock Cost ($)": p["reorder"]["estimated_cost"],
            }
            for p in low_only
        ])
    else:  # Category Valuation Summary
        cat_agg = []
        for cat in inventory.CATEGORIES:
            cat_p = [p for p in all_products if p["category"] == cat]
            if cat_p:
                cat_agg.append({
                    "Category": cat,
                    "Total SKUs": len(cat_p),
                    "Total Units": sum(p["quantity"] for p in cat_p),
                    "Valuation ($)": round(sum(p["total_stock_value"] for p in cat_p), 2),
                    "Expired Count": sum(1 for p in cat_p if p["expiry_status_key"] == "EXPIRED"),
                    "Low Stock Count": sum(1 for p in cat_p if p["stock_status_key"] in ("OUT_OF_STOCK", "LOW_STOCK")),
                })
        df_rep = pd.DataFrame(cat_agg)

    st.dataframe(df_rep, use_container_width=True, hide_index=True)

    csv_bytes = df_rep.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇️ Download {selected_report} (CSV)",
        data=csv_bytes,
        file_name=f"{selected_report.lower().replace(' ', '_')}_{date.today().isoformat()}.csv",
        mime="text/csv",
        type="primary"
    )
