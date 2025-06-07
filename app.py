from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Temporary in-memory store (single program allowed)
programs = []
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "new_program":
            if programs:
                flash("A program is already active. You can now Create a Day.", "error")
            else:
                program_name = request.form.get("program_name")
                if program_name:
                    programs.append({
                        "id": 1,
                        "name": program_name,
                    })
                    flash("Your program has been created — go ahead and Add Events to Program below.", "success")
                else:
                    flash("Program name is required.", "error")

        elif form_type == "clear_program":
            programs.clear()
            flash("Program cleared. You can create a new one now.", "info")

        return redirect(url_for("home"))

    return render_template("index.html", programs=programs, days=DAYS)

if __name__ == "__main__":
    app.run(debug=True, port=5005)
