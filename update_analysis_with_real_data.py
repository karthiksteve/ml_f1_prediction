"""Extract real results from HTML and update analysis page"""
import re
from bs4 import BeautifulSoup

# Read the original HTML to extract real data
with open('ML_FINAL.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all prediction results
patterns = {
    'model1': {
        'title': 'XG BOOST MODEL',
        'search': r'Charles Leclerc.*?Ferrari.*?85\.419'
    }
}

# Extract podium predictions
podium_pattern = r'🥇 P1: ([^(]+) \(([^)]+)\) \((\d+\.\d+) s\)\s*🥈 P2: ([^(]+) \(([^)]+)\) \((\d+\.\d+) s\)\s*🥉 P3: ([^(]+) \(([^)]+)\) \((\d+\.\d+) s\)'
podium_matches = re.findall(podium_pattern, html_content)

# Extract metrics
metrics_pattern = r'Mean Absolute Error \(MAE\): ([\d.]+) seconds.*?Root Mean Squared Error \(RMSE\): ([\d.]+) seconds.*?R-squared \(R2\) Score: ([-\d.]+)'
metrics_matches = re.findall(metrics_pattern, html_content, re.DOTALL)

print("Found", len(podium_matches), "podium predictions")
print("Found", len(metrics_matches), "metric sets")

for i, podium in enumerate(podium_matches[:3], 1):
    print(f"\nModel {i} Podium:")
    print(f"  P1: {podium[0].strip()} ({podium[1]}) {podium[2]}s")
    print(f"  P2: {podium[3].strip()} ({podium[4]}) {podium[5]}s")
    print(f"  P3: {podium[6].strip()} ({podium[7]}) {podium[8]}s")

for i, metrics in enumerate(metrics_matches[:3], 1):
    print(f"\nModel {i} Metrics:")
    print(f"  MAE: {metrics[0]}s")
    print(f"  RMSE: {metrics[1]}s")
    print(f"  R²: {metrics[2]}")

