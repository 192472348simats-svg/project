import os
import sys
import traceback
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QFileDialog, QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QProgressBar, QSplitter
)
from PySide6.QtCore import Qt, Signal, QThread, QSettings
from PySide6.QtGui import QColor

from core.csv_loader import CSVLoader
from core.validator import DataValidator, ValidationResult
from core.analytics import AnalyticsEngine, StudentAnalytics
from core.ppt_generator import PPTReportGenerator, PPTGenerationError


class CSVLoadWorker(QThread):
    """
    Background worker thread for reading and parsing student CSV files off the main UI thread.
    """
    progress = Signal(str)
    finished = Signal(list, list, object, list)  # records, analytics_list, val_result, warnings
    error = Signal(str, str)

    def __init__(self, csv_path: str):
        super().__init__()
        self.csv_path = csv_path

    def run(self):
        try:
            self.progress.emit("Loading CSV dataset...")
            loader = CSVLoader(self.csv_path)
            records, warnings = loader.load_csv()

            self.progress.emit("Validating student data...")
            val_result = DataValidator.validate(records)

            self.progress.emit("Calculating student analytics...")
            analytics_list = [AnalyticsEngine.analyze_student(r) for r in val_result.valid_records]

            self.finished.emit(records, analytics_list, val_result, warnings)
        except Exception as e:
            tb_str = traceback.format_exc()
            print("\n" + "="*80, file=sys.stderr)
            print("CSV LOADING ERROR DETECTED:", file=sys.stderr)
            print(tb_str, file=sys.stderr)
            print("="*80 + "\n", file=sys.stderr)
            self.error.emit(str(e), tb_str)


class GenerationThread(QThread):
    """
    Background worker thread for PPT generation to keep GUI smooth and responsive.
    """
    progress = Signal(int, int, str)
    finished = Signal(dict)
    error = Signal(str, str)  # formatted_msg, raw_traceback

    def __init__(self, analytics_list, student_records, export_dir, template_path, image_folder, recent_events, mentor_name, mentor_phone):
        super().__init__()
        self.analytics_list = analytics_list
        self.student_records = student_records
        self.export_dir = export_dir
        self.template_path = template_path
        self.image_folder = image_folder
        self.recent_events = recent_events
        self.mentor_name = mentor_name
        self.mentor_phone = mentor_phone

    def run(self):
        try:
            generator = PPTReportGenerator(
                template_path=self.template_path,
                image_folder=self.image_folder,
                recent_events=self.recent_events,
                mentor_name=self.mentor_name,
                mentor_phone=self.mentor_phone
            )
            results = generator.generate_all_reports(
                self.analytics_list,
                self.export_dir,
                student_records=self.student_records,
                progress_callback=lambda current, total, msg: self.progress.emit(current, total, msg)
            )
            self.finished.emit(results)
        except PPTGenerationError as e:
            tb_str = e.traceback_str or traceback.format_exc()
            self.error.emit(str(e), tb_str)
        except Exception as e:
            tb_str = traceback.format_exc()
            print("\n" + "="*80, file=sys.stderr)
            print("UNHANDLED GENERATION WORKER EXCEPTION:", file=sys.stderr)
            print(tb_str, file=sys.stderr)
            print("="*80 + "\n", file=sys.stderr)
            formatted_msg = (
                f"PowerPoint Generation Failed\n\n"
                f"File:\nppt_generator.py\n\n"
                f"Function:\ngenerate_all_reports()\n\n"
                f"Reason:\n{str(e)}"
            )
            self.error.emit(formatted_msg, tb_str)


