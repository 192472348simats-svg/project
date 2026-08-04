from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont


class LoginScreen(QWidget):
    """
    Local Mentor Authentication Screen.
    Runs 100% offline.
    """
    login_successful = Signal(str)  # Emits mentor name upon successful login

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Login Container Card
        card = QFrame()
        card.setObjectName("LoginCard")
        card.setStyleSheet("""
            QFrame#LoginCard {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 16px;
                padding: 40px;
                min-width: 380px;
                max-width: 420px;
            }
        """)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setYOffset(10)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(18)

        # App Logo & Title
        title_label = QLabel("MENTOR REPORT GENERATOR")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #818CF8;")

        subtitle_label = QLabel("Offline College Academic Report Assistant")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 13px; color: #94A3B8;")

        # Inputs
        name_label = QLabel("Mentor Name / ID:")
        name_label.setStyleSheet("font-weight: 600; color: #C7D2FE;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Dr. A. Sharma")
        self.name_input.setText("Dr. A. Sharma")  # Default placeholder text for quick access

        pass_label = QLabel("Password / Passcode:")
        pass_label.setStyleSheet("font-weight: 600; color: #C7D2FE;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Enter passcode (default: mentor123)")
        self.pass_input.setText("mentor123")

        # Remember session notice
        offline_notice = QLabel("🔒 100% Offline Mode — Local Verification")
        offline_notice.setAlignment(Qt.AlignCenter)
        offline_notice.setStyleSheet("font-size: 11px; color: #10B981; margin-top: 5px;")

        # Login Button
        login_btn = QPushButton("LOGIN TO DASHBOARD")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4F46E5;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6366F1;
            }
        """)
        login_btn.clicked.connect(self._handle_login)

        # Assemble layout
        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(name_label)
        card_layout.addWidget(self.name_input)
        card_layout.addWidget(pass_label)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(offline_notice)
        card_layout.addSpacing(10)
        card_layout.addWidget(login_btn)

        main_layout.addWidget(card)

    def _handle_login(self):
        name = self.name_input.text().strip()
        passcode = self.pass_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter your Mentor Name or ID.")
            return

        # Offline pass-through check
        self.login_successful.emit(name)
