from flask import Flask, render_template, request, send_file
from datetime import datetime
import os

from SRC.content_similarity import check_similarity
from SRC.access_monitor import detect_suspicious_access
from SRC.risk_score import calculate_risk_score
from SRC.integrity_checker import verify_integrity
from SRC.pdf_report import generate_pdf


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "Reports"
PDF_REPORT_PATH = os.path.join(REPORT_FOLDER, "IP_Risk_Report.pdf")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        protected = request.files.get("protected_file")
        suspect = request.files.get("suspect_file")

        if not protected or not suspect:
            return render_template(
                "index.html",
                error="Please upload both protected and suspect documents."
            )

        protected_path = os.path.join(UPLOAD_FOLDER, protected.filename)
        suspect_path = os.path.join(UPLOAD_FOLDER, suspect.filename)

        protected.save(protected_path)
        suspect.save(suspect_path)

        similarity = check_similarity(protected_path, suspect_path)
        similarity_percentage = round(similarity * 100, 2)

        alerts = detect_suspicious_access("Data/access_logs.csv")

        overall_score, threat_level = calculate_risk_score(
            similarity_percentage,
            alerts
        )

        original_hash, uploaded_hash, integrity_status = verify_integrity(
            protected_path,
            suspect_path
        )

        alert_count = len(alerts)
        analysis_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

        explanation = (
            f"The suspect document shows {similarity_percentage}% similarity with the protected IP document. "
            f"The system also detected {alert_count} suspicious access-related indicators. "
            f"Based on document similarity, access behavior, and integrity verification, "
            f"the overall IP risk score is {overall_score}/100 with a {threat_level} threat level."
        )

        recommendations = []

        if similarity_percentage >= 70:
            recommendations.extend([
                "Review the suspected document for possible intellectual property duplication.",
                "Notify the original IP owner or responsible authority.",
                "Restrict sharing or redistribution of the suspected document."
            ])

        if alert_count >= 1:
            recommendations.extend([
                "Review suspicious user activity in access logs.",
                "Enable multi-factor authentication for sensitive document access.",
                "Limit bulk downloads and apply role-based access controls."
            ])

        if threat_level == "HIGH":
            recommendations.extend([
                "Conduct an immediate investigation of high-risk access behavior.",
                "Preserve logs and evidence for audit or legal review."
            ])

        recommendations.append(
            "Maintain SHA-256 hashes of protected IP documents for integrity verification."
        )

        generate_pdf(
            PDF_REPORT_PATH,
            similarity_percentage,
            overall_score,
            threat_level,
            alerts,
            explanation,
            recommendations,
            analysis_time,
            integrity_status,
            original_hash,
            uploaded_hash
        )

        return render_template(
            "index.html",
            similarity=similarity_percentage,
            alerts=alerts,
            risk=overall_score,
            threat=threat_level,
            explanation=explanation,
            recommendations=recommendations,
            original_hash=original_hash,
            uploaded_hash=uploaded_hash,
            integrity_status=integrity_status,
            alert_count=alert_count,
            analysis_time=analysis_time,
            pdf_available=True
        )

    return render_template("index.html")


@app.route("/download-report")
def download_report():
    return send_file(PDF_REPORT_PATH, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)