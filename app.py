from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

program = None
events = []
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# --- Handlers ---

def handle_new_program():
    global program, events
    if program:
        flash("A program is already active. You can now add day info below.", "error")
    else:
        name = request.form.get("program_name")
        if name:
            program = {"id": 1, "name": name, "days": []}
            events = []
            flash("Your program has been created — you can now add days.", "success")
        else:
            flash("Program name is required.", "error")


def handle_day_schedule():
    if not program:
        flash("Create a program first before adding a day.", "error")
        return

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



def handle_new_event():
    if not program or not program.get("days"):
        flash("Create a program and add at least one day before adding events.", "error")
        return

    day = request.form.get("day")
    stage = request.form.get("stage")
    title = request.form.get("title")
    detail = request.form.get("detail")
    start = request.form.get("event_start")
    end = request.form.get("event_end")
    picture = request.form.get("picture_url") or None


    if not all([day, stage, title, detail, start, end]):
        flash("All event fields are required.", "error")
        return

    day_obj = next((d for d in program["days"] if d["day"] == day), None)
    if not day_obj:
        flash(f"Day '{day}' not found in the current program.", "error")
        return

    # parse times as datetime.time
    fmt = "%H:%M"
    try:
        ev_start = datetime.strptime(start, fmt).time()
        ev_end   = datetime.strptime(end, fmt).time()
        day_start = datetime.strptime(day_obj["day_start"], fmt).time()
        day_end   = datetime.strptime(day_obj["day_ends"], fmt).time()
    except ValueError:
        flash("Invalid time format.", "error")
        return

    # check ordering
    if ev_end <= ev_start:
        flash("Event end time must be after its start time.", "error")
        return

    # check within day window
    if ev_start < day_start or ev_end > day_end:
        flash(
          f"Event '{title}' must fall between {day_obj['day_start']} and {day_obj['day_ends']} for {day}.",
          "warning"
        )
        return

    if int(stage) > int(day_obj["stage_count"]):
        flash(
          f"Stage {stage} exceeds the number of stages ({day_obj['stage_count']}) for {day}.",
          "error"
        )
        return

    # all good—add the event
    events.append({
        "day": day,
        "stage": int(stage),
        "title": title.strip(),
        "detail": detail.strip(),
        "event_start": start,
        "event_end": end,
        "picture": picture
    })
    flash(f"Event '{title}' added to {day} (Stage {stage}).", "success")



def handle_set_interval():
    if not program:
        flash("Create a program first.", "error")
        return
    try:
        interval = int(request.form.get("slot_interval", 30))
        if interval not in (60, 30, 15, 10):
            raise ValueError
        program["slot_interval"] = interval
        flash(f"Slot interval set to {interval} minutes.", "success")
    except ValueError:
        flash("Invalid interval.", "error")


def handle_clear_program():
    global program, events
    program = None
    events = []
    session.pop("table_styles", None)  # Clear style on reset
    flash("Program cleared. You can create a new one now.", "info")


def handle_set_styles():
    selected = request.form.getlist("styles")
    if "default" in selected:
        session["table_styles"] = []
    else:
        session["table_styles"] = selected
    flash("Table styles updated.", "success")


# --- Routes ---

@app.route("/", methods=["GET", "POST"])
def home():
    form_handlers = {
        "new_program": handle_new_program,
        "day_schedule": handle_day_schedule,
        "new_event": handle_new_event,
        "set_interval": handle_set_interval,
        "clear_program": handle_clear_program,
        "set_styles": handle_set_styles,
    }

    if request.method == "POST":
        form_type = request.form.get("form_type")
        handler = form_handlers.get(form_type)
        if handler:
            handler()
        else:
            flash("Unknown form submission.", "error")
        return redirect(url_for("home"))

    return render_template(
        "index.html",
        program=program,
        days=DAYS,
        events=events,
        table_styles=session.get("table_styles", [])
    )


if __name__ == "__main__":
    app.run(debug=True, port=5005)
