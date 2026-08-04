from typing import List, Dict, Any, Tuple


class ValidationResult:
    """
    Holds the output of CSV validation including valid records, errors, and warnings.
    """
    def __init__(self, valid_records: List[Dict[str, Any]], errors: List[str], warnings: List[str]):
        self.valid_records = valid_records
        self.errors = errors
        self.warnings = warnings
        self.total_records = len(valid_records) + len(errors)
        self.is_valid = len(errors) == 0


class DataValidator:
    """
    Validates CSV student data for missing values, invalid ranges, and duplicates.
    """

    @staticmethod
    def validate(records: List[Dict[str, Any]]) -> ValidationResult:
        valid_records = []
        errors = []
        warnings = []
        seen_reg_nos = set()

        if not records:
            return ValidationResult([], ["The dataset contains no records."], [])

        for idx, rec in enumerate(records):
            row_num = rec.get("row_num", idx + 2)
            row_errors = []

            # 1. Check Register Number
            reg_no = rec.get("reg_no", "").strip()
            if not reg_no or reg_no.startswith("REG_"):
                row_errors.append(f"Row {row_num}: Missing or invalid Register Number.")
            elif reg_no in seen_reg_nos:
                row_errors.append(f"Row {row_num}: Duplicate Register Number '{reg_no}'.")
            else:
                seen_reg_nos.add(reg_no)

            # 2. Check Name
            name = rec.get("name", "").strip()
            if not name or name.startswith("Student_"):
                warnings.append(f"Row {row_num}: Student Name is blank or generic.")

            # 3. Check Overall Attendance Range
            att = rec.get("overall_attendance", 0.0)
            if att < 0.0 or att > 100.0:
                row_errors.append(f"Row {row_num} ({name}): Overall attendance {att}% is out of valid range (0–100%).")

            # 4. Check Subject Attendance
            subject_att = rec.get("subject_attendance", {})
            for subj, sval in subject_att.items():
                if sval < 0.0 or sval > 100.0:
                    warnings.append(f"Row {row_num} ({name}): Subject '{subj}' attendance {sval}% is outside 0–100%.")

            # 5. Check Arrears
            arrears = rec.get("arrears", 0)
            if arrears < 0:
                row_errors.append(f"Row {row_num} ({name}): Arrears count cannot be negative ({arrears}).")

            if row_errors:
                errors.extend(row_errors)
            else:
                valid_records.append(rec)

        return ValidationResult(valid_records, errors, warnings)
