import pdfplumber
import re
import json
import os

def parse_pdf(pdf_path, output_json_path=None):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    result_pattern = re.compile(
        r"([А-Яа-яA-Za-z()\- %]+)\s+[A-Z]{1,3}\s+([\d.]+)\s+(\S+)\s+([\d.]+ - [\d.]+)\s+([A-Za-z+.\-]+)"
    )
    section_pattern = re.compile(r"^[А-Яа-я ]{3,}$")

    current_section = None
    results = {}
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if section_pattern.match(line):
            current_section = line.strip()
            if current_section not in results:
                results[current_section] = []
            continue

        match = result_pattern.match(line)
        if match and current_section:
            indicator, value, unit, ref_range, method = match.groups()
            results[current_section].append({
                "indicator": indicator.strip(),
                "value": float(value),
                "unit": unit,
                "reference_range": ref_range,
                "method": method
            })

    results = {section: indicators for section, indicators in results.items() if indicators}

    if output_json_path:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

    return results
