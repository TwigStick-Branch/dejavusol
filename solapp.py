from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = 'https://webhook.site/2e33a9ef-cb19-4159-b5ae-2982a3fd3c12'


# 1. Serve an HTML page that listens for postMessage
@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
  <body>
    <h2>Flask Page Ready</h2>
    <script>
      window.addEventListener("message", function(event) {
        // For testing, log the message
        console.log("Received message:", event.data);

        // Send to Flask's /receive
        fetch('/receive', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ data: event.data })
        })
        .then(res => res.json())
        .then(resp => console.log('Forwarded to webhook:', resp))
        .catch(err => console.error('Error:', err));
      });
    </script>
  </body>
</html>
''')

# 2. Forward received data to your webhook
@app.route('/receive', methods=['GET','POST'])
def receive_message():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    try:
        resp = requests.post(WEBHOOK_URL, json=data)
        return jsonify({"status": "forwarded", "webhook_response": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()