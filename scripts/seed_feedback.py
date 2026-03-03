"""Seed feedback data from feedback_data.json into the database."""

import sys
import json
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import get_session, engine
from database.models import Base, Feedback
from api.crud import create_feedback
from config import FEEDBACK_DATA_PATH


def seed_feedback():
    """Load feedback_data.json into DB if not already seeded."""
    Base.metadata.create_all(bind=engine)
    db = get_session()

    try:
        existing_count = db.query(Feedback).count()
        if existing_count > 0:
            print(f"[seed] {existing_count} feedbacks already in DB, skipping seed.")
            return

        if not FEEDBACK_DATA_PATH.exists():
            print(f"[seed] {FEEDBACK_DATA_PATH} not found, skipping.")
            return

        with open(FEEDBACK_DATA_PATH) as f:
            feedbacks = json.load(f)

        print(f"[seed] Inserting {len(feedbacks)} feedbacks...")
        for fb in feedbacks:
            fb_date = fb.get("feedback_date")
            if isinstance(fb_date, str):
                fb_date = date.fromisoformat(fb_date)
            create_feedback(
                db=db,
                username=fb["username"],
                campaign_id=fb["campaign_id"],
                comment=fb["comment"],
                feedback_date=fb_date,
            )
        print(f"[seed] Done! {len(feedbacks)} feedbacks inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_feedback()
