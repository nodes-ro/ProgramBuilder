from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # One-to-many relationship: Program → Events
    events = db.relationship("Event", backref="program", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Program {self.name}>"

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key: each Event belongs to a Program
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)

    # Assigned day (e.g., "Monday")
    day = db.Column(db.String(16), nullable=False)

    # Time boundaries for the day's schedule
    day_start = db.Column(db.String(5), nullable=False)
    day_end = db.Column(db.String(5), nullable=False)

    # Core event details
    title = db.Column(db.String(120), nullable=False)
    detail = db.Column(db.String(240), nullable=False)

    # Optional image path
    picture = db.Column(db.String(255))

    # Time boundaries for the specific event
    event_start = db.Column(db.String(5), nullable=False)
    event_end = db.Column(db.String(5), nullable=False)

    # Optional stage name (e.g., "Main", "Workshop A")
    stage = db.Column(db.String(120))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Event '{self.title}' on {self.day} (Program {self.program_id})>"
