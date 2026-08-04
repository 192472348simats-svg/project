import os
import re
import pandas as pd
from typing import List, Dict, Any, Tuple


class CSVLoader:
    """
    Handles reading and normalizing student CSV files exported from Google Forms.
    """

    # Flexible column mapping rules (case-insensitive substring matching)
    COLUMN_MAPPINGS = {
        "name": ["student name", "name of the student", "full name", "name"],
        "reg_no": ["register number", "reg no", "register no", "reg number", "roll number", "roll no", "reg_no"],
        "department": ["department", "dept", "branch", "course"],
        "overall_attendance": ["overall attendance", "attendance percentage", "attendance (%)", "attendance", "overall_attendance"],
        "subject_attendance": ["subject-wise attendance", "subject attendance", "subject wise attendance", "subject_attendance"],
        "completed_courses": ["number of completed courses", "completed courses", "courses completed", "completed_courses"],
        "arrears": ["number of arrears", "arrears count", "arrears", "no of arrears"],
        "nptel_courses": ["nptel courses", "nptel certifications", "nptel", "nptel_courses"],
        "mentor_remarks": ["mentor remarks", "mentor comments", "remarks", "mentor_remarks"],
        "achievements": ["achievements", "accomplishments", "extra curricular", "achievements"],
        "image_filename": ["image filename", "photo filename", "photo", "image", "image_filename"]
    }

    def __init__(self, file_path: str = ""):
        self.file_path = file_path

    def load_csv(self, file_path: str = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Loads CSV file and returns normalized records list and warning messages.
        """
        path = file_path or self.file_path
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"CSV file not found at path: {path}")

        try:
            # Read CSV with pandas (handles UTF-8, Latin-1 gracefully)
            df = pd.read_csv(path)
        except Exception:
            df = pd.read_csv(path, encoding="latin-1")

        if df.empty:
            raise ValueError("The selected CSV file is empty.")

        warnings = []
        normalized_df, mapping_warnings = self._normalize_columns(df)
        warnings.extend(mapping_warnings)

        records = []
        for index, row in normalized_df.iterrows():
            record = self._clean_record(row, index + 2)  # 1-indexed header is row 1
            records.append(record)

        return records, warnings

    def _normalize_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Maps CSV header names to standardized internal key names.
        """
        warnings = []
        df_cols = [str(col).strip() for col in df.columns]
        column_map = {}

        for internal_key, possible_names in self.COLUMN_MAPPINGS.items():
            found = False
            for col in df_cols:
                col_lower = col.lower()
                for name in possible_names:
                    if name in col_lower:
                        column_map[col] = internal_key
                        found = True
                        break
                if found:
                    break
            if not found:
                if internal_key in ["name", "reg_no"]:
                    warnings.append(f"Critical column mapping missing for '{internal_key}'.")
                else:
                    warnings.append(f"Optional column for '{internal_key}' not automatically mapped.")

        # Rename matched columns
        renamed_df = df.rename(columns=column_map)
        return renamed_df, warnings

    def _clean_record(self, row: pd.Series, row_num: int) -> Dict[str, Any]:
        """
        Cleans and parses a single data row into a standard dictionary.
        """
        def get_val(key, default=""):
            val = row.get(key, default)
            if pd.isna(val) or val is None:
                return default
            return str(val).strip()

        def parse_num(key, default=0.0):
            val = row.get(key, None)
            if pd.isna(val) or val is None:
                return default
            try:
                # Remove % sign or text if present
                clean_str = re.sub(r"[^\d.]", "", str(val))
                return float(clean_str) if clean_str else default
            except Exception:
                return default

        def parse_int(key, default=0):
            return int(parse_num(key, float(default)))

        def parse_subjects(raw_val: str) -> Dict[str, float]:
            """
            Parses strings like "Maths: 85, Physics: 90, Chemistry: 78" or JSON.
            """
            if not raw_val:
                return {}
            
            subjects = {}
            # Try key:val pairs split by comma or semicolon or newline
            pairs = re.split(r"[,;\n]+", raw_val)
            for pair in pairs:
                if ":" in pair:
                    parts = pair.split(":", 1)
                    sname = parts[0].strip()
                    try:
                        sval = float(re.sub(r"[^\d.]", "", parts[1]))
                        if sname:
                            subjects[sname] = sval
                    except Exception:
                        pass
                elif "=" in pair:
                    parts = pair.split("=", 1)
                    sname = parts[0].strip()
                    try:
                        sval = float(re.sub(r"[^\d.]", "", parts[1]))
                        if sname:
                            subjects[sname] = sval
                    except Exception:
                        pass
            return subjects

        name = get_val("name", f"Student_{row_num}")
        reg_no = get_val("reg_no", f"REG_{row_num:03d}")
        department = get_val("department", "General")
        overall_attendance = parse_num("overall_attendance", 0.0)
        completed_courses = parse_int("completed_courses", 0)
        arrears = parse_int("arrears", 0)
        nptel_courses = get_val("nptel_courses", "None")
        mentor_remarks = get_val("mentor_remarks", "No specific remarks provided.")
        achievements = get_val("achievements", "None")
        image_filename = get_val("image_filename", "")

        raw_subject_att = get_val("subject_attendance", "")
        subject_attendance = parse_subjects(raw_subject_att)

        # Fallback if overall attendance is missing but subject attendance exists
        if overall_attendance == 0.0 and subject_attendance:
            overall_attendance = round(sum(subject_attendance.values()) / len(subject_attendance), 1)

        return {
            "row_num": row_num,
            "name": name,
            "reg_no": reg_no,
            "department": department,
            "overall_attendance": overall_attendance,
            "subject_attendance": subject_attendance,
            "completed_courses": completed_courses,
            "arrears": arrears,
            "nptel_courses": nptel_courses,
            "mentor_remarks": mentor_remarks,
            "achievements": achievements,
            "image_filename": image_filename
        }
