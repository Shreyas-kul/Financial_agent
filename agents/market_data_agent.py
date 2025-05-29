import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

class MarketDataAgent:
    def __init__(self):
        # List of major Asian tech stocks
        self.asia_tech_stocks = {
            '2330.TW': 'TSMC',
            '005930.KS': 'Samsung',
            '9984.T': 'SoftBank',
            '0700.HK': 'Tencent',
            '9988.HK': 'Alibaba',
            '3690.HK': 'Meituan',
            '035420.KS': 'NAVER',
            '035720.KS': 'Kakao'
        }
        
    def get_portfolio_exposure(self) -> Tuple[float, Dict[str, float]]:
        """Calculate portfolio exposure to Asian tech stocks"""
        total_market_cap = 0
        market_caps = {}
        
        for symbol, name in self.asia_tech_stocks.items():
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                market_cap = info.get('marketCap', 0)
                if market_cap:
                    market_caps[name] = market_cap
                    total_market_cap += market_cap
            except Exception as e:
                print(f"Error fetching data for {name}: {str(e)}")
                
        # Calculate percentages
        exposure = {name: (cap / total_market_cap) * 100 
                   for name, cap in market_caps.items()}
        
        return sum(exposure.values()), exposure

    def get_earnings_surprises(self) -> Dict[str, float]:
        """Get earnings surprises for Asian tech stocks"""
        surprises = {}
        
        for symbol, name in self.asia_tech_stocks.items():
            try:
                stock = yf.Ticker(symbol)
                earnings = stock.earnings_dates
                
                if not earnings.empty:
                    # Get most recent earnings
                    latest = earnings.iloc[0]
                    if 'Surprise(%)' in latest:
                        surprises[name] = latest['Surprise(%)']
            except Exception as e:
                print(f"Error fetching earnings for {name}: {str(e)}")
                
        return surprises

    def get_market_sentiment(self) -> Dict[str, Any]:
        """Analyze market sentiment for Asian tech sector"""
        sentiment_data = {
            'overall': 'neutral',
            'factors': []
        }
        
        try:
            # Get regional index data
            indices = {
                '^HSI': 'Hang Seng Tech',
                '^AXJO': 'ASX 200',
                '^N225': 'Nikkei 225'
            }
            
            for symbol, name in indices.items():
                index = yf.Ticker(symbol)
                hist = index.history(period='5d')
                
                if not hist.empty:
                    change = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100
                    sentiment_data['factors'].append({
                        'index': name,
                        'change': change,
                        'trend': 'up' if change > 0 else 'down'
                    })
            
            # Get yield data
            treasury = yf.Ticker('^TNX')
            hist = treasury.history(period='5d')
            if not hist.empty:
                yield_change = hist['Close'][-1] - hist['Close'][0]
                sentiment_data['factors'].append({
                    'factor': 'US 10Y Yield',
                    'change': yield_change,
                    'impact': 'cautionary' if yield_change > 0 else 'supportive'
                })
                
            # Determine overall sentiment
            positive_factors = sum(1 for f in sentiment_data['factors'] 
                                if f.get('trend') == 'up' or f.get('impact') == 'supportive')
            total_factors = len(sentiment_data['factors'])
            
            if positive_factors / total_factors > 0.6:
                sentiment_data['overall'] = 'positive'
            elif positive_factors / total_factors < 0.4:
                sentiment_data['overall'] = 'negative'
            else:
                sentiment_data['overall'] = 'neutral'
                
        except Exception as e:
            print(f"Error analyzing market sentiment: {str(e)}")
            sentiment_data['overall'] = 'neutral'
            sentiment_data['error'] = str(e)
            
        return sentiment_data 