class DashboardView(QWidget):
    """
    Main Dashboard view featuring file pickers, recent events editor, validation report,
    summary analytics, and report generation triggers.
    """
    preview_requested = Signal(list)  # Emits list of StudentAnalytics objects

    def __init__(self, parent=None):
        super().__init__(parent)
        self.csv_path = ""

        # Pull the mentor's saved default template/export dir from Settings,
        # if one was ever saved there - previously Settings and Dashboard
        # never shared state, so a template chosen in Settings was silently
        # ignored at generation time.
        self.qsettings = QSettings()
        saved_template = self.qsettings.value("template_path", "", type=str)
        self.template_path = saved_template if (saved_template and os.path.exists(saved_template)) else ""

        self.image_folder = ""
        self.export_dir = self.qsettings.value("export_dir", os.path.abspath("exports"), type=str)

        self.records = []
        self.analytics_list = []
        self.validation_result = None

        self._init_ui()

        # Reflect the pre-loaded default template (if any) in the picker card,
        # so the mentor can see at a glance which template will actually be used.
        if self.template_path:
            self.template_card.path_label.setText(os.path.basename(self.template_path))

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Title Banner
        header_layout = QHBoxLayout()
        title_lbl = QLabel("MENTOR REPORT GENERATOR (NEW.PPTX REPLICATION ENGINE)")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #818CF8;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # -------------------------------------------------------------
        # FILE SELECTION & RECENT EVENTS ROW
        # -------------------------------------------------------------
        file_cards_layout = QHBoxLayout()
        file_cards_layout.setSpacing(12)

        # CSV Picker Card
        self.csv_card = self._create_file_picker_card(
            "1. Google Forms CSV", "Select student CSV dataset...", "Browse CSV", self._browse_csv
        )
        # Template Picker Card
        self.template_card = self._create_file_picker_card(
            "2. PowerPoint Template (.pptx)", "NEW.pptx format template...", "Browse Template", self._browse_template
        )
        # Image Folder Picker Card
        self.image_card = self._create_file_picker_card(
            "3. Student Photos Folder", "Select photos directory...", "Browse Folder", self._browse_image_folder
        )

        file_cards_layout.addWidget(self.csv_card)
        file_cards_layout.addWidget(self.template_card)
        file_cards_layout.addWidget(self.image_card)
        layout.addLayout(file_cards_layout)

        # Recent Events & Mentor Info Editor Frame
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 12px;")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(15)

        l_ev = QLabel("Recent Institutional Events:")
        l_ev.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        self.events_input = QLineEdit("SIMMAM 2026")
        self.events_input.setToolTip("e.g. SIMMAM 2026, College Cultural Festival")

        l_mname = QLabel("Mentor Name:")
        l_mname.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        self.mname_input = QLineEdit("Dr. T. Kumaragurubaran")

        l_mphone = QLabel("Mentor Phone:")
        l_mphone.setStyleSheet("font-weight: bold; color: #C7D2FE;")
        self.mphone_input = QLineEdit("7373032383")

        info_layout.addWidget(l_ev)
        info_layout.addWidget(self.events_input)
        info_layout.addWidget(l_mname)
        info_layout.addWidget(self.mname_input)
        info_layout.addWidget(l_mphone)
        info_layout.addWidget(self.mphone_input)

        layout.addWidget(info_frame)

        # -------------------------------------------------------------
        # SUMMARY METRICS CARDS ROW
        # -------------------------------------------------------------
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(12)

        self.card_total = self._create_metric_card("Total Students", "0", "Records Loaded")
        self.card_avg_att = self._create_metric_card("Avg Attendance", "0.0%", "Cohort Mean")
        self.card_high_risk = self._create_metric_card("High/Critical Risk", "0", "Intervention Needed")
        self.card_backlogs = self._create_metric_card("Arrears Students", "0", "Backlogs Recorded")

        metrics_layout.addWidget(self.card_total["frame"])
        metrics_layout.addWidget(self.card_avg_att["frame"])
        metrics_layout.addWidget(self.card_high_risk["frame"])
        metrics_layout.addWidget(self.card_backlogs["frame"])
        layout.addLayout(metrics_layout)

        # -------------------------------------------------------------
        # DATA TABLE & CONTROL BUTTONS
        # -------------------------------------------------------------
        table_frame = QFrame()
        table_frame.setStyleSheet("background-color: #1E293B; border-radius: 10px; padding: 10px;")
        tf_layout = QVBoxLayout(table_frame)

        action_layout = QHBoxLayout()
        
        self.validate_btn = QPushButton("VALIDATE CSV DATA")
        self.validate_btn.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        self.validate_btn.clicked.connect(self._validate_csv)

        self.preview_btn = QPushButton("PREVIEW FIRST STUDENT")
        self.preview_btn.setStyleSheet("background-color: #6366F1; color: white; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        self.preview_btn.clicked.connect(self._trigger_preview)
        self.preview_btn.setEnabled(False)

        self.generate_btn = QPushButton("GENERATE ALL PPT REPORTS")
        self.generate_btn.setStyleSheet("background-color: #059669; color: white; font-weight: bold; padding: 8px 20px; border-radius: 6px;")
        self.generate_btn.clicked.connect(self._generate_reports)
        self.generate_btn.setEnabled(False)

        action_layout.addWidget(self.validate_btn)
        action_layout.addWidget(self.preview_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.generate_btn)

        tf_layout.addLayout(action_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Reg No", "Student Name", "Dept", "Overall Att %", "Arrears", "Risk Level", "Academic Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tf_layout.addWidget(self.table)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 5px;
                text-align: center;
                background-color: #0F172A;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #10B981;
            }
        """)
        tf_layout.addWidget(self.progress_bar)

        layout.addWidget(table_frame)

    def _create_file_picker_card(self, title: str, placeholder: str, btn_text: str, callback):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 10px;")
        l = QVBoxLayout(frame)

        lbl = QLabel(title)
        lbl.setStyleSheet("font-weight: bold; color: #C7D2FE;")

        path_lbl = QLabel(placeholder)
        path_lbl.setStyleSheet("color: #94A3B8; font-size: 11px;")
        path_lbl.setWordWrap(True)

        btn = QPushButton(btn_text)
        btn.setStyleSheet("background-color: #334155; color: white; border-radius: 6px; padding: 6px;")
        btn.clicked.connect(callback)

        l.addWidget(lbl)
        l.addWidget(path_lbl)
        l.addWidget(btn)

        frame.path_label = path_lbl
        frame.btn = btn
        return frame

    def _create_metric_card(self, title: str, value: str, subtext: str):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 12px;")
        l = QVBoxLayout(frame)

        lbl = QLabel(title.upper())
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #94A3B8;")

        val_lbl = QLabel(value)
        val_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #818CF8;")

        sub_lbl = QLabel(subtext)
        sub_lbl.setStyleSheet("font-size: 11px; color: #64748B;")

        l.addWidget(lbl)
        l.addWidget(val_lbl)
        l.addWidget(sub_lbl)

        return {"frame": frame, "val_lbl": val_lbl}

    def _set_ui_enabled(self, enabled: bool):
        """
        Disables UI controls during async operations to prevent duplicate clicks.
        """
        self.csv_card.btn.setEnabled(enabled)
        self.template_card.btn.setEnabled(enabled)
        self.image_card.btn.setEnabled(enabled)
        self.validate_btn.setEnabled(enabled)
        self.events_input.setEnabled(enabled)
        self.mname_input.setEnabled(enabled)
        self.mphone_input.setEnabled(enabled)

        if enabled:
            has_data = len(self.analytics_list) > 0
            self.generate_btn.setEnabled(has_data)
            self.preview_btn.setEnabled(has_data)
        else:
            self.generate_btn.setEnabled(False)
            self.preview_btn.setEnabled(False)

    def _browse_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Google Forms CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_path = file_path
            self.csv_card.path_label.setText(os.path.basename(file_path))
            self._load_and_preview_csv()

    def _browse_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PowerPoint Template", "", "PowerPoint (*.pptx)")
        if file_path:
            self.template_path = file_path
            self.template_card.path_label.setText(os.path.basename(file_path))

    def _browse_image_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Student Photos Folder")
        if folder_path:
            self.image_folder = folder_path
            self.image_card.path_label.setText(os.path.basename(folder_path))

    def set_sample_csv(self, file_path: str):
        self.csv_path = file_path
        self.csv_card.path_label.setText(os.path.basename(file_path))
        self._load_and_preview_csv()

    def _load_and_preview_csv(self):
        if not self.csv_path:
            return

        self._set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Loading CSV dataset...")

        self.csv_worker = CSVLoadWorker(self.csv_path)
        self.csv_worker.progress.connect(lambda msg: self.progress_bar.setFormat(f"{msg}..."))
        self.csv_worker.finished.connect(self._on_csv_loaded)
        self.csv_worker.error.connect(self._on_csv_load_error)
        self.csv_worker.start()

    def _on_csv_loaded(self, records, analytics_list, val_result, warnings):
        self.records = records
        self.analytics_list = analytics_list
        self.validation_result = val_result

        self._update_table_and_metrics()
        self.progress_bar.setVisible(False)
        self._set_ui_enabled(True)

        if warnings:
            msg = "\n".join(warnings[:5])
            QMessageBox.information(self, "CSV Mapping Notice", f"CSV Header Mapping Warnings:\n{msg}")

        if val_result and val_result.errors:
            err_msg = "\n".join(val_result.errors[:4])
            QMessageBox.warning(self, "Validation Warnings", f"Validation errors found in records:\n{err_msg}")

    def _on_csv_load_error(self, err_msg, tb_str):
        self.progress_bar.setVisible(False)
        self._set_ui_enabled(True)
        QMessageBox.critical(self, "Error Loading CSV", f"Could not parse CSV file:\n{err_msg}")

    def _validate_csv(self):
        if not self.csv_path:
            QMessageBox.warning(self, "No CSV Selected", "Please select a valid CSV dataset first.")
            return

        self._load_and_preview_csv()

    def _update_table_and_metrics(self):
        self.table.setRowCount(len(self.analytics_list))
        for row, a in enumerate(self.analytics_list):
            self.table.setItem(row, 0, QTableWidgetItem(a.reg_no))
            self.table.setItem(row, 1, QTableWidgetItem(a.name))
            self.table.setItem(row, 2, QTableWidgetItem(a.department))
            self.table.setItem(row, 3, QTableWidgetItem(f"{a.overall_attendance:.1f}%"))
            self.table.setItem(row, 4, QTableWidgetItem(str(a.arrears)))

            risk_item = QTableWidgetItem(a.risk_level)
            if a.risk_level in ["Critical", "High"]:
                risk_item.setForeground(QColor("#EF4444"))
            elif a.risk_level == "Medium":
                risk_item.setForeground(QColor("#F59E0B"))
            else:
                risk_item.setForeground(QColor("#10B981"))
            self.table.setItem(row, 5, risk_item)

            self.table.setItem(row, 6, QTableWidgetItem(a.academic_status))

        total = len(self.analytics_list)
        avg_att = (sum(a.overall_attendance for a in self.analytics_list) / total) if total > 0 else 0.0
        high_risk_count = sum(1 for a in self.analytics_list if a.risk_level in ["High", "Critical"])
        arrear_count = sum(1 for a in self.analytics_list if a.arrears > 0)

        self.card_total["val_lbl"].setText(str(total))
        self.card_avg_att["val_lbl"].setText(f"{avg_att:.1f}%")
        self.card_high_risk["val_lbl"].setText(str(high_risk_count))
        self.card_backlogs["val_lbl"].setText(str(arrear_count))

    def _trigger_preview(self):
        if self.analytics_list:
            self.preview_requested.emit(self.analytics_list)

    def _generate_reports(self):
        if not self.analytics_list:
            QMessageBox.warning(self, "No Data", "Please load a valid student CSV dataset first.")
            return

        self._set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Reading Template... (0%)")

        recent_events = self.events_input.text().strip() or "SIMMAM 2026"
        mentor_name = self.mname_input.text().strip() or "Dr. T. Kumaragurubaran"
        mentor_phone = self.mphone_input.text().strip() or "7373032383"

        self.thread = GenerationThread(
            self.analytics_list,
            self.records,
            self.export_dir,
            self.template_path,
            self.image_folder,
            recent_events,
            mentor_name,
            mentor_phone
        )
        self.thread.progress.connect(self._on_progress)
        self.thread.finished.connect(self._on_generation_finished)
        self.thread.error.connect(self._on_generation_error)
        self.thread.start()

    def _on_progress(self, current, total, msg):
        pct = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(pct)
        self.progress_bar.setFormat(f"{msg} ({pct}%)")

    def _on_generation_finished(self, results):
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("Export Complete (100%)")
        self.progress_bar.setVisible(False)
        self._set_ui_enabled(True)

        combined_path = results["combined_ppt"]
        count = results["total_generated"]

        msg = f"Successfully generated {count} individual student reports and combined cohort presentation matching NEW.pptx!\n\nLocation:\n{combined_path}"
        QMessageBox.information(self, "Reports Generated Successfully", msg)

    def _on_generation_error(self, err_msg, tb_str):
        self.progress_bar.setVisible(False)
        self._set_ui_enabled(True)
        print("\n" + "="*80, file=sys.stderr)
        print("FULL POWERPOINT GENERATION TRACEBACK:", file=sys.stderr)
        print(tb_str, file=sys.stderr)
        print("="*80 + "\n", file=sys.stderr)

        QMessageBox.critical(self, "PowerPoint Generation Failed", err_msg)