from flask import Flask, render_template

app = Flask(__name__)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TIME_AXIS = [ "30 min", "60 min"]
@app.route("/")
def home():
    # Flask now renders the file templates/index.html
    return render_template("index.html", days=DAYS, time_axis=TIME_AXIS)

if __name__ == "__main__":
    app.run(debug=True,port=5005)
