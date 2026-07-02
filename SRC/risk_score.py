def calculate_risk_score(similarity_percentage, access_alerts):
    score = 0

    # Content similarity risk
    if similarity_percentage >= 70:
        score += 60
    elif similarity_percentage >= 40:
        score += 35
    else:
        score += 10

    # Access behavior risk
    alert_count = len(access_alerts)

    if alert_count >= 5:
        score += 40
    elif alert_count >= 3:
        score += 30
    elif alert_count >= 1:
        score += 15
    else:
        score += 0

    if score >= 80:
        threat_level = "HIGH"
    elif score >= 50:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    return min(score, 100), threat_level