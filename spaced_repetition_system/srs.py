from datetime import datetime, timedelta

INTERVALS = [0, 3, 7, 21]


def get_next_review(last_modified: datetime):
    timedelta_since_last_modified = datetime.now().date() - last_modified.date()
    closest_interval = next(iter([x for x in INTERVALS if x - timedelta_since_last_modified.days >= 0]), INTERVALS[-1])
    next_review = datetime.now() + timedelta(days=closest_interval-timedelta_since_last_modified.days % 21)
    return next_review