# skills-copilot-codespaces-vscode

Basic automation script for visa agencies.

## Usage

```bash
python visa_automation.py input.csv output.csv
```

### Expected input columns

- `applicant_name`
- `appointment_date` (`YYYY-MM-DD`)
- `documents_submitted` (semicolon-separated list)

The script writes `missing_documents` and `action` columns to the output CSV.
