# 🔍 Lead Qualification Automation (Python Version)

This project filters and qualifies leads using predefined criteria, including keyword rules and Ideal Customer Profile (ICP) logic. It deduplicates results and stores high-confidence matches in a structured format with the date of extraction.

> ⚠️ **Note:** Dummy data for leads, keyword rules, and ICP logic is already pre-defined within the provided scripts. You do **not** need to manually create `keywords.json` or `icp_config.json` unless you want to customize them.

---

## ▶️ How to Run It

1. **Set up the Python Environment**  
   Ensure you have Python installed and the necessary dependencies.

2. **Clone the Repository**  
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/CIPHER-000/lead_qualification_automation-python-.git
   cd lead_qualification_automation-python-

3. **Configure Data Files**

- The project includes dummy lead data for testing purposes.

- You can replace or extend the default `keywords.json` and `icp_config.json` to customize the filtering criteria.

4. **Run the Script**

To process the leads, run either of the main Python scripts depending on the type of results you want:

- `keyword_tracker1.py` – generates `all_matched_results.csv` (leads that match any keyword, regardless of ICP)
- `keyword_tracker2.py` – generates `filtered_results.csv` (leads that match both keyword and ICP criteria)

   ```bash
   python keyword_tracker1.py
   python keyword_tracker2.py

---

## 🧰 Tech Stack Used
- Python – Programming language used for the automation logic

- JSON – For input/output data formats

---

## 📌 Assumptions and Limitations

### ✅ Feature Summary

- **Keyword Matching Logic**  
  Keywords are defined in `keywords/keywords.json` and support both `AND` and `OR` logic per rule. Posts must match at least one keyword from any rule to be considered.

- **ICP Role Filtering (Only in `keyword_tracker2.py`)**  
  ICP role terms are loaded from `keywords/icp_config.json`. A lead must match at least one ICP keyword in the username or bio to be included in the filtered results.

- **Scoring Mechanism (Only in `keyword_tracker2.py`)**  
  A confidence score (capped at 1.0) is computed as follows:
  - `+0.2` per unique matched keyword  
  - `+0.3` if the profile matches ICP roles  
  - `+0.1` if likes > 10  
  - `+0.1` if comments > 3  

- **Deduplication**  
  Both scripts use the post URL (`post_url`) to ensure each result is unique and avoid duplicates in the output.

- **Result Metadata**  
  Each result includes a `date_extracted` field (UTC format) to support tracking and audits.

- **Post Engagement Info**  
  Likes and comments are included in the output and optionally influence the confidence score in `keyword_tracker2.py`.

- **Data Source and Format**  
  - Uses `dummy_posts.json` as input for testing.  
  - Outputs JSON files:
    - `all_matched_results.json` (from `keyword_tracker1.py`)  
    - `filtered_results.json` (from `keyword_tracker2.py`)


---

## ✅ Expected Result
- When the script is executed, it will generate two separate output files:

- **all_matched_results.json** – contains all leads that match any of the defined keywords, regardless of ICP match.

- **filtered_results.json** – contains only qualified leads that match both keywords AND ICP criteria, along with confidence scoring and reason.

These outputs help distinguish between general interest leads and highly targeted ones.

---

## 📄 Sample Output

Two sample output files are included for quick review:

- 📁 [`all_matched_results.json`](results/all_matched_results.json)
- 📁 [`filtered_results.json`](results/filtered_results.json)

