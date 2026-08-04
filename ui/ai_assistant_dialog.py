from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt


class AIAssistantDialog(QDialog):
    """
    UI Dialog for the reserved AI Writing Assistant module.
    Currently DISABLED by default as per core offline specification.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Writing Assistant (Reserved Module)")
        self.setFixedSize(540, 420)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Title
        title_lbl = QLabel("AI WRITING ASSISTANT (RESERVED MODULE)")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #818CF8;")
        layout.addWidget(title_lbl)

        # Disabled Banner Frame
        banner = QFrame()
        banner.setStyleSheet("background-color: #451A1A; border: 1px solid #EF4444; border-radius: 8px; padding: 12px;")
        b_layout = QVBoxLayout(banner)

        b_lbl = QLabel("⚠️ MODULE DISABLED (FUTURE EXTENSION)")
        b_lbl.setStyleSheet("font-weight: bold; color: #EF4444; font-size: 13px;")

        b_desc = QLabel(
            "The AI Writing Assistant is reserved for future online LLM integrations.\n"
            "By design, all core analytics, risk scoring, attendance calculations, "
            "and PowerPoint report generation remain 100% offline, deterministic, "
            "and rule-based."
        )
        b_desc.setWordWrap(True)
        b_desc.setStyleSheet("color: #FCA5A5; font-size: 11px;")

        b_layout.addWidget(b_lbl)
        b_layout.addWidget(b_desc)
        layout.addWidget(banner)

        # Mock Sample Interface Box
        mock_box = QFrame()
        mock_box.setStyleSheet("background-color: #1E293B; border-radius: 8px; padding: 12px;")
        m_layout = QVBoxLayout(mock_box)

        lbl1 = QLabel("Sample Remark Polish Preview:")
        lbl1.setStyleSheet("font-weight: bold; color: #C7D2FE;")

        self.input_txt = QTextEdit()
        self.input_txt.setPlaceholderText("Raw Mentor Remark: 'Good student, needs attendance boost in maths.'")
        self.input_txt.setPlainText("Raw Mentor Remark: 'Good student, needs attendance boost in maths.'")
        self.input_txt.setEnabled(False)

        lbl2 = QLabel("Rule Restriction:")
        lbl2.setStyleSheet("font-weight: bold; color: #10B981; font-size: 11px;")

        rule_lbl = QLabel("🔒 The AI Assistant can ONLY rewrite narrative text. It is STRICTLY PROHIBITED from modifying numerical attendance data or calculated risk levels.")
        rule_lbl.setWordWrap(True)
        rule_lbl.setStyleSheet("color: #94A3B8; font-size: 10px;")

        m_layout.addWidget(lbl1)
        m_layout.addWidget(self.input_txt)
        m_layout.addWidget(lbl2)
        m_layout.addWidget(rule_lbl)

        layout.addWidget(mock_box)

        # Close Button
        close_btn = QPushButton("CLOSE DIALOG")
        close_btn.setStyleSheet("background-color: #334155; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
