from content_similarity import check_similarity
from access_monitor import detect_suspicious_access
from risk_score import calculate_risk_score
from datetime import datetime

original_doc = "data/protected_docs/original_ip.txt"
suspect_doc = "data/uploaded_docs/suspect_document.txt"
log_file = "data/access_logs.csv"

report_path = "reports/ip_monitoring_risk_report.txt"

print("Secure Digital IP Monitoring System")
print("-----------------------------------")

report = []
report.append("Secure Digital IP Monitoring System - Risk Report")
report.append("Generated On: " + str(datetime.now()))
report.append("-----------------------------------------------")

score = check_similarity(original_doc, suspect_doc)
percentage = round(score * 100, 2)

alerts = detect_suspicious_access(log_file)

overall_score, overall_level = calculate_risk_score(
    percentage,
    alerts
)

print(f"\nContent Similarity Score: {percentage}%")
report.append(f"\nContent Similarity Score: {percentage}%")

if percentage >= 70:
    content_status = "Possible IP duplication detected"
    content_risk = "HIGH"
elif percentage >= 40:
    content_status = "Partial content similarity detected"
    content_risk = "MEDIUM"
else:
    content_status = "No major duplication detected"
    content_risk = "LOW"

print(f"Alert: {content_status}")
print(f"Content Risk Level: {content_risk}")

report.append(f"Content Alert: {content_status}")
report.append(f"Content Risk Level: {content_risk}")

print("\nSuspicious Access Monitoring")
print("----------------------------")

report.append("\nSuspicious Access Monitoring")
report.append("----------------------------")

if alerts:
    for alert in alerts:
        print(f"Alert: {alert}")
        report.append(f"Access Alert: {alert}")
    access_risk = "HIGH"
else:
    print("No suspicious access activity detected")
    report.append("No suspicious access activity detected")
    access_risk = "LOW"

print(f"Access Risk Level: {access_risk}")
report.append(f"Access Risk Level: {access_risk}")

with open(report_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print(f"\nRisk report generated successfully: {report_path}")

print("\nOverall AI Risk Assessment")
print("--------------------------")
print(f"Overall Risk Score : {overall_score}/100")
print(f"Threat Level       : {overall_level}")

report.append("\nOverall AI Risk Assessment")
report.append("--------------------------")
report.append(f"Overall Risk Score : {overall_score}/100")
report.append(f"Threat Level       : {overall_level}")

with open(report_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report))