# Mentor Report Generator (AI-Assisted Framework)

A **Windows Desktop Application** built in **Python** using **PySide6** that allows college mentors to generate professional PowerPoint reports from student CSV files exported from Google Forms.

The application operates **100% offline**, ensuring student data privacy while providing deterministic, rule-based analytics, attendance breakdown charts, risk scoring, and automated mentor recommendations.

---

## Key Features

- **100% Offline Core**: All analytics, risk calculations, and report generation take place locally on your computer.
- **Rule-Based Analytics Engine**:
  - Attendance Categories (`Excellent ≥90%`, `Good 75–89%`, `Needs Improvement 60–74%`, `Critical <60%`).
  - Risk Scoring (`Low`, `Medium`, `High`, `Critical`).
  - Academic Standing (`Distinction`, `Regular Standing`, `Academic Probation`, `Academic Warning`).
- **PowerPoint Report Generator**:
  - Produces individual student `.pptx` presentations.
  - Produces a single combined cohort presentation `.pptx`.
  - Embeds high-resolution Matplotlib charts (horizontal subject bar charts & attendance donut charts).
  - Automatically handles student photos or generates custom initials avatars.
- **Interactive GUI**:
  - Built using **PySide6** with custom modern dark/sleek styling.
  - Interactive Preview tab with live risk badges and rule-based recommendation lists.
  - Built-in validation engine reporting missing columns, duplicate register numbers, and out-of-range values.
- **Reserved AI Assistant Module**:
  - Interface stub (`core/ai_assistant.py`) and UI dialog reserved for optional future LLM extension.
  - Strictly prohibited from altering attendance percentages or calculated risk stats.

---

## Tech Stack

- **GUI Framework**: PySide6 (Qt for Python)
- **Data Processing**: pandas
- **Report Generation**: python-pptx
- **Chart Visualizations**: matplotlib
- **Avatar & Image Processing**: Pillow (PIL)
- **PDF Export**: pywin32 (Windows COM)

---

## Installation & Setup

1. **Clone or download the project repository**.
2. **Install Python 3.12+** if not already installed.
3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Launch the desktop GUI by executing:

```bash
python main.py
```

### Quick Start Guide

1. **Login Screen**: Click **Login to Dashboard** (default passcode pre-filled).
2. **Dashboard**:
   - The sample CSV `sample_data/sample_students.csv` is automatically loaded on start.
   - Click **Validate CSV Data** to run integrity checks and compute cohort statistics.
   - Click **Preview First Student** to inspect individual student risk score and rule-based recommendations.
   - Click **Generate All PPT Reports** to export presentations into `exports/`.

---

## Project Structure

```text
MentorReportGenerator/
│
├── main.py                     # Entry point of the PySide6 desktop app
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── ui/                         # User Interface Views
│   ├── main_window.py          # Main window container with sidebar
│   ├── login.py                # Local mentor authentication screen
│   ├── dashboard.py            # Main dashboard, file pickers, metrics & table
│   ├── preview.py              # Interactive student report preview card
│   ├── settings.py             # Export paths & preferences settings
│   └── ai_assistant_dialog.py  # Reserved AI Writing Assistant UI stub
│
├── core/                       # Core Offline Business Logic
│   ├── csv_loader.py           # Flexible CSV parser & header normalizer
│   ├── validator.py            # Data validator for errors & warnings
│   ├── analytics.py            # Rule-based deterministic analytics engine
│   ├── recommendations.py     # Rule-based mentor recommendation generator
│   ├── charts.py               # Matplotlib chart generator (bar & donut charts)
│   ├── image_handler.py        # Photo processor & initials avatar generator
│   ├── ppt_generator.py        # python-pptx slide builder (Individual & Combined)
│   └── ai_assistant.py         # Reserved AI Assistant interface
│
├── templates/
│   └── template_builder.py     # Script to generate default mentor_template.pptx
│
├── sample_data/                # Sample test data
│   └── sample_students.csv     # Pre-configured Google Forms student dataset
│
└── assets/
    └── styles.qss              # Custom Qt style sheet (dark modern theme)
```

---

## Packaging into a Standalone `.exe` (PyInstaller)

To build a single Windows executable (.exe):

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets" --add-data "templates;templates" --add-data "sample_data;sample_data" main.py
```

The compiled standalone application will be generated in the `dist/main` directory.
