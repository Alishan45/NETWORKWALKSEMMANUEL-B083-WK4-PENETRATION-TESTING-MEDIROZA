#!/usr/bin/env python3
"""
Mediroza General Hospital - Milestone 3: Database Dump Analysis & Intelligence Extraction
Author: Ali Shan (Batch B083)
Mentor: Waqas Karim CCIE - Networkwalks Academy
"""

import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SQL_FILE = os.path.join(BASE_DIR, "targets", "mediroza_db_backup_2019.sql")
OUTPUT_DIR = os.path.join(BASE_DIR, "targets")

print("[*] Initiating Milestone 3 - Critical Data Exposure Parsing")
print(f"[*] Reading Database Backup: {SQL_FILE}")

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

def extract_insert_rows(table_name):
    needle = f"INSERT INTO `{table_name}`"
    start = sql_text.find(needle)
    if start == -1:
        return []
    val_idx = sql_text.find("VALUES", start)
    end_idx = sql_text.find(";\n", val_idx)
    vals_str = sql_text[val_idx + len("VALUES"):end_idx].strip()
    
    rows = []
    for line in vals_str.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove leading '(' and trailing '),' or ');'
        if line.startswith("("):
            line = line[1:]
        if line.endswith(";"):
            line = line[:-1]
        if line.endswith(")"):
            line = line[:-1]
        elif line.endswith("),"):
            line = line[:-2]
        
        parsed = list(csv.reader([line], quotechar="'", skipinitialspace=True))[0]
        rows.append([c.strip() for c in parsed])
    return rows

# 1. Parse Staff Table
print("\n[+] --- Extracting Hospital Staff & Executive Salaries ---")
staff_records = extract_insert_rows("staff")

staff_csv_path = os.path.join(OUTPUT_DIR, "hospital_staff_salaries.csv")
with open(staff_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Full Name", "Job Title", "Department", "Email", "Phone", "National ID", "Monthly Salary (ZAR)", "Date Joined"])
    total_salary = 0
    for s in staff_records:
        writer.writerow(s)
        total_salary += int(s[7])
        print(f"    - ID {s[0]:>2}: {s[1]:<28} | {s[2]:<26} | {s[3]:<18} | ZAR {int(s[7]):>8,}")

print(f"\n[+] Total Hospital Staff Count: {len(staff_records)} Employees")
print(f"[+] Total Monthly Payroll Expenditure: ZAR {total_salary:,} (~ZAR {total_salary * 12:,} / annum)")
print(f"[+] Exported to: {staff_csv_path}")

# 2. Parse Shareholders Table
print("\n[+] --- Extracting Hospital Shareholders & Equity Holdings ---")
sh_records = extract_insert_rows("shareholders")

sh_csv_path = os.path.join(OUTPUT_DIR, "hospital_shareholders.csv")
with open(sh_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Shareholder Name", "Share Percent (%)", "Shares Held", "Share Class"])
    total_pct = 0.0
    total_shares = 0
    for s in sh_records:
        writer.writerow(s)
        total_pct += float(s[2])
        total_shares += int(s[3])
        print(f"    - ID {s[0]:>2}: {s[1]:<35} | {s[2]:>5}% | {int(s[3]):>8,} Shares | Class: {s[4]}")

print(f"\n[+] Total Shareholders Identified: {len(sh_records)}")
print(f"[+] Total Capitalization: {total_shares:,} shares ({total_pct:.1f}%)")
print(f"[+] Exported to: {sh_csv_path}")
print("\n[+] Milestone 3 Complete. High-impact financial and executive data fully documented.")
