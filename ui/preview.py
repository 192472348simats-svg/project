import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QFrame, QPushButton, QTextEdit, QScrollArea, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor

from core.analytics import StudentAnalytics
from core.paragraph_builder import ParagraphBuilder
from core.image_handler import ImageHandler


class PreviewView(QWidget):
    """
    Interactive Preview Screen allowing mentors to review calculated student analytics,
    risk badges, and the exact generated Slide 2 Parent Letter before exporting PPT reports.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.analytics_list = []
        self.current_student = None
        self.image_handler = ImageHandler()

        self._init_ui()

    def set_students(self, students: list):
        self.analytics_list = students
        self.student_combo.clear()
        for s in students:
            self.student_combo.addItem(f"{s.name} ({s.reg_no}) - Risk: {s.risk_level}")

        if students:
            self.student_combo.setCurrentIndex(0)
            self._update_preview(0)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Title & Selector
        header_layout = QHBoxLayout()
        title_lbl = QLabel("STUDENT REPORT & PARENT LETTER PREVIEW")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #818CF8;")
        header_layout.addWidget(title_lbl)

        header_layout.addStretch()

        combo_label = QLabel("Select Student:")
        combo_label.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        self.student_combo = QComboBox()
        self.student_combo.setMinimumWidth(320)
        self.student_combo.currentIndexChanged.connect(self._update_preview)

        header_layout.addWidget(combo_label)
        header_layout.addWidget(self.student_combo)

        layout.addLayout(header_layout)

        # -------------------------------------------------------------
        # PREVIEW CARD CONTAINER
        # -------------------------------------------------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.preview_card = QFrame()
        self.preview_card.setStyleSheet("background-color: #1E293B; border-radius: 12px; padding: 20px;")
        card_layout = QVBoxLayout(self.preview_card)
        card_layout.setSpacing(15)

        # Top Profile Section (Photo + Key Info)
        profile_row = QHBoxLayout()

        # Avatar Label
        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(140, 140)
        self.avatar_lbl.setStyleSheet("border-radius: 70px; border: 2px solid #6366F1; background-color: #0F172A;")
        profile_row.addWidget(self.avatar_lbl)

        # Student Key Information
        info_layout = QVBoxLayout()
        self.name_lbl = QLabel("Student Name")
        self.name_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #F8FAFC;")

        self.reg_dept_lbl = QLabel("Reg No | Department")
        self.reg_dept_lbl.setStyleSheet("font-size: 14px; color: #94A3B8;")

        self.risk_badge = QLabel("RISK: LOW")
        self.risk_badge.setStyleSheet("font-size: 14px; font-weight: bold; color: #10B981; padding: 4px 8px;")

        info_layout.addWidget(self.name_lbl)
        info_layout.addWidget(self.reg_dept_lbl)
        info_layout.addWidget(self.risk_badge)
        info_layout.addStretch()

        profile_row.addLayout(info_layout)
        profile_row.addStretch()

        card_layout.addLayout(profile_row)

        # -------------------------------------------------------------
        # STATS GRID CARDS
        # -------------------------------------------------------------
        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)

        self.card_att = self._create_stat_box("Overall Attendance", "0.0%", "Category: Good")
        self.card_arrears = self._create_stat_box("Active Arrears", "0", "Backlog Count")
        self.card_status = self._create_stat_box("Academic Standing", "Regular", "Status")
        self.card_rec_lvl = self._create_stat_box("Action Priority", "Standard", "Priority")

        stats_row.addWidget(self.card_att["frame"])
        stats_row.addWidget(self.card_arrears["frame"])
        stats_row.addWidget(self.card_status["frame"])
        stats_row.addWidget(self.card_rec_lvl["frame"])

        card_layout.addLayout(stats_row)

        # -------------------------------------------------------------
        # SLIDE 2 PARENT LETTER PREVIEW BOX
        # -------------------------------------------------------------
        letter_box = QFrame()
        letter_box.setStyleSheet("background-color: #0F172A; border-radius: 8px; padding: 15px;")
        l_layout = QVBoxLayout(letter_box)

        letter_header = QLabel("GENERATED SLIDE 2 PARENT LETTER (PARAGRAPH BUILDER)")
        letter_header.setStyleSheet("font-weight: bold; color: #818CF8; font-size: 13px;")

        self.parent_letter_txt = QTextEdit()
        self.parent_letter_txt.setReadOnly(True)
        self.parent_letter_txt.setMinimumHeight(240)
        self.parent_letter_txt.setStyleSheet("background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155; font-size: 12px; padding: 10px;")

        l_layout.addWidget(letter_header)
        l_layout.addWidget(self.parent_letter_txt)

        card_layout.addWidget(letter_box)

        self.scroll.setWidget(self.preview_card)
        layout.addWidget(self.scroll)

    def _create_stat_box(self, label: str, value: str, subtext: str):
        frame = QFrame()
        frame.setStyleSheet("background-color: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 10px;")
        l = QVBoxLayout(frame)

        lbl = QLabel(label.upper())
        lbl.setStyleSheet("font-size: 10px; font-weight: bold; color: #94A3B8;")

        val_lbl = QLabel(value)
        val_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #818CF8;")

        sub_lbl = QLabel(subtext)
        sub_lbl.setStyleSheet("font-size: 10px; color: #64748B;")

        l.addWidget(lbl)
        l.addWidget(val_lbl)
        l.addWidget(sub_lbl)

        return {"frame": frame, "val_lbl": val_lbl, "sub_lbl": sub_lbl}

    def _update_preview(self, index: int):
        if index < 0 or index >= len(self.analytics_list):
            return

        s: StudentAnalytics = self.analytics_list[index]
        self.current_student = s

        self.name_lbl.setText(s.name)
        self.reg_dept_lbl.setText(f"Register No: {s.reg_no}  |  Department: {s.department}")
        self.risk_badge.setText(f"RISK ASSESSMENT: {s.risk_level.upper()} RISK (Score: {s.risk_score}/100)")

        if s.risk_level in ["Critical", "High"]:
            self.risk_badge.setStyleSheet("font-size: 14px; font-weight: bold; color: #EF4444; background-color: #451A1A; padding: 4px 10px; border-radius: 6px;")
        elif s.risk_level == "Medium":
            self.risk_badge.setStyleSheet("font-size: 14px; font-weight: bold; color: #F59E0B; background-color: #45301A; padding: 4px 10px; border-radius: 6px;")
        else:
            self.risk_badge.setStyleSheet("font-size: 14px; font-weight: bold; color: #10B981; background-color: #1A382B; padding: 4px 10px; border-radius: 6px;")

        self.card_att["val_lbl"].setText(f"{s.overall_attendance:.1f}%")
        self.card_att["sub_lbl"].setText(f"Category: {s.attendance_category}")

        self.card_arrears["val_lbl"].setText(str(s.arrears))
        self.card_arrears["sub_lbl"].setText("Active Backlogs")

        self.card_status["val_lbl"].setText(s.academic_status)
        self.card_status["sub_lbl"].setText("Standing")

        self.card_rec_lvl["val_lbl"].setText(s.recommendation_level)
        self.card_rec_lvl["sub_lbl"].setText("Action Priority")

        # Generate Slide 2 Parent Letter text
        letter_text = ParagraphBuilder.generate_parent_letter(s)
        self.parent_letter_txt.setPlainText(letter_text)

        # Update Avatar Image
        photo_path = self.image_handler.get_student_image(s.reg_no, s.name, s.image_filename)
        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            self.avatar_lbl.setPixmap(pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
