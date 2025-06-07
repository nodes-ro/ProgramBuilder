from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

program = None
events = []  # Optional, for event support later
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
                        "days": []  # ✅ Correct structure
                    }
                    flash("Your program has been created — you can now add days.", "success")
                else:
                    flash("Program name is required.", "error")

        elif form_type == "day_schedule":
            if not program:
                flash("Create a program first before adding a day.", "error")
            else:
                day_info = {
                    "day": request.form.get("day"),
                    "day_start": request.form.get("day_start"),
                    "day_ends": request.form.get("day_ends"),
                    "stage_count": request.form.get("stage_count")
                }

                # Optional: prevent duplicates
                if any(d["day"] == day_info["day"] for d in program["days"]):
                    flash(f"Day '{day_info['day']}' already exists.", "warning")
                else:
                    program["days"].append(day_info)
                    flash(f"Day '{day_info['day']}' added to the program.", "success")

        elif form_type == "new_event":
            if not program:
                flash("Create a program and add at least one day before adding events.", "error")
            else:
                event = {
                    "day": request.form.get("day"),
                    "stage": request.form.get("stage"),
                    "title": request.form.get("title"),
                    "detail": request.form.get("detail"),
                    "event_start": request.form.get("event_start"),
                    "event_end": request.form.get("event_end"),
                    "picture": None  # You can add file upload support later
                }
                events.append(event)
                flash(f"Event '{event['title']}' added to {event['day']} (Stage {event['stage']}).", "success")


        elif form_type == "clear_program":
            program = None
            flash("Program cleared. You can create a new one now.", "info")

        return redirect(url_for("home"))

    return render_template("index.html", program=program, days=DAYS, events=events)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
