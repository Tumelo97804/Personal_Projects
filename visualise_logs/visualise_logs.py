from flask import Flask, render_template_string
from parse import parse_logs

# Create the Flask application
from flask import Flask, render_template
from parse import parse_logs  # assuming parse_logs is in log_parser.py

app = Flask(__name__)

@app.route("/")
def home():
    summary = parse_logs()
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
