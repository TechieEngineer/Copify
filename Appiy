from flask import Flask, request, jsonify, render_template_string
import uuid

app = Flask(__name__)

# Memory storage tracking dynamic object metadata dictionaries
clipboard_history = []

# --- INJECT HTML INTERFACE TEMPLATE ENGINE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Local Clipboard</title>
    <style>
        :root { --bg-color: #f5f5f7; --card-bg: white; --text-color: #333; --sub-text: #666; --border-color: #e5e5e7; --accent-color: #0071e3; --btn-hover: #0077ed; --danger-color: #ff3b30; --danger-hover: #ff453a; }
        [data-theme="dark"] { --bg-color: #1c1c1e; --card-bg: #2c2c2e; --text-color: #f5f5f7; --sub-text: #aeaeb2; --border-color: #3a3a3c; --accent-color: #0a84ff; --btn-hover: #409cff; --danger-color: #ff453a; --danger-hover: #ff6961; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 1000px; margin: 40px auto; padding: 0 20px; background: var(--bg-color); color: var(--text-color); transition: background 0.3s, color 0.3s; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .subtitle { font-size: 14px; color: var(--sub-text); margin-top: -15px; margin-bottom: 20px; }
        .theme-btn { background: var(--card-bg); color: var(--text-color); border: 1px solid var(--border-color); padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 500; }
        textarea { width: 100%; height: 140px; padding: 12px; box-sizing: border-box; border: 1px solid var(--border-color); border-radius: 8px; font-size: 16px; resize: vertical; background: var(--card-bg); color: var(--text-color); }
        .submit-btn { background: var(--accent-color); color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; margin-top: 10px; width: 100%; font-weight: 500; }
        .submit-btn:hover { background: var(--btn-hover); }
        .history-section { margin-top: 40px; border-top: 2px solid var(--border-color); padding-top: 20px; }
        .history-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; }
        .history-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
        .history-item { background: var(--card-bg); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; min-height: 120px; position: relative; }
        .history-text { white-space: pre-wrap; word-break: break-all; font-size: 15px; margin-bottom: 15px; color: var(--text-color); padding-right: 25px; }
        .card-footer { display: flex; justify-content: flex-end; border-top: 1px solid var(--border-color); padding-top: 8px; gap: 8px; }
        .copy-btn { background: var(--bg-color); color: var(--accent-color); border: 1px solid var(--border-color); padding: 6px 12px; font-size: 13px; border-radius: 6px; cursor: pointer; flex-grow: 2; text-align: center; }
        .del-btn { background: transparent; color: var(--danger-color); border: 1px solid var(--danger-color); padding: 6px 12px; font-size: 13px; border-radius: 6px; cursor: pointer; flex-grow: 1; text-align: center; }
        .del-btn:hover { background: var(--danger-color); color: white; }
        .empty-state { color: var(--sub-text); font-style: italic; text-align: center; grid-column: 1 / -1; padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h2>📋 Live Local Clipboard</h2>
        <button class="theme-btn" onclick="toggleTheme()">🌓 Toggle Mode</button>
    </div>
    <p class="subtitle">Updates automatically across your local network.</p>

    <textarea id="textInput" placeholder="Paste your text or document content here..."></textarea>
    <button class="submit-btn" onclick="sendText()">Save & Share</button>

    <div class="history-section">
        <div class="history-title">📜 Shared History</div>
        <div id="historyList" class="history-list"></div>
    </div>

    <script>
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }
        if (localStorage.getItem('theme') === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }

        function sendText() {
            const inputField = document.getElementById('textInput');
            const text = inputField.value.trim();
            if (!text) return;
            fetch('/api/share', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => { inputField.value = ""; updateUI(data.history); });
        }

        function deleteItem(itemId) {
            fetch('/api/delete', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    updateUI(data.history);
                } else {
                    alert("Error: " + data.message);
                }
            });
        }

        function fetchUpdates() {
            fetch('/api/history').then(response => response.json()).then(data => { updateUI(data.history); });
        }

        function updateUI(history) {
            const listContainer = document.getElementById('historyList');
            if (history.length === 0) { listContainer.innerHTML = '<div class="empty-state">No clips shared yet.</div>'; return; }
            let html = "";
            history.forEach((item) => {
                const safeText = item.text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
                html += `<div class="history-item">
                    <div class="history-text">${safeText}</div>
                    <div class="card-footer">
                        <button class="copy-btn" onclick="universalCopy('${btoa(unescape(encodeURIComponent(safeText)))}')">Copy Text</button>
                        <button class="del-btn" onclick="deleteItem('${item.id}')">Delete</button>
                    </div>
                </div>`;
            });
            listContainer.innerHTML = html;
        }

        function universalCopy(base64Text) {
            const text = decodeURIComponent(escape(atob(base64Text)));
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(() => { alert("Copied!"); }).catch(err => fallbackCopy(text));
            } else {
                fallbackCopy(text);
            }
        }

        function fallbackCopy(text) {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed"; 
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.width = "2em";
            textArea.style.height = "2em";
            textArea.style.padding = "0";
            textArea.style.border = "none";
            textArea.style.outline = "none";
            textArea.style.boxShadow = "none";
            textArea.style.background = "transparent";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                const successful = document.execCommand('copy');
                if (successful) { alert("Copied!"); } else { alert("Unable to copy."); }
            } catch (err) {
                alert("Fallback copy failed.");
            }
            document.body.removeChild(textArea);
        }

        setInterval(fetchUpdates, 2000);
        fetchUpdates();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({"history": clipboard_history})

@app.route('/api/share', methods=['POST'])
def share_text():
    data = request.json or {}
    text_content = data.get('text', '').strip()
    if text_content:
        item_id = str(uuid.uuid4())[:8]
        clipboard_history.insert(0, {
            "id": item_id,
            "text": text_content
        })
        if len(clipboard_history) > 50:
            clipboard_history.pop()
    return jsonify({"success": True, "history": clipboard_history})

@app.route('/api/delete', methods=['DELETE'])
def delete_text():
    data = request.get_json(silent=True) or {}
    item_id = data.get('id')
    
    if not item_id:
        return jsonify({"success": False, "message": "Missing required item identity payload."}), 400
    
    target_item = next((item for item in clipboard_history if item["id"] == item_id), None)
    
    if not target_item:
        return jsonify({"success": False, "message": "Item not found in history"}), 404
        
    clipboard_history.remove(target_item)
    return jsonify({"success": True, "history": clipboard_history})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
