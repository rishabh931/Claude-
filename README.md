# Indian Stock PnL Analyzer 📈

A comprehensive Streamlit web application for analyzing Profit & Loss statements of Indian stocks with visual representations and detailed insights.

## Features

- **Stock Search**: Enter any Indian stock symbol or name for analysis
- **Comprehensive PnL Analysis**: Revenue, gross profit, operating income, and net income trends
- **Visual Representations**: Interactive charts and graphs using Plotly
- **Key Insights**: Automated bullet-point analysis of financial performance
- **Popular Stocks**: Quick access to major Indian companies
- **Financial Metrics**: Margins, growth rates, and profitability ratios

## Supported Stocks

The application works with all Indian stocks listed on:
- **NSE (National Stock Exchange)**: Use `.NS` suffix (e.g., `RELIANCE.NS`)
- **BSE (Bombay Stock Exchange)**: Use `.BO` suffix (e.g., `RELIANCE.BO`)

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/indian-stock-pnl-analyzer.git
   cd indian-stock-pnl-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

### Deployment on Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Connect your GitHub account** and select this repository

4. **Deploy** - Streamlit Cloud will automatically install dependencies and deploy your app

5. **Share** your app URL with others!

## How to Use

1. **Enter Stock Symbol**: Input any Indian stock symbol (e.g., `TCS.NS`, `RELIANCE.NS`)
2. **Or Select Popular Stocks**: Choose from pre-loaded popular Indian companies
3. **View Analysis**: Get comprehensive PnL analysis with:
   - Revenue trends and growth rates
   - Profit margins (Gross, Operating, Net)
   - Visual charts and graphs
   - Key financial insights
   - Performance assessment

## Sample Stock Symbols

| Company | NSE Symbol | BSE Symbol |
|---------|------------|------------|
| Reliance Industries | `RELIANCE.NS` | `RELIANCE.BO` |
| Tata Consultancy Services | `TCS.NS` | `TCS.BO` |
| Infosys | `INFY.NS` | `INFY.BO` |
| HDFC Bank | `HDFCBANK.NS` | `HDFCBANK.BO` |
| ICICI Bank | `ICICIBANK.NS` | `ICICIBANK.BO` |

## Technology Stack

- **Frontend**: Streamlit
- **Data Source**: Yahoo Finance (yfinance)
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud

## File Structure

```
indian-stock-pnl-analyzer/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## Features Explained

### PnL Analysis Components

1. **Revenue Analysis**
   - Total revenue trends over years
   - Year-over-year growth rates
   - Revenue growth visualization

2. **Profitability Metrics**
   - Gross Profit Margin
   - Operating Profit Margin  
   - Net Profit Margin
   - Trend analysis and comparisons

3. **Visual Representations**
   - Interactive bar charts for revenue
   - Line charts for margin trends
   - Growth rate visualizations
   - Comparative profit analysis

4. **Key Insights Generation**
   - Automated analysis of financial health
   - Growth assessment
   - Profitability evaluation
   - Industry context
   - Investment perspective

### Data Sources

The application uses Yahoo Finance API through the `yfinance` library to fetch:
- Historical financial data
- Annual and quarterly financials
- Stock price information
- Company information and metrics

## Limitations

- Data availability depends on Yahoo Finance
- Some companies may have limited financial history
- Real-time data may have slight delays
- Analysis is based on publicly available financial statements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Disclaimer

This application is for educational and informational purposes only. The financial analysis and insights provided should not be considered as investment advice. Always consult with qualified financial advisors before making investment decisions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have suggestions for improvements, please:
1. Check existing [Issues](https://github.com/your-username/indian-stock-pnl-analyzer/issues)
2. Create a new issue with detailed description
3. Contact the maintainer

---

**Made with ❤️ for Indian Stock Market Analysis**
