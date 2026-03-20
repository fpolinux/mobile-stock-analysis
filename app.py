from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        ticker = request.form.get("ticker","").upper().strip()
        result = f"Running analysis for {ticker}"
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)