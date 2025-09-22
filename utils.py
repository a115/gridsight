from datetime import datetime


def get_settlement_period(datetime: datetime) -> int:
    # 2 settlement periods per hour, 1-indexed
    return (datetime.hour * 2) + (1 if datetime.minute >= 30 else 0) + 1
