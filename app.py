import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Singapore's Business Formation Trends", page_icon="📊", layout="wide")

# Custom CSS for KPI cards and Top Padding
st.markdown("""
    <style>
    /* Remove top padding to bring title up */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    .kpi-card {
        background-color: #f8f9fa; padding: 20px;
        border-radius: 10px; text-align: center;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .kpi-value { font-size: 32px; font-weight: 700; color: #1f77b4; }
    .kpi-label { font-size: 14px; color: #6c757d; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px;}
    </style>
""", unsafe_allow_html=True)

# 2. Load Data
@st.cache_data
def load_data():
    conn = sqlite3.connect("business_data.db")
    query = "SELECT Industry, Year, New_Registrations FROM registrations"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# 3. Header
st.title("Singapore's Business Formation Trends")
st.write("") 

# 4. Sidebar
with st.sidebar:
    st.header("Dashboard Filters")
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    
    selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    
    all_industries = sorted(df['Industry'].unique())
    selected_industries = st.multiselect("Select Industries (Leave blank for all):", options=all_industries)

# 5. Filtering Logic
filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
if selected_industries:
    filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]

if filtered_df.empty:
    st.warning("No data available. Please adjust your filters.")
    st.stop()

# 6. KPI Metrics
first_year = int(filtered_df['Year'].min())
latest_year = int(filtered_df['Year'].max())

total_regs = filtered_df['New_Registrations'].sum()
latest_year_regs = filtered_df[filtered_df['Year'] == latest_year]['New_Registrations'].sum()
first_year_regs = filtered_df[filtered_df['Year'] == first_year]['New_Registrations'].sum()
growth_pct = ((latest_year_regs - first_year_regs) / first_year_regs) * 100 if first_year_regs > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_regs:,.0f}</div><div class="kpi-label">Total Volume ({first_year}-{latest_year})</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{latest_year_regs:,.0f}</div><div class="kpi-label">Latest Year ({latest_year})</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-value">{growth_pct:+.1f}%</div><div class="kpi-label">Total Growth ({first_year} to {latest_year})</div></div>', unsafe_allow_html=True)

st.write("")

# 7. TABS LAYOUT
tab1, tab2, tab3 = st.tabs(["📊 Trends & Analysis", "🏆 Industry Overview", "🔍 Raw Data"])

with tab1:
    # --- LINE CHART ---
    fig_line = px.line(
        filtered_df, x="Year", y="New_Registrations", color="Industry", markers=True,
        title=f"Historical Registrations ({first_year}-{latest_year})",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_line.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='Lightgray'))
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.divider()
    
    # --- HISTORICAL BUSINESS INTELLIGENCE ---
    st.subheader("📑 Historical Market Intelligence")
    st.markdown("Key data-driven insights extracted from the selected time period.")
    
    df_pivot = filtered_df.pivot(index='Year', columns='Industry', values='New_Registrations')
    df_diff = df_pivot.diff()
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown("#### 📈 Market Surges")
        if not df_diff.empty and df_diff.notna().any().any():
            max_increase_ind = df_diff.max().idxmax()
            max_inc_year = df_diff[max_increase_ind].idxmax()
            max_inc_val = df_diff[max_increase_ind].max()
            st.success(f"**{max_increase_ind}** experienced the largest single-year expansion in **{max_inc_year}**, adding **{max_inc_val:,.0f}** new registrations.")
            
    with col_insight2:
        st.markdown("#### 📉 Market Contractions")
        if not df_diff.empty and df_diff.notna().any().any():
            max_decrease_ind = df_diff.min().idxmin()
            max_dec_year = df_diff[max_decrease_ind].idxmin()
            max_dec_val = df_diff[max_decrease_ind].min()
            if max_dec_val < 0:
                st.error(f"**{max_decrease_ind}** faced the sharpest contraction in **{max_dec_year}**, losing **{abs(max_dec_val):,.0f}** registrations.")
            else:
                st.info("No negative growth was recorded in the selected timeframe.")

    st.markdown("#### 📊 Long-Term Growth (CAGR)")
    st.markdown("Compound Annual Growth Rate (CAGR) represents the mean annual growth rate over the selected time period.")
    
    cagr_data = []
    years_diff = latest_year - first_year
    if years_diff > 0:
        for ind in filtered_df['Industry'].unique():
            ind_df = filtered_df[filtered_df['Industry'] == ind].sort_values('Year')
            start_rows = ind_df[ind_df['Year'] == first_year]['New_Registrations']
            end_rows = ind_df[ind_df['Year'] == latest_year]['New_Registrations']
            
            if not start_rows.empty and not end_rows.empty:
                start_val = start_rows.values[0]
                end_val = end_rows.values[0]
                
                if start_val > 0 and end_val > 0:
                    cagr = ((end_val / start_val) ** (1/years_diff) - 1) * 100
                    cagr_data.append({"Industry": ind, "CAGR": cagr})
                    
        if cagr_data:
            cagr_df = pd.DataFrame(cagr_data).sort_values(by="CAGR", ascending=False)
            top_cagr = cagr_df.iloc[0]
            st.info(f"**{top_cagr['Industry']}** demonstrated the strongest long-term resilience and growth, achieving a CAGR of **{top_cagr['CAGR']:.2f}%** annually between {first_year} and {latest_year}.")

with tab2:
    total_df = filtered_df.groupby("Industry")["New_Registrations"].sum().reset_index().sort_values("New_Registrations", ascending=False)
    fig_bar = px.bar(
        total_df, x="Industry", y="New_Registrations", color="Industry",
        title=f"Total Volume by Industry ({first_year}-{latest_year})",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_bar.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='Lightgray'))
    st.plotly_chart(fig_bar, use_container_width=True)
    
    top_ind = total_df.iloc[0]
    st.info(f"**Market Volume Leader:** **{top_ind['Industry']}** dominates the selected timeframe with a total of {top_ind['New_Registrations']:,.0f} registrations.")

with tab3:
    st.dataframe(filtered_df.sort_values(by=["Industry", "Year"]), use_container_width=True)

# 8. FOOTER (Fixed to bottom of content, not floating)
st.markdown("---") # A subtle line above the footer
st.markdown(
    "<div style='text-align: right; color: #888888; font-size: 12px; padding-bottom: 20px;'>An empirical analysis of ACRA business registrations. <b>Data Source: data.gov.sg</b></div>", 
    unsafe_allow_html=True
)