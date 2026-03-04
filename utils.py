from datetime import datetime


def get_settlement_period(timestamp: datetime) -> int:
    # 2 settlement periods per hour, 1-indexed
    return (timestamp.hour * 2) + (1 if timestamp.minute >= 30 else 0) + 1


def get_start_and_end_of_settlement_period(
    timestamp: datetime,
) -> tuple[datetime, datetime]:
    """
    Returns the start and end timestamps for the settlement period containing the given datetime.
    Settlement periods are 30-minute blocks.

    Args:
        timestamp: A datetime object

    Returns:
        A tuple of (datetime, datetime) for the settlement period
    """
    # Determine if we're in the first half (00-29 mins) or second half (30-59 mins) of the hour
    if timestamp.minute < 30:
        start_minute = 0
        end_minute = 29
    else:
        start_minute = 30
        end_minute = 59

    start = timestamp.replace(minute=start_minute, second=0, microsecond=0)
    end = timestamp.replace(minute=end_minute, second=59, microsecond=999999)

    return start, end
