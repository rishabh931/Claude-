import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indian Stock PnL Analyzer",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Indian Stock PnL Statement Analysis")
st.markdown("Enter an Indian stock symbol to get comprehensive Profit & Loss analysis with visual insights")

# Sidebar for inputs
st.sidebar.header("Stock Selection")
stock_input = st.sidebar.text_input(
    "Enter Stock Symbol or Name", 
    placeholder="e.g., RELIANCE.NS, TCS.NS, INFY.NS",
    help="Add .NS suffix for NSE stocks or .BO for BSE stocks"
)

# Common Indian stock symbols for quick selection
st.sidebar.subheader("Popular Indian Stocks")
popular_stocks = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "ITC": "ITC.NS",
    "Wipro": "WIPRO.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Maruti Suzuki": "MARUTI.NS"
}

selected_stock = st.sidebar.selectbox("Or select from popular stocks:", [""] + list(popular_stocks.keys()))

if selected_stock:
    stock_symbol = popular_stocks[selected_stock]
elif stock_input:
    stock_symbol = stock_input.upper()
    if not (stock_symbol.endswith('.NS') or stock_symbol.endswith('.BO')):
        stock_symbol += '.NS'
else:
    stock_symbol = None

def get_stock_info(symbol):
    """Fetch stock information and financial data"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        financials = stock.financials
        quarterly_financials = stock.quarterly_financials
        return stock, info, financials, quarterly_financials
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None, None, None

def analyze_pnl_trends(financials):
    """Analyze PnL trends and calculate key metrics"""
    if financials is None or financials.empty:
        return None
    
    analysis = {}
    
    # Key financial metrics
    revenue = financials.loc['Total Revenue'] if 'Total Revenue' in financials.index else None
    gross_profit = financials.loc['Gross Profit'] if 'Gross Profit' in financials.index else None
    operating_income = financials.loc['Operating Income'] if 'Operating Income' in financials.index else None
    net_income = financials.loc['Net Income'] if 'Net Income' in financials.index else None
    
    if revenue is not None:
        analysis['revenue'] = revenue
        analysis['revenue_growth'] = revenue.pct_change().fillna(0) * 100
    
    if gross_profit is not None:
        analysis['gross_profit'] = gross_profit
        analysis['gross_margin'] = (gross_profit / revenue * 100) if revenue is not None else None
    
    if operating_income is not None:
        analysis['operating_income'] = operating_income
        analysis['operating_margin'] = (operating_income / revenue * 100) if revenue is not None else None
    
    if net_income is not None:
        analysis['net_income'] = net_income
        analysis['net_margin'] = (net_income / revenue * 100) if revenue is not None else None
    
    return analysis

def create_pnl_visualizations(analysis, company_name):
    """Create comprehensive PnL visualizations"""
    
    if not analysis or 'revenue' not in analysis:
        st.warning("Insufficient financial data for visualization")
        return
    
    # Revenue and Profitability Trend
    fig1 = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Trend', 'Profit Margins', 'Revenue Growth Rate', 'Profitability Comparison'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Revenue trend
    years = analysis['revenue'].index.year
    revenue_values = analysis['revenue'].values / 1e9  # Convert to billions
    
    fig1.add_trace(
        go.Bar(x=years, y=revenue_values, name='Revenue (₹ Billions)', marker_color='lightblue'),
        row=1, col=1
    )
    
    # Profit margins
    if 'gross_margin' in analysis and analysis['gross_margin'] is not None:
        fig1.add_trace(
            go.Scatter(x=years, y=analysis['gross_margin'].values, name='Gross Margin %', 
                      line=dict(color='green', width=3)),
            row=1, col=2
        )
    
    if 'operating_margin' in analysis and analysis['operating_margin'] is not None:
        fig1.add_trace(
            go.Scatter(x=years, y=analysis['operating_margin'].values, name='Operating Margin %',
                      line=dict(color='orange', width=3)),
            row=1, col=2
        )
    
    if 'net_margin' in analysis and analysis['net_margin'] is not None:
        fig1.add_trace(
            go.Scatter(x=years, y=analysis['net_margin'].values, name='Net Margin %',
                      line=dict(color='red', width=3)),
            row=1, col=2
        )
    
    # Revenue growth rate
    if 'revenue_growth' in analysis:
        fig1.add_trace(
            go.Bar(x=years, y=analysis['revenue_growth'].values, name='Revenue Growth %',
                   marker_color=['green' if x > 0 else 'red' for x in analysis['revenue_growth'].values]),
            row=2, col=1
        )
    
    # Profitability comparison
    if all(k in analysis for k in ['gross_profit', 'operating_income', 'net_income']):
        profit_data = pd.DataFrame({
            'Gross Profit': analysis['gross_profit'].values / 1e9,
            'Operating Income': analysis['operating_income'].values / 1e9,
            'Net Income': analysis['net_income'].values / 1e9
        }, index=years)
        
        for col in profit_data.columns:
            fig1.add_trace(
                go.Bar(x=years, y=profit_data[col], name=f'{col} (₹ Billions)'),
                row=2, col=2
            )
    
    fig1.update_layout(height=800, title_text=f"{company_name} - Comprehensive PnL Analysis")
    st.plotly_chart(fig1, use_container_width=True)

def generate_pnl_insights(analysis, info):
    """Generate key insights from PnL analysis"""
    insights = []
    
    if 'revenue' in analysis:
        latest_revenue = analysis['revenue'].iloc[0] / 1e9
        insights.append(f"**Latest Annual Revenue**: ₹{latest_revenue:.2f} billion")
        
        if len(analysis['revenue']) > 1:
            revenue_change = analysis['revenue_growth'].iloc[0]
            trend = "increased" if revenue_change > 0 else "decreased"
            insights.append(f"**Revenue Growth**: Revenue {trend} by {abs(revenue_change):.1f}% year-over-year")
    
    if 'gross_margin' in analysis and analysis['gross_margin'] is not None:
        latest_gross_margin = analysis['gross_margin'].iloc[0]
        insights.append(f"**Gross Margin**: {latest_gross_margin:.1f}% - indicates pricing power and cost efficiency")
    
    if 'operating_margin' in analysis and analysis['operating_margin'] is not None:
        latest_op_margin = analysis['operating_margin'].iloc[0]
        insights.append(f"**Operating Margin**: {latest_op_margin:.1f}% - shows operational efficiency")
    
    if 'net_margin' in analysis and analysis['net_margin'] is not None:
        latest_net_margin = analysis['net_margin'].iloc[0]
        insights.append(f"**Net Margin**: {latest_net_margin:.1f}% - overall profitability after all expenses")
    
    # Profitability assessment
    if 'net_margin' in analysis and analysis['net_margin'] is not None:
        net_margin = analysis['net_margin'].iloc[0]
        if net_margin > 15:
            insights.append("**Profitability Assessment**: Excellent profitability - company demonstrates strong pricing power")
        elif net_margin > 10:
            insights.append("**Profitability Assessment**: Good profitability - healthy business model")
        elif net_margin > 5:
            insights.append("**Profitability Assessment**: Moderate profitability - room for improvement")
        else:
            insights.append("**Profitability Assessment**: Low profitability - may indicate competitive pressures")
    
    # Growth assessment
    if 'revenue_growth' in analysis and len(analysis['revenue_growth']) > 1:
        avg_growth = analysis['revenue_growth'].mean()
        if avg_growth > 15:
            insights.append("**Growth Assessment**: High growth company - expanding rapidly")
        elif avg_growth > 8:
            insights.append("**Growth Assessment**: Steady growth - consistent business expansion")
        elif avg_growth > 0:
            insights.append("**Growth Assessment**: Moderate growth - stable business")
        else:
            insights.append("**Growth Assessment**: Declining revenue - business challenges evident")
    
    # Industry context
    sector = info.get('sector', 'Unknown')
    insights.append(f"**Industry**: {sector} sector company")
    
    market_cap = info.get('marketCap', 0)
    if market_cap > 0:
        market_cap_cr = market_cap / 1e7  # Convert to crores
        insights.append(f"**Market Capitalization**: ₹{market_cap_cr:.0f} crores")
    
    return insights

# Main application logic
if stock_symbol:
    with st.spinner(f"Fetching data for {stock_symbol}..."):
        stock, info, financials, quarterly_financials = get_stock_info(stock_symbol)
    
    if stock and info:
        company_name = info.get('longName', stock_symbol)
        st.header(f"📊 PnL Analysis for {company_name}")
        
        # Company overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"₹{info.get('currentPrice', 'N/A')}")
        with col2:
            st.metric("Market Cap", f"₹{info.get('marketCap', 0)/1e7:.0f} Cr" if info.get('marketCap') else "N/A")
        with col3:
            st.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
        
        # Analyze financials
        if financials is not None and not financials.empty:
            analysis = analyze_pnl_trends(financials)
            
            if analysis:
                # Create visualizations
                st.subheader("📈 Visual Analysis")
                create_pnl_visualizations(analysis, company_name)
                
                # Generate insights
                st.subheader("🔍 Key Insights")
                insights = generate_pnl_insights(analysis, info)
                
                for insight in insights:
                    st.markdown(f"• {insight}")
                
                # Financial data table
                st.subheader("📋 Financial Data Summary (₹ Crores)")
                
                if 'revenue' in analysis:
                    financial_summary = pd.DataFrame({
                        'Year': analysis['revenue'].index.year,
                        'Revenue': (analysis['revenue'].values / 1e7).round(2),
                        'Gross Profit': (analysis.get('gross_profit', pd.Series([0]*len(analysis['revenue']))).values / 1e7).round(2) if 'gross_profit' in analysis else 'N/A',
                        'Operating Income': (analysis.get('operating_income', pd.Series([0]*len(analysis['revenue']))).values / 1e7).round(2) if 'operating_income' in analysis else 'N/A',
                        'Net Income': (analysis.get('net_income', pd.Series([0]*len(analysis['revenue']))).values / 1e7).round(2) if 'net_income' in analysis else 'N/A'
                    })
                    
                    st.dataframe(financial_summary, use_container_width=True)
            else:
                st.warning("Unable to analyze financial data - insufficient information available")
        else:
            st.warning(f"No financial data available for {company_name}. This might be due to:")
            st.markdown("• Company not listed on NSE/BSE")
            st.markdown("• Incorrect stock symbol")
            st.markdown("• Recent listing with limited financial history")
    else:
        st.error("Unable to fetch stock data. Please check the stock symbol and try again.")

else:
    st.info("👆 Please enter a stock symbol or select from popular stocks to begin analysis")
    st.markdown("### How to use:")
    st.markdown("• Enter Indian stock symbols with .NS (NSE) or .BO (BSE) suffix")
    st.markdown("• Examples: RELIANCE.NS, TCS.NS, INFY.NS")
    st.markdown("• Or select from the popular stocks in the sidebar")
    
    st.markdown("### Features:")
    st.markdown("• Comprehensive PnL statement analysis")
    st.markdown("• Visual representation of financial trends")
    st.markdown("• Key financial metrics and ratios")
    st.markdown("• Growth and profitability insights")
    st.markdown("• Industry context and comparisons")

# Footer
st.markdown("---")
st.markdown("**Disclaimer**: This analysis is for informational purposes only and should not be considered as investment advice.")
