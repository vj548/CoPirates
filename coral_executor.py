import subprocess
import json
import re

class CoralExecutor:
    def execute_query(self, sql_query: str) -> dict:
        result = subprocess.run(
            ['coral', 'sql', sql_query],
            capture_output=True,
            text=True
        )
        
        output = result.stdout
        error = result.stderr
        
        # Parse the table output into rows
        rows = []
        lines = output.strip().split('\n')
        
        for line in lines:
            # Skip separator lines like +---+---+
            if line.startswith('+') and line.endswith('+'):
                continue
            # Skip header separators
            if '|' in line and line.strip() and not any(c.isalpha() for c in line.replace('|', '').strip()):
                continue
            # Parse data rows
            if '|' in line and len(line.strip()) > 2:
                # Split by | and clean each cell
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells and any(cells):  # Only add non-empty rows
                    rows.append(cells)
        
        # If we have headers, convert to dict
        if rows:
            # First row might be headers
            first_row = rows[0]
            if len(first_row) > 0:
                result_data = []
                for row in rows[1:]:
                    row_dict = {}
                    for i, cell in enumerate(row):
                        row_dict[f"col_{i}"] = cell
                    result_data.append(row_dict)
                
                return {
                    "row_count": len(result_data),
                    "data": result_data,
                    "raw_output": output
                }
        
        return {"row_count": 0, "data": [], "raw_output": output, "error": error}
