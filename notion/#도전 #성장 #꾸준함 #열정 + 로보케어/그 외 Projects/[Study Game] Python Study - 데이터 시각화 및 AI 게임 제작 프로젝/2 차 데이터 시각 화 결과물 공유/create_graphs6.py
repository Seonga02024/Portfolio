
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define file paths using forward slashes for compatibility
csv_path = "video-game-sales/versions/1/vgsales.csv"
desktop_path = "C:/Users/Desktop"
platform_graph_path = os.path.join(desktop_path, "platform_sales_heatmap_final_v2.png")
genre_graph_path = os.path.join(desktop_path, "genre_popularity_heatmap_final_v2.png")

# Set Korean font for matplotlib
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

try:
    df = pd.read_csv(csv_path)
    
    # Data Cleaning
    df.dropna(subset=['Year', 'Platform', 'Genre', 'Global_Sales'], inplace=True)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df.dropna(subset=['Year'], inplace=True)
    df['Year'] = df['Year'].astype(int)
    df = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]

    # --- Graph 1: Platform Heatmap ---
    top_platforms = df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
    df_top_platforms = df[df['Platform'].isin(top_platforms)]
    platform_pivot = df_top_platforms.pivot_table(index='Platform', columns='Year', values='Global_Sales', aggfunc='sum').fillna(0)
    
    plt.figure(figsize=(18, 8))
    ax1 = sns.heatmap(platform_pivot, cmap="Blues", annot=False)
    ax1.set_title("연도에 따른 비디오 플랫폼 인기 변화", pad=20, fontsize=16)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Platform', fontsize=12)

    # Find and highlight the max value
    max_val = platform_pivot.max().max()
    max_loc = platform_pivot.where(platform_pivot == max_val).stack().index.tolist()[0]
    max_row_idx = platform_pivot.index.get_loc(max_loc[0])
    max_col_idx = platform_pivot.columns.get_loc(max_loc[1])
    ax1.add_patch(plt.Rectangle((max_col_idx, max_row_idx), 1, 1, fill=False, edgecolor='red', lw=3))

    plt.savefig(platform_graph_path)
    print(f"Platform heatmap saved to {platform_graph_path}")
    plt.clf()

    # --- Graph 2: Genre Heatmap ---
    genre_pivot = df.pivot_table(index='Genre', columns='Year', values='Global_Sales', aggfunc='sum').fillna(0)

    plt.figure(figsize=(18, 8))
    ax2 = sns.heatmap(genre_pivot, cmap="Greens", annot=False)
    ax2.set_title("연도에 따른 비디오 게임 장르 인기 변화", pad=20, fontsize=16)
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Genre', fontsize=12)

    # Find and highlight the max value
    max_val_genre = genre_pivot.max().max()
    max_loc_genre = genre_pivot.where(genre_pivot == max_val_genre).stack().index.tolist()[0]
    max_row_idx_genre = genre_pivot.index.get_loc(max_loc_genre[0])
    max_col_idx_genre = genre_pivot.columns.get_loc(max_loc_genre[1])
    ax2.add_patch(plt.Rectangle((max_col_idx_genre, max_row_idx_genre), 1, 1, fill=False, edgecolor='red', lw=3))

    plt.savefig(genre_graph_path)
    print(f"Genre heatmap saved to {genre_graph_path}")

except FileNotFoundError:
    print(f"Error: The file was not found at {csv_path}")
except Exception as e:
    print(f"An error occurred: {e}")

