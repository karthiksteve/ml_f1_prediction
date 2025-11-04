"""
Python script to convert Jupyter notebook to HTML with custom styling options
Run this script to generate different versions of HTML output from your notebook
"""

import subprocess
import os

# Get the notebook filename
notebook_file = "ML_FINAL.ipynb"

print("Converting notebook to HTML...")
print("=" * 50)

# Option 1: Basic HTML (already done with nbconvert command)
print("\n✅ Basic HTML conversion completed!")
print(f"   Output: {notebook_file.replace('.ipynb', '.html')}")

# Option 2: Self-contained HTML (embeds all outputs and images inline)
print("\n📦 Creating self-contained HTML (all outputs embedded)...")
subprocess.run([
    "jupyter", "nbconvert",
    "--to", "html",
    notebook_file,
    "--output", "ML_FINAL_standalone.html",
    "--embed-images",
    "--no-input"  # Optional: hide code cells, show only outputs
])

print("\n✅ Self-contained HTML created!")

# Option 3: HTML with custom template (if you want more control)
print("\n🎨 Creating styled HTML version...")
subprocess.run([
    "jupyter", "nbconvert",
    "--to", "html",
    notebook_file,
    "--output", "ML_FINAL_styled.html",
    "--template", "classic"  # Can also use 'basic' or custom templates
])

print("\n✅ Styled HTML created!")

# Option 4: HTML without code cells (execution results only)
print("\n📊 Creating HTML with outputs only (no code cells)...")
subprocess.run([
    "jupyter", "nbconvert",
    "--to", "html",
    notebook_file,
    "--output", "ML_FINAL_output_only.html",
    "--no-input"
])

print("\n✅ Output-only HTML created!")

print("\n" + "=" * 50)
print("\n📝 Summary of generated HTML files:")
print("   • ML_FINAL.html - Basic HTML conversion")
print("   • ML_FINAL_standalone.html - Self-contained (all images embedded)")
print("   • ML_FINAL_styled.html - Styled version")
print("   • ML_FINAL_output_only.html - Results only (no code)")
print("\n💡 Tip: Open any .html file in your web browser to view!")

