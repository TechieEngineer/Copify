from flask import Flask, request, render_template_string

app = Flask(__name__)

# In-memory storage for the shared text
shared_data = {"text": ""}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Clipboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; background: #f5f5f7; }
        textarea { width: 100%; height: 250px; padding: 12px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 8px; font-size: 16px; resize: vertical; }
        button { background: #0071e3; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; margin-top: 10px; width: 100%; }
        button:hover { background: #0077ed; }
        .status { color: green; font-weight: bold; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <h2>📋 Local Clipboard</h2>
    <form method="POST">
        <textarea name="text" placeholder="Paste your text or document content here...">{{ text }}</textarea>
        <button type="submit">Save & Share</button>
    </form>
    {% if saved %}
        <div class="status">✓ Updated successfully!</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    saved = False
    if request.method == 'POST':
        shared_data['text'] = request.form.get('text', '')
        saved = True
    return render_template_string(HTML_TEMPLATE, text=shared_data['text'], saved=saved)

if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible to all devices on the local network
    app.run(host='0.0.0.0', port=5000)
