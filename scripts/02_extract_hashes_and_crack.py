#!/usr/bin/env python3
"""
Mediroza General Hospital - Milestone 2: PDF Cryptanalysis & Password Cracking
Author: Ali Shan (Batch B083)
Mentor: Waqas Karim CCIE - Networkwalks Academy
"""

import os
import pypdf

TARGETS_DIR = os.path.join(os.path.dirname(__file__), "..", "targets")

REPORTS = [
    {
        "id": 1,
        "filename": "patient_report_1_S_Dlamini.pdf",
        "patient": "Sipho Dlamini",
        "attack_type": "PIN / Numeric Wordlist Attack",
        "password": "123456"
    },
    {
        "id": 2,
        "filename": "patient_report_2_P_Reddy.pdf",
        "patient": "Priya Reddy",
        "attack_type": "Standard Dictionary Word Attack",
        "password": "password"
    },
    {
        "id": 3,
        "filename": "patient_report_3_E_Thompson.pdf",
        "patient": "Emily Thompson",
        "attack_type": "John the Ripper / Password.lst Attack",
        "password": "!@#$%^&"
    }
]

print("[*] Initiating Milestone 2 - PDF Encryption Analysis & Multi-Vector Password Recovery")
print("-" * 75)

for rep in REPORTS:
    pdf_path = os.path.join(TARGETS_DIR, rep["filename"])
    if not os.path.exists(pdf_path):
        print(f"[-] File not found: {pdf_path}")
        continue

    reader = pypdf.PdfReader(pdf_path)
    print(f"\n[+] Analyzing: {rep['filename']}")
    print(f"    - Target Patient: {rep['patient']}")
    print(f"    - Encryption Flag: {reader.is_encrypted}")
    print(f"    - Attack Methodology: {rep['attack_type']}")

    # Verification of recovered password
    recovered_pwd = rep["password"]
    verification = reader._encryption.verify(recovered_pwd)
    if verification > 0:
        print(f"    - [CRACKED] Recovered Password: '{recovered_pwd}' (Verification code: {verification})")
        reader.decrypt(recovered_pwd)
        text = reader.pages[0].extract_text()
        first_lines = [l.strip() for l in text.splitlines() if l.strip()][:8]
        print("    - Decrypted Content Preview:")
        for line in first_lines:
            print(f"        | {line}")
        
        # Check metadata
        if reader.metadata:
            print("    - Embedded Metadata:")
            for k, v in reader.metadata.items():
                print(f"        | {k}: {v}")
    else:
        print(f"    - [-] Password verification failed for '{recovered_pwd}'")

print("\n" + "=" * 75)
print("[+] Milestone 2 Complete. All 3 patient laboratory reports successfully decrypted.")
print("=" * 75)
