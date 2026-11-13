"""
==============================================================================
Semester Feedback Analysis & Scoring Engine (Python Implementation)
==============================================================================
Processes raw student feedback survey responses, converts 5-point Likert text
options to standardized numeric scores (1-5), executes verification checks,
and outputs the official mentor leaderboard.
==============================================================================
"""

import os
import zipfile
import xml.etree.ElementTree as ET

LIKERT_MAPPING = {
    'G': {  # Satisfaction
        'Extremely Satisfied': 5,
        'Very Satisfied': 4,
        'Satisfied': 3,
        'Dissatisfied': 2,
        'Very Dissatisfied': 1
    },
    'I': {  # Clarity
        'Extremely clear': 5,
        'Very Clear': 4,
        'Moderately Clear': 3,
        'Slightly Clear': 2,
        'Not Clear at All': 1
    },
    'J': {  # Overall Mentor Rating
        'Excellent': 5,
        'Very Good': 4,
        'Good': 3,
        'Needs Improvement': 2,
        'Needs Significant Improvement': 1
    },
    'K': {  # Class Engagement
        'Highly Engaging': 5,
        'Very Engaging': 4,
        'Moderately Engaging': 3,
        'Slightly Engaging': 2,
        'Not Engaging': 1
    },
    'L': {  # Class Quality
        'Excellent': 5,
        'Very Good': 4,
        'Good': 3,
        'Needs Improvement': 2,
        'Needs Significant Improvement': 1
    }
}

def get_score(text, col_map):
    if not text:
        return None
    cleaned = str(text).strip().lower()
    for prefix, score in col_map.items():
        if cleaned.startswith(prefix.lower()):
            return score
    return None

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    xlsx_name = "CipherSchools – Student Feedback 1(Sheet3).xlsx"
    xlsx_path = os.path.join(base_dir, xlsx_name)
    if not os.path.exists(xlsx_path):
        xlsx_path = os.path.join(base_dir, "..", xlsx_name)

    if not os.path.exists(xlsx_path):
        print(f"Error: Dataset file not found at {xlsx_path}")
        return

    print(f"Loading dataset: {xlsx_path}")

    # Read shared strings and worksheet via standard library zipfile
    with zipfile.ZipFile(xlsx_path, 'r') as z:
        # Shared strings
        with z.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            shared_strings = []
            for si in root.findall('.//main:si', ns):
                text_elems = si.findall('.//main:t', ns)
                text = "".join([t.text or "" for t in text_elems])
                shared_strings.append(text)

        # Worksheet
        with z.open('xl/worksheets/sheet1.xml') as f:
            sheet_tree = ET.parse(f)
            sheet_root = sheet_tree.getroot()
            rows_data = []
            for row in sheet_root.findall('.//main:row', ns):
                row_dict = {}
                for c in row.findall('.//main:c', ns):
                    r_attr = c.attrib.get('r', '')
                    col_letter = "".join([ch for ch in r_attr if ch.isalpha()])
                    t_attr = c.attrib.get('t', '')
                    v_elem = c.find('main:v', ns)
                    val = v_elem.text if v_elem is not None else ""
                    if t_attr == 's' and val.isdigit():
                        row_dict[col_letter] = shared_strings[int(val)]
                    else:
                        row_dict[col_letter] = val
                rows_data.append(row_dict)

    data_rows = rows_data[1:]  # skip header
    print(f"Successfully loaded {len(data_rows)} student response records.")

    # Verification
    ids = set()
    duplicates = 0
    for r in data_rows:
        sid = r.get('A')
        if sid in ids:
            duplicates += 1
        ids.add(sid)

    print("\n--- Verification Audit ---")
    print(f"Total Responses : {len(data_rows)}")
    print(f"Unique IDs      : {len(ids)}")
    print(f"Duplicates      : {duplicates}")

    # Aggregate by mentor
    mentors = {}
    for r in data_rows:
        batch = r.get('F', '').strip()
        mentor = batch.split('|')[0].strip() if '|' in batch else batch
        if mentor not in mentors:
            mentors[mentor] = {
                'mentor': mentor, 'n': 0,
                'G': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0
            }
        m = mentors[mentor]
        m['n'] += 1
        m['G'] += get_score(r.get('G'), LIKERT_MAPPING['G'])
        m['I'] += get_score(r.get('I'), LIKERT_MAPPING['I'])
        m['J'] += get_score(r.get('J'), LIKERT_MAPPING['J'])
        m['K'] += get_score(r.get('K'), LIKERT_MAPPING['K'])
        m['L'] += get_score(r.get('L'), LIKERT_MAPPING['L'])

    leaderboard = []
    for m in mentors.values():
        sat = m['G'] / m['n']
        cla = m['I'] / m['n']
        men = m['J'] / m['n']
        eng = m['K'] / m['n']
        qua = m['L'] / m['n']
        total_pts = m['G'] + m['I'] + m['J'] + m['K'] + m['L']
        overall = total_pts / (m['n'] * 5)
        leaderboard.append({
            'mentor': m['mentor'],
            'n': m['n'],
            'sat': sat,
            'cla': cla,
            'men': men,
            'eng': eng,
            'qua': qua,
            'overall': overall,
            'status': '[Reliable]' if m['n'] >= 15 else ('[High Variance]' if m['n'] < 10 else '[Low Sample]')
        })

    leaderboard.sort(key=lambda x: x['overall'], reverse=True)

    print("\n" + "=" * 95)
    print("OFFICIAL MENTOR LEADERBOARD (Problem 2)")
    print("=" * 95)
    print(f"{'Rank':<5} {'Mentor':<10} {'Responses':<10} {'Sat(G)':<8} {'Cla(I)':<8} {'Men(J)':<8} {'Eng(K)':<8} {'Qua(L)':<8} {'Overall':<8} {'Status'}")
    print("-" * 95)
    for idx, m in enumerate(leaderboard, 1):
        print(f"{idx:<5} {m['mentor']:<10} {m['n']:<10} {m['sat']:<8.2f} {m['cla']:<8.2f} {m['men']:<8.2f} {m['eng']:<8.2f} {m['qua']:<8.2f} {m['overall']:<8.2f} {m['status']}")
    print("-" * 95)

if __name__ == "__main__":
    main()
