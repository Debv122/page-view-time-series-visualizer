import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_and_clean_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'], index_col='date')
    # Clean data: remove top and bottom 2.5%
    lower = df['value'].quantile(0.025)
    upper = df['value'].quantile(0.975)
    df_clean = df[(df['value'] >= lower) & (df['value'] <= upper)]
    return df_clean

# Line plot
def draw_line_plot(df):
    df_line = df.copy()
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.tight_layout()
    fig.savefig('line_plot.png')
    return fig

# Bar plot
def draw_bar_plot(df):
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    # Group by year and month, then calculate mean
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    # Ensure months are in calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped = df_grouped[month_order]
    ax = df_grouped.plot(kind='bar', figsize=(15, 8))
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    # Add data labels
    for p in ax.patches:
        height = p.get_height()
        if not pd.isna(height):
            ax.annotate(f'{int(height)}',
                        (p.get_x() + p.get_width() / 2, height),
                        ha='center', va='bottom', fontsize=8, rotation=90)
    plt.savefig('bar_plot.png')
    return ax.get_figure()

# Box plot
def draw_box_plot(df):
    df_box = df.copy().reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    # Sort months for correct order
    df_box = df_box.sort_values('month_num')
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    # Annotate medians
    for i, year in enumerate(sorted(df_box['year'].unique())):
        median = df_box[df_box['year'] == year]['value'].median()
        axes[0].annotate(f'{int(median)}', (i, median), ha='center', va='bottom', fontsize=8, color='black')
    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    # Annotate medians
    for i, month in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']):
        median = df_box[df_box['month'] == month]['value'].median()
        axes[1].annotate(f'{int(median)}', (i, median), ha='center', va='bottom', fontsize=8, color='black')
    plt.tight_layout()
    fig.savefig('box_plot.png')
    return fig

# Example usage (to be removed or modified as needed)
# df = load_and_clean_data('fcc-forum-pageviews.csv')
# draw_line_plot(df)
# draw_bar_plot(df)
# draw_box_plot(df) 