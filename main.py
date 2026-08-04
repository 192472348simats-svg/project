import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont

from ui.main_window import MainWindow
from templates.template_builder import build_default_template


def main():
    """
    Application Entry Point for Mentor Report Generator desktop application.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("AI-Assisted Mentor Report Generator")
    app.setOrganizationName("College Academic Suites")

    # Ensure default template exists
    template_path = os.path.abspath("templates/mentor_template.pptx")
    if not os.path.exists(template_path):
        try:
            build_default_template(template_path)
        except Exception as e:
            print(f"Notice: Could not pre-build template file: {e}")

    # Load QSS Stylesheet
    qss_path = os.path.abspath("assets/styles.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
