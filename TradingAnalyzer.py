import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def show_market_trend(symbol,timeframe,bars,plot=False,print=False,show_std_plot=False):
    """
    This is a MetaTrader5 function that shows the trend or direction or condition of the market.

    Input:
    symbol: market symbol from your broker
    timeframe: MetaTrader5_TIMEFRAME_<give your timeframe>
    bars: number of bars to look for
    plot: if you want to plot the trend
    print: if you want to print the trend
    show_std_plot: if you want to plot the standard deviation
    
    OutPut:
    returns one of the the following condition:
    1. Strong Upward
    2. Strong Downward
    3. Moderate Upward
    4. Moderate Downward
    5. Weak Upward
    6. Weak Downward
    7. Neutral
    9. Sideways
    10. Indecisive
  
    """
    

    symbol = symbol
    timeframe = timeframe
    # bars to look for
    bars = bars
    # Get the current datetime in UTC timezone
    last_bar = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
    server_time = last_bar[0]['time']
    utc_now = pd.to_datetime(server_time, unit='s', utc=True)

    # Get the last 100 bars from the MetaTrader 5 terminal
    rates = mt5.copy_rates_from(symbol, timeframe, utc_now, bars)

    # Convert the data to a pandas dataframe
    df = pd.DataFrame(rates)

    # Drop the time and real volume columns
    df.drop(['time', 'real_volume'], axis=1, inplace=True)

    # Define a function to calculate the trend direction based on the slope of a linear regression line
    def trend_direction(data): 
        # Calculate the slope of the linear regression line for the given window
        slope = np.polyfit(np.arange(len(data)), data, 1)[0]
        
        # Return the trend direction based on the slope value
        if slope > 0.001:
            return "Upward"
        elif slope < -0.001:
            return "Downward"
        else:
            return "Sideways"

    # Define a function to calculate the trend strength based on the standard deviation of the residuals
    def trend_strength(data): 
        # Calculate the linear regression line
        line = np.polyfit(np.arange(len(data)), data, 1)
        
        # Calculate the residuals (the difference between the actual values and the predicted values)
        residuals = data - (line[0] * np.arange(len(data)) + line[1])
        
        # Calculate the standard deviation of the residuals
        std = np.std(residuals)
        
        # Return the trend strength based on the standard deviation value
        if std < 0.01:
            return "Strong"
        elif std < 0.05:
            return "Moderate"
        else:
            return "Weak"

    # Define a function to calculate the trend type based on the trend direction and strength
    def trend_type(direction, strength): 
        # Return the trend type based on the direction and strength values
        if direction == "Upward" and strength == "Strong":
            return "Strong Bullish"
        elif direction == "Downward" and strength == "Strong":
            return "Strong Bearish"
        elif direction == "Upward" and strength == "Moderate":
            return "Moderate Bullish"
        elif direction == "Downward" and strength == "Moderate":
            return "Moderate Bearish"
        elif direction == "Upward" and strength == "Weak":
            return "Weak Bullish"
        elif direction == "Downward" and strength == "Weak":
            return "Weak Bearish"
        elif direction == "Sideways" and strength == "Weak":
            return "Indecisive"
        else:
            return "Neutral"

    # Calculate the trend direction, strength, and type for the close prices
    df['trend_direction'] = trend_direction(df['close']) 
    df['trend_strength'] = trend_strength(df['close']) 
    df['trend_type'] = df.apply(lambda row: trend_type(row['trend_direction'], row['trend_strength']), axis=1)

    # Get the last trend type
    last_trend = df['trend_type'].iloc[-1]

    if print == True:
        # Print the result
        print(f"The market trend for {symbol} on {timeframe} is ====>{last_trend}<===")


    if plot == True:
        # Plot the close prices and the trend types
        plt.figure(figsize=(15, 10)) 
        plt.plot(df['close'], label='Close Price') 
        plt.scatter(df.index, df['close'], c=df['trend_type'].map({
        'Bullish': '#00FF00',
        'Bearish': '#FF0000',
        'Indecisive': '#FFFF00',
        'Neutral': '#0000FF',
        'Strong Bullish': '#006400',  # Dark Green
        'Strong Bearish': '#8B0000',  # Dark Red
        'Moderate Bullish': '#00FF00',  # Light Green
        'Moderate Bearish': '#FF0000',  # Light Red
        'Weak Bullish': '#006400',  # Dark Green
        'Weak Bearish': '#8B0000'  # Dark Red
                                                                    }),

                                                                    label='Trend Type') 
        plt.title(f"Market Trend for {symbol} on {timeframe}: {last_trend}") 
        plt.xlabel('Bar Index') 
        plt.ylabel('Price') 
        plt.legend() 
        plt.show()


    if show_std_plot == True:
        # -------------------temp -------------------------

        
        # Calculate the linear regression
        line = np.polyfit(np.arange(len(df['close'])), df['close'], 1)

        # Calculate the residuals
        residuals = df['close'] - (line[0] * np.arange(len(df['close'])) + line[1])

        # Plot the data, linear regression line, and residuals
        plt.figure(figsize=(15, 10))

        # Plot the data
        plt.scatter(np.arange(len(df['close'])), df['close'], label='Actual Data')

        # Plot the linear regression line
        plt.plot(np.arange(len(df['close'])), line[0] * np.arange(len(df['close'])) + line[1], color='red', label='Linear Regression Line')

        # Plot the residuals
        plt.bar(np.arange(len(df['close'])), residuals, color='gray', alpha=0.5, label='Residuals')

        plt.title(f"Linear Regression and Residuals for {symbol} on {timeframe}")
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()
        plt.show()


    

        # Calculate the standard deviation of residuals
        residuals_std = np.std(residuals)

        # Plot the data, linear regression line, residuals, and a distribution plot with standard deviation lines
        plt.figure(figsize=(15, 12))

        # Plot the data
        plt.subplot(2, 1, 1)
        plt.scatter(np.arange(len(df['close'])), df['close'], label='Actual Data')
        plt.plot(np.arange(len(df['close'])), line[0] * np.arange(len(df['close'])) + line[1], color='red', label='Linear Regression Line')
        plt.errorbar(np.arange(len(df['close'])), df['close'], yerr=residuals_std, fmt='none', color='gray', ecolor='gray', capsize=2, label='Residuals (Std Dev)')
        plt.title(f"Linear Regression, Residuals, and Std Dev for {symbol} on {timeframe}")
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()

        # Plot the distribution of residuals
        plt.subplot(2, 1, 2)
        plt.hist(residuals, bins=20, color='gray', edgecolor='black', alpha=0.7, label='Residuals Distribution')
        plt.axvline(np.mean(residuals), color='red', linestyle='dashed', linewidth=2, label='Mean')
        plt.axvline(np.mean(residuals) + residuals_std, color='blue', linestyle='dashed', linewidth=2, label='Mean + 1 Std Dev')
        plt.axvline(np.mean(residuals) - residuals_std, color='blue', linestyle='dashed', linewidth=2, label='Mean - 1 Std Dev')
        plt.title("Distribution of Residuals")
        plt.xlabel('Residuals')
        plt.ylabel('Frequency')
        plt.legend()

        plt.tight_layout()
        plt.show()

    return last_trend