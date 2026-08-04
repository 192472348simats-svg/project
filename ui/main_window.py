import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QPushButton, QLabel, QFrame, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.login import LoginScreen
from ui.dashboard import DashboardView
from ui.preview import PreviewView
from ui.settings import SettingsView
from ui.ai_assistant_dialog import AIAssistantDialog


class MainWindow(QMainWindow):
    """
    Main Application Window container featuring sidebar navigation,
    stacked views, and status bar.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mentor Report Generator — Offline College Academic Suite")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 700)

        self.current_mentor = ""
        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------------------------------------------
        # 1. SIDEBAR NAVIGATION FRAME
        # -------------------------------------------------------------
        self.sidebar = QFrame()
        self.sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(8)

        # App Logo & Title
        app_title = QLabel("MENTOR REPORT")
        app_title.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(app_title)

        app_sub = QLabel("Academic Suite v1.0")
        app_sub.setStyleSheet("font-size: 11px; color: #64748B; padding-left: 10px; margin-bottom: 15px;")
        sidebar_layout.addWidget(app_sub)

        # Navigation Buttons
        self.btn_dashboard = QPushButton("📊  Dashboard")
        self.btn_dashboard.setProperty("class", "nav-btn active")
        self.btn_dashboard.clicked.connect(lambda: self.switch_view(0))

        self.btn_preview = QPushButton("🔍  Preview Reports")
        self.btn_preview.setProperty("class", "nav-btn")
        self.btn_preview.clicked.connect(lambda: self.switch_view(1))

        self.btn_settings = QPushButton("⚙️  Settings")
        self.btn_settings.setProperty("class", "nav-btn")
        self.btn_settings.clicked.connect(lambda: self.switch_view(2))

        self.btn_ai = QPushButton("🤖  AI Assistant (Stub)")
        self.btn_ai.setProperty("class", "nav-btn")
        self.btn_ai.clicked.connect(self._open_ai_dialog)

        self.btn_logout = QPushButton("🚪  Logout")
        self.btn_logout.setProperty("class", "nav-btn")
        self.btn_logout.clicked.connect(self._handle_logout)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_preview)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addWidget(self.btn_ai)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        main_layout.addWidget(self.sidebar)

        # -------------------------------------------------------------
        # 2. MAIN CONTENT STACK
        # -------------------------------------------------------------
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top Header Bar
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #1E293B; border-bottom: 1px solid #334155; padding: 10px 20px;")
        tb_layout = QHBoxLayout(top_bar)

        self.mentor_status_lbl = QLabel("Logged in as: Guest Mentor")
        self.mentor_status_lbl.setStyleSheet("font-weight: bold; color: #C7D2FE;")

        mode_lbl = QLabel("🔒 100% Offline Mode")
        mode_lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #10B981; background-color: #1A382B; padding: 4px 10px; border-radius: 6px;")

        tb_layout.addWidget(self.mentor_status_lbl)
        tb_layout.addStretch()
        tb_layout.addWidget(mode_lbl)

        content_layout.addWidget(top_bar)

        # Stacked Views Widget
        self.stack = QStackedWidget()

        # Page 0: Login View
        self.login_view = LoginScreen()
        self.login_view.login_successful.connect(self._on_login_success)

        # Page 1: Dashboard View
        self.dashboard_view = DashboardView()
        self.dashboard_view.preview_requested.connect(self._on_preview_requested)

        # Page 2: Preview View
        self.preview_view = PreviewView()

        # Page 3: Settings View
        self.settings_view = SettingsView()

        self.stack.addWidget(self.login_view)      # index 0
        self.stack.addWidget(self.dashboard_view)  # index 1
        self.stack.addWidget(self.preview_view)    # index 2
        self.stack.addWidget(self.settings_view)   # index 3

        content_layout.addWidget(self.stack)

        main_layout.addWidget(content_container)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("background-color: #0F172A; color: #94A3B8; font-size: 11px;")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. Select a Google Forms CSV file to start.")

        # Hide sidebar initially until login
        self.sidebar.setVisible(False)
        self.stack.setCurrentIndex(0)

    def _on_login_success(self, mentor_name: str):
        self.current_mentor = mentor_name
        self.mentor_status_lbl.setText(f"Logged in as: {mentor_name}")
        self.sidebar.setVisible(True)
        self.stack.setCurrentIndex(1)  # Show Dashboard
        self.status_bar.showMessage(f"Welcome, {mentor_name}! Dashboard ready.")

        # Auto-load sample dataset if available for immediate convenience
        sample_path = os.path.abspath("sample_data/sample_students.csv")
        sample_photos = os.path.abspath("sample_data/sample_photos")
        if os.path.exists(sample_path):
            self.dashboard_view.set_sample_csv(sample_path)
            if os.path.exists(sample_photos):
                self.dashboard_view.image_folder = sample_photos

    def switch_view(self, view_index: int):
        """
        Switches stacked pages: 0: Dashboard, 1: Preview, 2: Settings
        """
        # Map view_index to stack index (0 is login view)
        target_stack_idx = view_index + 1
        self.stack.setCurrentIndex(target_stack_idx)

        # Update button highlights
        self.btn_dashboard.setStyleSheet("background-color: #4F46E5; color: white;" if view_index == 0 else "")
        self.btn_preview.setStyleSheet("background-color: #4F46E5; color: white;" if view_index == 1 else "")
        self.btn_settings.setStyleSheet("background-color: #4F46E5; color: white;" if view_index == 2 else "")

    def _on_preview_requested(self, students: list):
        self.preview_view.set_students(students)
        self.switch_view(1)  # Jump to Preview View

    def _open_ai_dialog(self):
        dialog = AIAssistantDialog(self)
        dialog.exec()

    def _handle_logout(self):
        reply = QMessageBox.question(self, "Logout Confirmation", "Are you sure you want to log out?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sidebar.setVisible(False)
            self.stack.setCurrentIndex(0)  # Show Login Screen
            self.status_bar.showMessage("Logged out.")
