import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QFrame, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, QSettings


class SettingsView(QWidget):
    """
    Settings screen for configuring application export paths, default directories,
    and PDF generation options. Persists via QSettings so the chosen defaults
    (especially the mentor's PowerPoint template) are actually picked up by the
    Dashboard on next launch, instead of silently going nowhere.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.qsettings = QSettings()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_lbl = QLabel("APPLICATION SETTINGS")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #818CF8;")
        layout.addWidget(title_lbl)

        # Settings Card
        card = QFrame()
        card.setStyleSheet("background-color: #1E293B; border-radius: 12px; padding: 20px;")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)

        # Export Path
        l1 = QLabel("Default Export Directory:")
        l1.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        h1 = QHBoxLayout()
        saved_export_dir = self.qsettings.value("export_dir", os.path.abspath("exports"), type=str)
        self.export_path_input = QLineEdit(saved_export_dir)
        btn1 = QPushButton("Browse...")
        btn1.setStyleSheet("background-color: #334155; color: white; padding: 6px 14px; border-radius: 6px;")
        btn1.clicked.connect(self._browse_export)
        h1.addWidget(self.export_path_input)
        h1.addWidget(btn1)

        card_layout.addWidget(l1)
        card_layout.addLayout(h1)

        # Template Path
        l2 = QLabel("Default PowerPoint Template Path (.pptx):")
        l2.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        h2 = QHBoxLayout()
        default_tpl = os.path.abspath("templates/mentor_template.pptx")
        saved_tpl = self.qsettings.value("template_path", default_tpl, type=str)
        self.template_path_input = QLineEdit(saved_tpl)
        btn2 = QPushButton("Browse...")
        btn2.setStyleSheet("background-color: #334155; color: white; padding: 6px 14px; border-radius: 6px;")
        btn2.clicked.connect(self._browse_template)
        h2.addWidget(self.template_path_input)
        h2.addWidget(btn2)

        card_layout.addWidget(l2)
        card_layout.addLayout(h2)

        # PDF Export Checkbox
        saved_pdf_enabled = self.qsettings.value("pdf_export_enabled", True, type=bool)
        self.pdf_chk = QCheckBox("Enable Windows PowerPoint PDF Conversion (Requires Microsoft PowerPoint COM)")
        self.pdf_chk.setChecked(saved_pdf_enabled)
        self.pdf_chk.setStyleSheet("color: #F8FAFC; font-weight: 600;")
        card_layout.addWidget(self.pdf_chk)

        # Offline Enforcement Badge
        offline_lbl = QLabel("🔒 Core Application Mode: 100% Offline (Local Data Processing Enforced)")
        offline_lbl.setStyleSheet("color: #10B981; font-weight: bold; padding: 10px 0;")
        card_layout.addWidget(offline_lbl)

        # Save Button
        save_btn = QPushButton("SAVE SETTINGS")
        save_btn.setStyleSheet("background-color: #4F46E5; color: white; font-weight: bold; padding: 10px 20px; border-radius: 8px;")
        save_btn.clicked.connect(self._save_settings)
        card_layout.addWidget(save_btn)

        layout.addWidget(card)
        layout.addStretch()

    def _browse_export(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if folder:
            self.export_path_input.setText(folder)

    def _browse_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PPTX Template", "", "PowerPoint (*.pptx)")
        if file_path:
            self.template_path_input.setText(file_path)

    def _save_settings(self):
        self.qsettings.setValue("export_dir", self.export_path_input.text().strip())
        self.qsettings.setValue("template_path", self.template_path_input.text().strip())
        self.qsettings.setValue("pdf_export_enabled", self.pdf_chk.isChecked())
        self.qsettings.sync()
        QMessageBox.information(
            self,
            "Settings Saved",
            "Application settings have been updated successfully.\n\n"
            "Your default template will now be pre-selected on the Dashboard "
            "(you can still override it per-run from the Dashboard's own "
            "template picker)."
        )