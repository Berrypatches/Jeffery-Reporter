from flask import Flask, render_template_string, request, Response
import time
import threading

app = Flask(__name__)

# HTML template with SSE support
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeffery - The Reporting Assistant</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #121212; color: #e0e0e0; text-align: center; padding: 50px; }
        h1 { color: #00e676; }
        form { margin: 20px 0; }
        input, button { padding: 10px; margin: 5px; border-radius: 5px; border: none; }
        input { width: 300px; }
        button { background-color: #00e676; color: #121212; cursor: pointer; }
        button:hover { background-color: #00c853; }
        #output { margin-top: 30px; padding: 20px; background-color: #1e1e1e; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>Welcome to Jeffery 😎</h1>
    <p>Your playful, over-the-top reporting assistant!</p>
    <form id="report-form">
        <input type="text" id="url" placeholder="Enter TikTok video URL" required><br>
        <input type="number" id="times" placeholder="Number of reports" min="1" required><br>
        <button type="submit">Submit</button>
    </form>
    <div id="output"></div>

    <script>
        document.getElementById('report-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const url = document.getElementById('url').value;
            const times = document.getElementById('times').value;
            document.getElementById('output').innerHTML = 'Jeffery is on it... 💼<br><br>';

            const eventSource = new EventSource(`/stream?url=${encodeURIComponent(url)}&times=${times}`);
            eventSource.onmessage = function(event) {
                if (event.data === "[DONE]") {
                    eventSource.close();
                    document.getElementById('output').innerHTML += '<br>🎯 All done! Jeffery out. 🕶️';
                } else {
                    document.getElementById('output').innerHTML += event.data + '<br>';
                }
            };
        });
    </script>
</body>
</html>
"""

def report_video(url, times, output):
    for i in range(1, times + 1):
        output.append(f"✅ Report {i}/{times} sent successfully!")
        delay = round(3 + (2 * time.perf_counter()) % 5, 2)
        output.append(f"⏳ Waiting {delay} seconds before the next report...")
        time.sleep(delay)
    output.append("[DONE]")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/stream')
def stream():
    url = request.args.get('url')
    times = int(request.args.get('times'))
    output = []

    thread = threading.Thread(target=report_video, args=(url, times, output))
    thread.start()

    def generate():
        last_index = 0
        while True:
            if last_index < len(output):
                for line in output[last_index:]:
                    yield f"data: {line}\n\n"
                    if line == "[DONE]":
                        return
                last_index = len(output)
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
