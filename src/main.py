from analyzer import StockAnalyzer

def format_fundamentals(fundamentals):
    if not fundamentals:
        return "Fundamental data not available"
        
    return "\n".join([
        f"P/E Ratio: {fundamentals['PE_Ratio']:.2f}",
        f"P/B Ratio: {fundamentals['PB_Ratio']:.2f}",
        f"Profit Margin: {fundamentals['Profit_Margin']:.2%}",
        f"ROE: {fundamentals['ROE']:.2%}",
        f"Revenue Growth: {fundamentals['Revenue_Growth']:.2%}",
        f"Analyst Rating (1-5): {fundamentals['Analyst_Rating']:.1f}",
        f"Target Price: ${fundamentals['Target_Price']:.2f}",
        f"Dividend Yield: {fundamentals['Dividend_Yield']:.2%}"
    ])

def main():
    ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    
    try:
        analyzer = StockAnalyzer(ticker)
        result = analyzer.get_recommendation()
        
        print(f"\nAnalysis for {result['ticker']}:")
        print(f"Overall Recommendation: {result['recommendation']}\n")
        
        print("Weekly Analysis:")
        print("Technical Signals:")
        for signal, reason in result['weekly_analysis']['signals']:
            print(f"- {signal}: {reason}")
        print("\nML Predictions:")
        print(f"- Upward Movement Probability: {result['weekly_analysis']['ml_prediction']['up_probability']:.0%}")
        print(f"- Downward Movement Probability: {result['weekly_analysis']['ml_prediction']['down_probability']:.0%}\n")
        
        print("Monthly Analysis:")
        print("Technical Signals:")
        for signal, reason in result['monthly_analysis']['signals']:
            print(f"- {signal}: {reason}")
        print("\nML Predictions:")
        print(f"- Upward Movement Probability: {result['monthly_analysis']['ml_prediction']['up_probability']:.0%}")
        print(f"- Downward Movement Probability: {result['monthly_analysis']['ml_prediction']['down_probability']:.0%}\n")
        
        print("Fundamental Analysis:")
        print(format_fundamentals(result['fundamentals']))
        
    except Exception as e:
        print(f"Error analyzing {ticker}: {str(e)}")

if __name__ == "__main__":
    main()