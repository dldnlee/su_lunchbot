from datetime import datetime

def convert_time_to_slack_ts(time_str: str) -> str:
    # Parse the provided time (e.g., '18:00') and set it for today's date
    now = datetime.now()
    hour, minute = map(int, time_str.split(":"))
    target_time = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute, second=0, microsecond=6)
    
    # Convert to Unix timestamp
    unix_timestamp = target_time.timestamp()
    return str(unix_timestamp)