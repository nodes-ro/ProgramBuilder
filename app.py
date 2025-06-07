from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Only one program allowed at a time
program = None
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@app.route("/", methods=["GET", "POST"])
def home():
    global program

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "new_program":
            if program:
                flash("A program is already active. You can now add day info below.", "error")
            else:
                program_name = request.form.get("program_name")
                if program_name:
                    program = {
                        "id": 1,
                        "name": program_name,
                        "day": None,
                        "day_start": None,
                        "day_ends": None,
                        "stage_count": None
                    }
                    flash("Your program has been created — you can now add a day.", "success")
                else:
                    flash("Program name is required.", "error")

        elif form_type == "day_schedule":
            if not program:
                flash("Create a program first before adding a day.", "error")
            else:
                program["day"] = request.form.get("day")
                program["day_start"] = request.form.get("day_start")
                program["day_ends"] = request.form.get("day_ends")
                program["stage_count"] = request.form.get("stage_count")
                flash("Day added to program successfully.", "success")

        elif form_type == "clear_program":
            program = None
            flash("Program cleared. You can create a new one now.", "info")

        return redirect(url_for("home"))

    return render_template("index.html", program=program, days=DAYS)

if __name__ == "__main__":
    app.run(debug=True, port=5005)
