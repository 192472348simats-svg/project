import os
import tempfile
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend suitable for PySide6 & thread execution
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Optional


class ChartGenerator:
    """
    Generates high-resolution Matplotlib charts for embedding into PowerPoint reports.
    """

    # High contrast modern color palette matching app aesthetics
    COLORS = {
        "primary": "#6366F1",     # Indigo
        "secondary": "#3B82F6",   # Blue
        "accent": "#10B981",      # Emerald Green
        "warning": "#F59E0B",     # Amber
        "danger": "#EF4444",      # Red
        "background": "#F8FAFC",  # Light slate
        "text": "#1E293B",        # Dark text
        "grid": "#E2E8F0"         # Light grid lines
    }

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or os.path.join(tempfile.gettempdir(), "mentor_report_charts")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_subject_attendance_chart(self, reg_no: str, subject_attendance: Dict[str, float], overall_att: float) -> str:
        """
        Renders horizontal bar chart for subject-wise attendance and saves to PNG file.
        """
        output_path = os.path.join(self.output_dir, f"chart_{reg_no}_subjects.png")

        # Setup figure
        plt.style.use("ggplot")
        fig, ax = plt.subplots(figsize=(6.5, 3.5), dpi=300)
        fig.patch.set_facecolor("white")
        ax.set_facecolor("#FAFAFA")

        if not subject_attendance:
            subjects = ["Overall Attendance"]
            percentages = [overall_att]
        else:
            subjects = list(subject_attendance.keys())
            percentages = list(subject_attendance.values())

        y_pos = np.arange(len(subjects))

        # Color bars based on threshold
        bar_colors = []
        for val in percentages:
            if val >= 85:
                bar_colors.append("#10B981") # Green
            elif val >= 75:
                bar_colors.append("#3B82F6") # Blue
            elif val >= 60:
                bar_colors.append("#F59E0B") # Amber
            else:
                bar_colors.append("#EF4444") # Red

        bars = ax.barh(y_pos, percentages, align="center", color=bar_colors, height=0.55, edgecolor="none")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(subjects, fontsize=9, fontweight="bold", color="#334155")
        ax.invert_yaxis()  # top-down

        # Add 75% threshold reference line
        ax.axvline(75, color="#EF4444", linestyle="--", linewidth=1.2, label="75% Requirement")

        ax.set_xlim(0, 105)
        ax.set_xlabel("Attendance (%)", fontsize=9, fontweight="bold", color="#475569")
        ax.set_title("Subject-wise Attendance Breakdown", fontsize=11, fontweight="bold", pad=10, color="#0F172A")
        ax.grid(axis="x", color="#E2E8F0", linestyle=":", linewidth=0.8)

        # Value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 1.5,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}%",
                ha="left",
                va="center",
                fontsize=8.5,
                fontweight="bold",
                color="#1E293B"
            )

        ax.legend(loc="lower right", fontsize=8, frameon=True, facecolor="white", edgecolor="#E2E8F0")

        plt.tight_layout()
        fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)

        return output_path

    def generate_overall_donut_chart(self, reg_no: str, overall_att: float) -> str:
        """
        Renders donut chart showing overall attendance vs absent percentage.
        """
        output_path = os.path.join(self.output_dir, f"chart_{reg_no}_donut.png")

        fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=300)
        fig.patch.set_facecolor("white")

        present = min(100.0, max(0.0, overall_att))
        absent = 100.0 - present

        color_present = "#10B981" if present >= 75 else ("#F59E0B" if present >= 60 else "#EF4444")
        color_absent = "#E2E8F0"

        wedges, texts = ax.pie(
            [present, absent],
            colors=[color_present, color_absent],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2)
        )

        # Center label
        ax.text(0, 0, f"{present:.1f}%\nPresent", ha="center", va="center", fontsize=12, fontweight="bold", color="#0F172A")
        ax.set_title("Overall Attendance", fontsize=10, fontweight="bold", pad=8, color="#334155")

        plt.tight_layout()
        fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)

        return output_path
