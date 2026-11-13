# CipherSchools Semester Student Feedback & Mentor Performance Intelligence

An end-to-end data analysis and executive reporting solution for university semester student feedback surveys, including a single official mentor leaderboard, scoring conversion methodology, statistical verification checks, and an interactive intelligence dashboard.

Repository: [https://github.com/sumitkhodiya/Cipher2.0](https://github.com/sumitkhodiya/Cipher2.0)

---

## Project Structure

```
├── CipherSchools – Student Feedback 1(Sheet3).xlsx   # Raw student feedback survey dataset (N = 238)
├── package.json                                      # Root project manifest (npm start, npm run analyze)
├── Question2/
│   ├── index.html                                    # Standalone executive analytics dashboard
│   ├── data.js                                       # Parsed & structured JSON survey database
│   ├── server.js                                     # Lightweight local Node.js server runner
│   ├── process_data.js                               # Node.js data processing & scoring pipeline
│   ├── analysis_pipeline.py                          # Python data processing & scoring pipeline
│   ├── mentor_leaderboard.csv                        # Official mentor leaderboard export (CSV)
│   ├── section_breakdown.csv                         # Section-level disaggregation export (CSV)
│   ├── package.json                                  # Question2 manifest
│   └── README.md                                     # In-depth Problem 2 executive submission report
└── README.md                                         # Project documentation
```

---

## Reproducing the Analysis & Running the Pipeline

You can re-run the full data extraction, 1-to-5 Likert conversion, audit checks, and scoring calculations at any time:

### Using Node.js:
```bash
npm run analyze
# or: node Question2/process_data.js
```

### Using Python:
```bash
python Question2/analysis_pipeline.py
```

---

## Problem 2 Executive Summary

### 01 Official Mentor Leaderboard (Single Table)
Every student response ($N = 238$) is accounted for and counted **exactly once**:

| Rank | Mentor | Responses ($n$) | Satisfaction (Col G) | Clarity (Col I) | Mentor Rating (Col J) | Engagement (Col K) | Class Quality (Col L) | Overall Score | Reliability Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Mentor E** | 30 | 4.43 | 4.30 | 4.60 | 4.23 | 4.47 | **4.41** (4.4067) | Reliable ($n \ge 15$) |
| **2** | **Mentor H** | 7 | 4.29 | 4.00 | 4.00 | 4.29 | 4.00 | **4.11** (4.1143) | [High Variance] ($n = 7$) |
| **3** | **Mentor B** | 50 | 4.16 | 3.92 | 4.16 | 4.14 | 4.10 | **4.10** (4.0960) | Reliable ($n \ge 15$) |
| **4** | **Mentor F** | 19 | 3.95 | 3.89 | 4.11 | 3.84 | 4.11 | **3.98** (3.9789) | Reliable ($n \ge 15$) |
| **5** | **Mentor C** | 33 | 4.00 | 3.76 | 4.09 | 3.91 | 4.00 | **3.95** (3.9515) | Reliable ($n \ge 15$) |
| **6** | **Mentor G** | 11 | 4.00 | 3.82 | 4.09 | 3.82 | 3.82 | **3.91** (3.9091) | [Low Sample] ($n = 11$) |
| **7** | **Mentor D** | 32 | 3.91 | 3.69 | 4.13 | 3.97 | 3.84 | **3.91** (3.9063) | Reliable ($n \ge 15$) |
| **8** | **Mentor A** | 56 | 3.82 | 3.66 | 3.88 | 3.73 | 3.77 | **3.77** (3.7714) | Reliable ($n \ge 15$) |
| — | **Cohort Benchmark** | **238** | **4.04** | **3.85** | **4.12** | **3.97** | **4.00** | **4.00** (3.9958) | **Program Average** |

---

## 02 Scoring Methodology
* **Scale Conversion:** 5-point Likert scales mapped to discrete integers 1 to 5 (*Extremely Satisfied / Excellent = 5*, down to *Very Dissatisfied / Needs Significant Improvement = 1*).
* **Question Separation:** Syllabus Pace (Col H) and Test Platform (Col M) were separated from mentor scoring as they measure institutional curriculum pacing and external software reliability, respectively.
* **Overall Composite Calculation:** Unweighted arithmetic mean across the five question averages:
  $$\text{Overall Score} = \frac{\text{Avg}(G) + \text{Avg}(I) + \text{Avg}(J) + \text{Avg}(K) + \text{Avg}(L)}{5}$$
* **Fairness Protocol:** Mentors with sample sizes below 15 (Mentor H with 7 and Mentor G with 11) are explicitly flagged for high sample variance.

---

## 03 Verification Checks
* **Total Rows:** 239 total spreadsheet rows (1 header + 238 valid responses).
* **Zero Duplicates:** Exactly 238 unique student IDs.
* **Exhaustive Sum Check:** $56 + 50 + 33 + 32 + 30 + 19 + 11 + 7 = 238$. Every response is counted exactly once.
* **Data Completeness:** Zero blank or unmapped values across all 1,190 evaluation cells.

---

## 04 Key Findings & Strategic Recommendations
* **Strengths:** Strong mentor interpersonal dedication (Cohort average 4.12/5.00). Top-ranked Mentor E (4.41) benchmarked strong hands-on problem practice (LeetCode / Codeforces).
* **Weaknesses:** Explanation clarity scored lowest (3.85/5.00). Mentor A suffered a severe drop in Section 2 (3.61 vs 3.89 in Section 1). 16% reported issues with CodeFri assessment platform stability.
* **Recommendations:**
  1. Optimize the CodeFri secure browser to resolve laptop freezing and screen-sharing issues.
  2. Implement pedagogical coaching for Mentor A (Section 2) focused on live coding and classroom management.
  3. Standardize weekly coding problem sessions bridging exam formats (NeoColab) with practical algorithms.

---

## How to Run the Interactive Dashboard

1. **Option 1 (Node.js Local Server):**
   ```bash
   cd Question2
   node server.js
   ```
   Open `http://localhost:3000` in your web browser.

2. **Option 2 (Direct File Open):**
   Open `Question2/index.html` directly in any modern browser (Chrome, Edge, Firefox, Safari).
