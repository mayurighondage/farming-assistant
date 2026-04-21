from flask import Flask, render_template_string, request
from PIL import Image
import os
import random

app = Flask(__name__)

# ================= SHARED UI COMPONENTS =================
STYLE = """
<style>
    body { margin:0; font-family: 'Segoe UI', Arial, sans-serif; background: #e8f5e9; text-align:center; color: #333; }
    header { background:#2e7d32; color:white; padding:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    nav { background:#1b5e20; padding:12px; text-align:center; position: sticky; top: 0; z-index: 1000; }
    nav a { color:white; margin:0 15px; text-decoration:none; font-weight:bold; transition: 0.3s; }
    nav a:hover { color:yellow; border-bottom: 2px solid yellow; }
    .container { padding:50px 20px; min-height: 70vh; }
    .card { background: white; padding: 30px; display: inline-block; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 400px; width: 100%; }
    input, select { margin: 10px 0; padding: 12px; width: 90%; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
    button { width: 95%; padding: 12px; background: #2e7d32; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 16px; margin-top: 10px; }
    button:hover { background: #1b5e20; }
    .result-box { margin-top: 25px; padding: 15px; border-radius: 8px; background: #f1f8e9; border: 1px dashed #2e7d32; }
    footer { background:#2e7d32; color:white; padding:15px; font-size: 0.9em; margin-top: 40px; }
</style>
"""

NAV_HTML = """
<nav>
    <a href="/">Home</a>
    <a href="/crop">Crop</a>
    <a href="/disease">Disease</a>
    <a href="/fertilizer">Fertilizer</a>
    <a href="/ph">pH</a>
</nav>
"""

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy classes for testing
CLASSES = ['Healthy', 'Early_Blight', 'Late_Blight']

# ================= ROUTES =================
@app.route('/')
def home():
    return render_template_string(f"""
    {STYLE}
    <header><h1>🌱 FarmAssist</h1><p>Smart Farming Solutions</p></header>
    {NAV_HTML}
    <div class="container">
        <div class="card">
            <h2>Welcome Farmer 👨‍🌾</h2>
            <p>Your digital partner for crop health, soil analysis, and nutrient management.</p>
            <p>Select a tool from the menu above to begin.</p>
        </div>
    </div>
    <footer>© 2026 FarmAssist | Empowering Agriculture</footer>
    """)

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    result = ""
    if request.method == 'POST':
        temp = float(request.form.get('temp', 0))
        hum = float(request.form.get('hum', 0))
        if temp > 30 and hum > 70: result = "Recommended Crop: Rice 🌾"
        elif temp < 25: result = "Recommended Crop: Wheat 🌱"
        else: result = "Recommended Crop: Maize 🌽"
    return render_template_string(f"""
    {STYLE}
    <header><h1>🌿 Crop Prediction</h1></header>
    {NAV_HTML}
    <div class="container">
        <div class="card">
            <form method="POST">
                <input name="temp" type="number" step="any" placeholder="Temperature (°C)" required>
                <input name="hum" type="number" step="any" placeholder="Humidity (%)" required>
                <button type="submit">Recommend Crop</button>
            </form>
            {f'<div class="result-box"><h2 style="color:#2e7d32;">{result}</h2></div>' if result else ''}
        </div>
    </div>
    """)

@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    res = ""
    if request.method == 'POST':
        n = float(request.form.get('n', 0))
        p = float(request.form.get('p', 0))
        k = float(request.form.get('k', 0))
        if n < 40: res = "Low Nitrogen: Apply Urea."
        elif p < 40: res = "Low Phosphorous: Apply DAP."
        elif k < 40: res = "Low Potassium: Apply MOP."
        else: res = "Nutrients Balanced: Use Organic Compost."
    return render_template_string(f"""
    {STYLE}
    <header><h1>🌱 Fertilizer Advisor</h1></header>
    {NAV_HTML}
    <div class="container">
        <div class="card">
            <form method="POST">
                <input name="n" type="number" placeholder="Nitrogen (N)" required>
                <input name="p" type="number" placeholder="Phosphorous (P)" required>
                <input name="k" type="number" placeholder="Potassium (K)" required>
                <button type="submit">Check Fertilizer</button>
            </form>
            {f'<div class="result-box"><h2 style="color:#2e7d32;">{res}</h2></div>' if res else ''}
        </div>
    </div>
    """)

@app.route('/disease', methods=['GET', 'POST'])
def disease():
    res = ""
    img_path = ""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(img_path)

            # Open the image (for model later)
            img = Image.open(img_path).convert('RGB')

            # Dummy prediction for testing
            prediction = random.choice(CLASSES)
            res = f"Detected Disease: {prediction}"

    return render_template_string(f"""
    {STYLE}
    <header><h1>🦠 Disease Detection</h1></header>
    {NAV_HTML}
    <div class="container">
        <div class="card">
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Upload & Detect</button>
            </form>
            {f'<img src="/{img_path}" width="200">' if img_path else ''}
            {f'<div class="result-box"><h2>{res}</h2></div>' if res else ''}
        </div>
    </div>
    """)

@app.route('/ph', methods=['GET', 'POST'])
def ph_test():
    res = ""
    if request.method == 'POST':
        val = float(request.form.get('ph_val', 7))
        if val < 6.0: res = "Soil is Acidic: Add Lime."
        elif val > 7.5: res = "Soil is Alkaline: Add Sulfur."
        else: res = "Soil is Neutral: Optimal!"
    return render_template_string(f"""
    {STYLE}
    <header><h1>🧪 pH Analysis</h1></header>
    {NAV_HTML}
    <div class="container">
        <div class="card">
            <form method="POST">
                <input name="ph_val" type="number" step="0.1" placeholder="Enter pH Value (0-14)" required>
                <button type="submit">Check Soil Type</button>
            </form>
            {f'<div class="result-box"><h2 style="color:#1976d2;">{res}</h2></div>' if res else ''}
        </div>
    </div>
    """)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 