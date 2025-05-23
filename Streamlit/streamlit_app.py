import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Page config
st.set_page_config(
    page_title="Retail Dashboard",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
/* Main container */
.main {
    background-color: #f8fafc;
}
/* Header */
.header {
    padding: 0.5rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    background-color: #1d4ed8;
    border-radius: 8px;
    padding: 1rem;
}
.header h1 {
    color: #ffffff !important;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0;
}
.header p {
    color: #e2e8f0;
    text-align: center;
    margin-top: 0.5rem;
}
/* Cards */
.metric-card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    text-align: center;
    margin-bottom: 1rem;
    border-left: 4px solid #1d4ed8;
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.metric-card h4 {
    margin: 0;
    font-size: 0.9rem;
    color: #000000;  /* Black title */
    font-weight: 600;
    letter-spacing: 0.5px;
}
.metric-card p {
    margin: 8px 0 0;
    font-size: 1.5rem;
    color: #1e293b;
    font-weight: 700;
}
/* Chart containers */
.chart-container {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.chart-container h3 {
    color: #1e293b;
    margin: 0.5rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    text-align: center;
}
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
/* Column spacing */
[data-testid="column"] {
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Constants ---
THEME_COLOR = "#1d4ed8"
SECONDARY_COLOR = "#64748b"


# --- Database Connection ---
@st.cache_resource
def init_connection():
    try:
        db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/retail_dwh"
        return create_engine(db_url)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()


@st.cache_data(ttl=600)
def load_data(query):
    engine = init_connection()
    return pd.read_sql(query, engine)


# --- KPI Metrics ---
def display_kpis(fact_sales):
    total_qty = fact_sales["QuantitySold"].sum()
    total_sales = fact_sales["TotalSales"].sum()
    net_sales = fact_sales["NetSales"].sum()
    avg_discount = fact_sales["DiscountAmount"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Total Quantity Sold</h4>
            <p>{int(total_qty):,}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Total Sales</h4>
            <p>${int(total_sales):,}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Net Sales</h4>
            <p>${int(net_sales):,}</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Avg Discount</h4>
            <p>${avg_discount:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)


# --- Top Stores by Sales ---
def get_top_stores():
    query = """
    SELECT s."StoreName", SUM(f."QuantitySold") AS quantitysold
    FROM dbt.fact f
    JOIN dbt.dim_store s ON f.store_key = s.store_key
    GROUP BY s."StoreName"
    ORDER BY quantitysold DESC
    LIMIT 5
    """
    return load_data(query)


# --- Monthly Sales Trend ---
def get_yearly_sales():
    query = """
    SELECT d.year, SUM(f."NetSales") AS netsales
    FROM dbt.fact f
    JOIN dbt.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year
    ORDER BY d.year
    """
    df = load_data(query)
    df['year'] = df['year'].astype(int)  # Ensure year is integer
    return df


# --- Top Products ---
def get_top_products():
    query = """
    SELECT p."ProductName", SUM(f."QuantitySold") AS quantitysold
    FROM dbt.fact f
    JOIN dbt.dim_product p ON f.product_key = p.product_key
    GROUP BY p."ProductName"
    ORDER BY quantitysold DESC
    LIMIT 5
    """
    return load_data(query)


# --- Promotions Impact ---
def get_promotion_impact():
    query = """
    SELECT pr."PromotionName", SUM(f."NetSales") AS netsales
    FROM dbt.fact f
    JOIN dbt.dim_promotion pr ON f.promotion_key = pr.promotion_key
    GROUP BY pr."PromotionName"
    ORDER BY netsales DESC
    LIMIT 5
    """
    return load_data(query)


# --- Load full fact table ---
def load_fact_sales():
    return load_data("SELECT * FROM dbt.fact")


# --- Charts in Main ---
def main():
    # Header with white title
    st.markdown("""
    <div class="header">
        <h1>📊 Retail Analytics Dashboard</h1>
        <p>Key metrics and insights from your retail operations</p>
    </div>
    """, unsafe_allow_html=True)

    fact_sales = load_fact_sales()
    display_kpis(fact_sales)

    # --- First Row: Top Stores & Yearly Sales ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="chart-container">
            <h3>🏬 Top 5 Stores by Quantity Sold</h3>
        """, unsafe_allow_html=True)
        top_stores = get_top_stores()
        fig1 = px.bar(
            top_stores,
            x="StoreName",
            y="quantitysold",
            height=400,
            color_discrete_sequence=[THEME_COLOR],
            text="quantitysold"
        )
        fig1.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.8
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Quantity Sold",
            xaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="chart-container">
            <h3>📈 Yearly Net Sales Trend</h3>
        """, unsafe_allow_html=True)
        yearly_sales = get_yearly_sales()
        fig2 = px.line(
            yearly_sales,
            x="year",
            y="netsales",
            height=400,
            markers=True,
            color_discrete_sequence=[THEME_COLOR],
            text="netsales"
        )
        fig2.update_traces(
            line_width=3,
            marker_size=10,
            texttemplate='$%{text:,.0f}',
            textposition="top center"
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Net Sales ($)",
            xaxis_title="Year",
            xaxis=dict(
                tickmode='array',
                tickvals=yearly_sales['year'].unique(),
                ticktext=yearly_sales['year'].unique().astype(str)
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Second Row: Top Products & Promotions ---
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="chart-container">
            <h3>🛒 Top 5 Products by Quantity Sold</h3>
        """, unsafe_allow_html=True)
        top_products = get_top_products()
        fig3 = px.bar(
            top_products,
            x="quantitysold",
            y="ProductName",
            orientation='h',
            height=500,
            color_discrete_sequence=[THEME_COLOR],
            text="quantitysold"
        )
        fig3.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.8
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Quantity Sold",
            yaxis_title="",
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="chart-container">
            <h3>🎯 Promotion Impact on Net Sales</h3>
        """, unsafe_allow_html=True)
        promo_impact = get_promotion_impact()
        fig4 = px.pie(
            promo_impact,
            names="PromotionName",
            values="netsales",
            height=500,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig4.update_traces(
            textinfo='percent+value',
            texttemplate='%{percent}<br>$%{value:,.0f}',
            marker=dict(line=dict(color='#ffffff', width=2)),
            pull=[0.1 if i == 0 else 0 for i in range(len(promo_impact))],
            showlegend=False
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()