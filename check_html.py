"""Quick script to analyze HTML file structure"""
with open('ML_FINAL.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
print("HTML File Analysis:")
print("=" * 50)
print(f"Total file size: {len(content):,} bytes ({len(content)/1024:.1f} KB)")
print(f"Code cells: {content.count('class=\"cell')}")
print(f"Output sections: {content.count('class=\"output')}")
print(f"Images (<img tags): {content.count('<img')}")
print(f"Tables: {content.count('<table')}")
print(f"Contains 'Predicted': {content.count('Predicted')}")
print(f"Contains podium emojis (🥇): {content.count('🥇')}")
print(f"Contains matplotlib images: {'image/png' in content or 'data:image' in content}")
print("\n✅ HTML file is ready to view!")

