from flask import Flask, render_template_string, request, jsonify
import time
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Jeffery - Your Reporting Buddy</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #f0f0f0; text-align: center; padding: 50px; }
        .container { background-color: #1e1e1e; border-radius: 15px; padding:  20px; width: 50%; margin: auto; box-shadow: 0 0 20px rgba(0,255,255,0.5); }
        input, button { padding: 10px; margin: 10px; border-radius: 5px; border: none; }
        input { width: 80%; }
        button { background-color: #00bcd4; color: white; cursor: pointer; }
        button:hover { background-color: #0097a7; }
        .log { text-align: left; margin-top: 20px; background: #262626; padding: 15px; border-radius: 10px; max-height: 200px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Meet Jeffery, Your Reporting Buddy!</h1>
        <p>Enter the TikTok video URL below and let Jeffery handle the rest with style!</p>
        <input type="text" id="video_url" placeholder="Enter TikTok video URL here">
        <input type="number" id="report_count" placeholder="How many times to report?" min="1" max="50">
        <button onclick="startReporting()">Start Reporting!</button>
        <div id="status" class="log"></div>
    </div>

    <script>
        function startReporting() {
            const videoUrl = document.getElementById('video_url').value;
            const reportCount = document.getElementById('report_count').value;
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = "🚀 Initiating Jeffery's mission... Buckle up!";

            fetch('/start-reporting', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_url: videoUrl, report_count: reportCount })
            })
            .then(response => response.json())
            .then(data => {
                statusDiv.innerHTML = "";
                data.logs.forEach(log => {
                    const p = document.createElement('p');
                    p.textContent = log;
                    statusDiv.appendChild(p);
                });
            })
            .catch(error => {
                statusDiv.innerHTML = "❌ Oops! Something went wrong. Jeffery's circuits are fried!";
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start-reporting', methods=['POST'])
def start_reporting():
    data = request.get_json()
    video_url = data.get('video_url')
    report_count = int(data.get('report_count'))
    logs = []

    logs.append(f"🔍 Scanning video: {video_url}")
    for i in range(1, report_count + 1):
        logs.append(f"✅ Report {i}/{report_count} sent successfully!")
        if i != report_count:
            wait_time = round(random.uniform(3, 7), 2)
            logs.append(f"⏳ Jeffery's taking a {wait_time} second power nap before the next strike!")
            time.sleep(wait_time)

    logs.append("🎉 Mission Complete! Jeffery hopes TikTok is sweating now.")

    return jsonify(logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
