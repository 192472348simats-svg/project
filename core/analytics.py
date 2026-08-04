from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional


@dataclass
class StudentAnalytics:
    """
    Data container holding deterministic analytics results for a student.
    """
    name: str
    reg_no: str
    department: str
    overall_attendance: float
    attendance_category: str  # Excellent, Good, Needs Improvement, Critical
    best_subject: Tuple[str, float]
    lowest_subject: Tuple[str, float]
    arrears: int
    completed_courses: int
    nptel_courses: str
    academic_status: str  # Distinction, Regular, Probation, Warning
    risk_level: str  # Low, Medium, High, Critical
    risk_score: int  # 0 to 100 numeric score for sorting/visualization
    recommendation_level: str  # High Priority, Moderate Support, Standard Monitoring, Praise & Maintain
    mentor_remarks: str
    achievements: str
    image_filename: str


class AnalyticsEngine:
    """
    Deterministic rule-based analytics engine for student performance data.
    """

    @classmethod
    def analyze_student(cls, student_record: Dict[str, Any]) -> StudentAnalytics:
        name = student_record.get("name", "Unknown")
        reg_no = student_record.get("reg_no", "N/A")
        dept = student_record.get("department", "General")
        attendance = float(student_record.get("overall_attendance", 0.0))
        arrears = int(student_record.get("arrears", 0))
        completed_courses = int(student_record.get("completed_courses", 0))
        nptel = student_record.get("nptel_courses", "None")
        remarks = student_record.get("mentor_remarks", "")
        achievements = student_record.get("achievements", "None")
        image_fn = student_record.get("image_filename", "")

        subject_att = student_record.get("subject_attendance", {})
        best_subject, lowest_subject = cls._compute_subject_extremes(subject_att, attendance)

        att_category = cls.get_attendance_category(attendance)
        risk_level, risk_score = cls.calculate_risk(attendance, arrears)
        academic_status = cls.calculate_academic_status(attendance, arrears, completed_courses)
        rec_level = cls.get_recommendation_level(risk_level, att_category)

        return StudentAnalytics(
            name=name,
            reg_no=reg_no,
            department=dept,
            overall_attendance=attendance,
            attendance_category=att_category,
            best_subject=best_subject,
            lowest_subject=lowest_subject,
            arrears=arrears,
            completed_courses=completed_courses,
            nptel_courses=nptel,
            academic_status=academic_status,
            risk_level=risk_level,
            risk_score=risk_score,
            recommendation_level=rec_level,
            mentor_remarks=remarks,
            achievements=achievements,
            image_filename=image_fn
        )

    @staticmethod
    def get_attendance_category(attendance: float) -> str:
        if attendance >= 90.0:
            return "Excellent"
        elif attendance >= 75.0:
            return "Good"
        elif attendance >= 60.0:
            return "Needs Improvement"
        else:
            return "Critical"

    @staticmethod
    def calculate_risk(attendance: float, arrears: int) -> Tuple[str, int]:
        """
        Determines risk level and 0-100 numerical risk score.
        Rules:
        - Critical Risk: Attendance < 50% or Arrears > 5
        - High Risk: Attendance < 60% and Arrears > 4 (or Attendance < 60% with Arrears > 2)
        - Medium Risk: Attendance < 75% or Arrears > 2
        - Low Risk: Otherwise
        """
        base_score = 0

        # Attendance penalty
        if attendance < 50:
            base_score += 50
        elif attendance < 60:
            base_score += 35
        elif attendance < 75:
            base_score += 20
        elif attendance < 85:
            base_score += 5

        # Arrears penalty
        if arrears > 5:
            base_score += 50
        elif arrears > 4:
            base_score += 40
        elif arrears > 2:
            base_score += 25
        elif arrears > 0:
            base_score += 10

        risk_score = min(100, base_score)

        if attendance < 50 or arrears > 5 or risk_score >= 80:
            return "Critical", risk_score
        elif (attendance < 60 and arrears > 4) or risk_score >= 60:
            return "High", risk_score
        elif (attendance < 75 or arrears > 2) or risk_score >= 30:
            return "Medium", risk_score
        else:
            return "Low", risk_score

    @staticmethod
    def calculate_academic_status(attendance: float, arrears: int, completed_courses: int) -> str:
        if attendance >= 85.0 and arrears == 0 and completed_courses >= 3:
            return "Distinction / Honor Roll"
        elif attendance >= 75.0 and arrears <= 2:
            return "Regular Standing"
        elif attendance < 60.0 or arrears > 4:
            return "Academic Warning"
        else:
            return "Academic Probation"

    @staticmethod
    def get_recommendation_level(risk_level: str, att_category: str) -> str:
        if risk_level in ["Critical", "High"]:
            return "Urgent Intervention Required"
        elif risk_level == "Medium" or att_category == "Needs Improvement":
            return "Targeted Academic Support Needed"
        elif att_category == "Good":
            return "Standard Regular Monitoring"
        else:
            return "Commendation & Advanced Growth"

    @staticmethod
    def _compute_subject_extremes(subject_att: Dict[str, float], overall_att: float) -> Tuple[Tuple[str, float], Tuple[str, float]]:
        if not subject_att:
            return ("General", overall_att), ("General", overall_att)

        sorted_subjs = sorted(subject_att.items(), key=lambda x: x[1], reverse=True)
        best = sorted_subjs[0]
        lowest = sorted_subjs[-1]
        return best, lowest
