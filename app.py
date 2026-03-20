from flask import Flask, render_template, request
from scripts.basic_stats import run_basic_stats, run_kpis

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker","").upper().strip()
        ##Identifies which button was pressed
        action = request.form.get("action")
        
        try:
            if action == "stats":
                result = run_basic_stats(ticker)
            elif action== "kpis":
                result = run_kpis(ticker)
        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)