from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

program = None
events = []
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@app.route("/", methods=["GET", "POST"])
def home():
    global program, events

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
                        "days": []
                    }
                    events = []
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

                if any(d["day"] == day_info["day"] for d in program["days"]):
                    flash(f"Day '{day_info['day']}' already exists.", "warning")
                else:
                    program["days"].append(day_info)
                    program["days"].sort(key=lambda d: DAYS.index(d["day"]))
                    flash(f"Day '{day_info['day']}' added to the program.", "success")

        elif form_type == "new_event":
            if not program or not program.get("days"):
                flash("Create a program and add at least one day before adding events.", "error")
            else:
                day = request.form.get("day")
                stage = request.form.get("stage")
                title = request.form.get("title")
                detail = request.form.get("detail")
                start = request.form.get("event_start")
                end = request.form.get("event_end")

                if not all([day, stage, title, detail, start, end]):
                    flash("All event fields are required.", "error")
                else:
                    # Find the selected day
                    day_obj = next((d for d in program["days"] if d["day"] == day), None)
                    if not day_obj:
                        flash(f"Day '{day}' not found in the current program.", "error")
                    elif int(stage) > int(day_obj["stage_count"]):
                        flash(f"Stage {stage} exceeds the number of stages ({day_obj['stage_count']}) for {day}.",
                              "error")
                    else:
                        event = {
                            "day": day,
                            "stage": int(stage),
                            "title": title.strip(),
                            "detail": detail.strip(),
                            "event_start": start,
                            "event_end": end,
                            "picture": None
                        }
                        events.append(event)
                        flash(f"Event '{title}' added to {day} (Stage {stage}).", "success")


        elif form_type == "clear_program":
            program = None
            events = []
            flash("Program cleared. You can create a new one now.", "info")

        return redirect(url_for("home"))

    return render_template("index.html", program=program, days=DAYS, events=events)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
