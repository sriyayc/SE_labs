# Lab 5 Issues Found and Fixed

Name: Sriya
SRN: PES2UG24CS523
File: tower_maintenance.py

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (B608) | Security (Bandit, Medium) | 11 | The INSERT query was built using `%` string formatting, so a site name with a quote could change the query | Used a parameterised query with `?` placeholders |
| Unsafe pickle (B301, B403) | Security (Bandit, Medium/Low) | 1, 43 | `pickle.loads` was used only to copy the rows. Pickle can run code if it ever loads untrusted data | Removed pickle and used `list(...)` to copy the rows |
| Hardcoded password (B105) | Security (Bandit, Low) | 6 | NOC password was written directly in the code | Read it from the `NOC_PASSWORD` environment variable |
| Broad exception (W0718) | Bug (Pylint) | 20 | `except Exception` hides every error, even real bugs | Catch only `sqlite3.Error` |
| Global statement (W0603) | Code quality (Pylint) | 16 | `global service_count` was used to change the counter | Kept the count in a `STATS` dict so no `global` is needed |
| Naming style (C0103) | Style (Pylint) | 10, 15, 34 | `addTower`, `serviceTower`, `riskLevel` were camelCase | Renamed to `add_tower`, `service_tower`, `risk_level` |
| Missing docstrings (C0114, C0116) | Style (Pylint) | 1 and all functions | No module or function docstrings | Added docstrings |
| Unnecessary else (R1705) | Style (Pylint) | 36 | `else` after `return` | Removed the else |
| Crash on missing tower | Bug (found while fixing) | 35 | `risk_level` did `row[0]` even when no tower matched, which crashes with TypeError | Return `"unknown"` when the row is None |
| Service not committed | Bug (found while fixing) | 18 | The UPDATE in `service_tower` was never committed | Added `conn.commit()` |
| main() runs on import | Code quality | 54 | `main()` ran whenever the file was imported | Wrapped it in `if __name__ == "__main__":` |
| Long lines (E501, C0301) | Style (Flake8, Pylint) | 5, 11, 18, 35, 43 | Lines longer than 79 characters | Split the SQL strings over two lines |
| Blank lines (E303) | Style (Flake8) | 25 | 3 blank lines before a function | Reduced to 2 |
| Missing whitespace (E225) | Style (Flake8) | 50 | `total=len(...)` | Changed to `total = len(...)` |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.14/10 | 10.00/10 |
| Bandit | 4 issues (2 Medium, 2 Low) | No issues |
| Flake8 | 7 issues | 0 issues |

The program still prints the same output: `['Ridge-A'] high 2 1`
