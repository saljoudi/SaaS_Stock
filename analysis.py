from flask import Blueprint, render_template, request, flash
from yahooquery import Ticker
import pandas as pd
import plotly.graph_objs as go

analysis_bp = Blueprint('analysis', __name__)

def get_stock_data(ticker, period='1d', interval='1m'):
    ticker_obj = Ticker(ticker)
    df = ticker_obj.history(period=period, interval=interval).reset_index()
    return df

@analysis_bp.route('/analysis', methods=['GET', 'POST'])
def analysis():
    # Default parameters
    ticker = 'AAPL'
    period = '1d'
    interval = '1m'
    
    if request.method == 'POST':
        # Retrieve parameters from a form if you build one
        ticker = request.form.get('ticker', ticker)
        period = request.form.get('period', period)
        interval = request.form.get('interval', interval)
    
    df = get_stock_data(ticker, period, interval)
    if df.empty:
        flash(f"No data found for {ticker} over the last {period} with interval {interval}.")
        graph_html = "<p>No data available.</p>"
    else:
        # Process data: ensure date column is datetime and set as index
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Create a basic price chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Close Price'))
        fig.update_layout(
            title=f"{ticker} Stock Price",
            xaxis_title="Date/Time",
            yaxis_title="Price",
            template="plotly_white"
        )
        # Render the figure as HTML
        graph_html = fig.to_html(full_html=False)
    
    return render_template('analysis.html', graph_html=graph_html)
