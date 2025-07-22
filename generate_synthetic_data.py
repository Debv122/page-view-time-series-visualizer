import pandas as pd
import numpy as np

def generate_synthetic_pageviews(start_date, end_date, seed=42):
    np.random.seed(seed)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    n = len(dates)
    # Simulate a base trend (slight growth over time)
    base = np.linspace(1200, 2500, n)
    # Add seasonality (higher on weekends)
    seasonality = 200 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    # Add weekly pattern (higher on weekends)
    weekly = np.where(dates.weekday >= 5, 300, 0)
    # Add random noise
    noise = np.random.normal(0, 80, n)
    values = base + seasonality + weekly + noise
    values = np.round(values).astype(int)
    df = pd.DataFrame({'date': dates, 'value': values})
    return df

if __name__ == '__main__':
    df = generate_synthetic_pageviews('2016-05-09', '2019-12-03')
    df.to_csv('fcc-forum-pageviews.csv', index=False)
    print('Synthetic data saved to fcc-forum-pageviews.csv') 