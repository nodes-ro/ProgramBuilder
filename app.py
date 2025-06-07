from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Temporary in-memory store
programs = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        program_name = request.form.get("program_name")
        program_description = request.form.get("program_description")

        if program_name:
            # Add new program to the list
            programs.append({
                "id": len(programs) + 1,
                "name": program_name,
                "description": program_description
            })
            flash("Your program has been created — go ahead and Add Events to Program below.", "success")
        else:
            flash("Program name is required.", "error")

        return redirect(url_for("home"))

    return render_template("index.html", programs=programs)

if __name__ == "__main__":
    app.run(debug=True, port=5005)
