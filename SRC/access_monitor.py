import pandas as pd


def detect_suspicious_access(log_file):
    logs = pd.read_csv(log_file)
    logs["timestamp"] = pd.to_datetime(logs["timestamp"])
    logs["hour"] = logs["timestamp"].dt.hour

    alerts = []

    # Rule 1: Unusual-hour downloads summarized by user
    unusual_downloads = logs[
        (logs["action"] == "download") &
        ((logs["hour"] < 6) | (logs["hour"] > 22))
    ]

    if not unusual_downloads.empty:
        grouped = unusual_downloads.groupby("user_id").size()

        for user, count in grouped.items():
            alerts.append(
                f"{user} performed {count} suspicious downloads during unusual hours"
            )

    # Rule 2: Too many downloads by same user
    download_counts = logs[logs["action"] == "download"].groupby("user_id").size()

    for user, count in download_counts.items():
        if count >= 3:
            alerts.append(
                f"High download activity detected: {user} downloaded {count} documents"
            )

    # Rule 3: Multiple failed access attempts
    failed_counts = logs[logs["action"] == "failed_access"].groupby("user_id").size()

    for user, count in failed_counts.items():
        if count >= 3:
            alerts.append(
                f"Multiple failed access attempts detected for {user}: {count} attempts"
            )

    return alerts