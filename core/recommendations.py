from typing import List
from .analytics import StudentAnalytics


class RecommendationEngine:
    """
    Generates deterministic, actionable mentor recommendations based on analytics.
    """

    @classmethod
    def generate_recommendations(cls, analytics: StudentAnalytics) -> List[str]:
        recommendations = []

        # 1. Attendance-based recommendations
        att = analytics.overall_attendance
        lowest_subj, lowest_val = analytics.lowest_subject

        if att < 60.0:
            recommendations.append(
                f"Schedule an immediate one-on-one counseling session regarding overall critical attendance ({att:.1f}%)."
            )
            recommendations.append(
                "Notify parents/guardians regarding mandatory attendance requirements and potential condonation issues."
            )
        elif att < 75.0:
            recommendations.append(
                f"Advise student to boost attendance in {lowest_subj} ({lowest_val:.1f}%) to cross the 75% threshold."
            )
            recommendations.append("Issue attendance warning letter and monitor weekly class log.")

        # 2. Arrears & Academic status recommendations
        if analytics.arrears > 4:
            recommendations.append(
                f"Mandatory enrollment in remedial classes for {analytics.arrears} active arrears."
            )
            recommendations.append("Assign a peer tutor for core subject revision prior to semester end exams.")
        elif analytics.arrears > 0:
            recommendations.append(
                f"Focus on clearing {analytics.arrears} active arrear(s) during upcoming re-examinations."
            )

        # 3. High performer recommendations
        if analytics.risk_level == "Low" and att >= 85.0:
            recommendations.append("Encourage student to pursue advanced NPTEL / SWAYAM certifications or research publications.")
            recommendations.append("Nominate student for department student council or technical club leadership roles.")

        # 4. NPTEL / Certification encouragement
        if not analytics.nptel_courses or analytics.nptel_courses.strip().lower() in ["none", "nil", "n/a"]:
            if analytics.arrears == 0:
                recommendations.append("Recommend registering for at least one NPTEL/Coursera domain course to enhance resume.")
        else:
            recommendations.append(f"Commend student for active completion of NPTEL course: {analytics.nptel_courses}.")

        # Fallback default if empty
        if not recommendations:
            recommendations.append("Maintain current academic standing with regular attendance and class participation.")

        return recommendations
