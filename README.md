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
3. **Install Dependencies**
   Install required Python packages with pip:
    ```bash
       pip install -r requirements.txt

4. **Configure Data Files**

- The project includes dummy lead data for testing purposes.

- You can replace or extend the default `keywords.json` and `icp_config.json` to customize the filtering criteria.

5. **Run the Script**

- Run the main Python script to start processing the leads:

  ```bash
  python lead_qualification.py

---

## 🧰 Tech Stack Used
- Python – Programming language used for the automation logic

- JSON – For input/output data formats

---

## 📌 Assumptions and Limitations

- **Keyword logic** supports both `AND` and `OR` conditions as defined in a JSON configuration file (`keywords.json`).
- **ICP matching** is based on configurable role keywords (e.g., "Head of Growth", "Marketing", etc.) and can be modified in the `icp_config.json`.
- Leads must match **at least one keyword AND one ICP role** to be considered valid for scoring and filtering.
- **Confidence scoring** is computed using the following logic:
  - +0.2 for keyword match
  - +0.3 for ICP match
  - +0.1 for lead engagement (e.g., likes, comments)
  - Capped at 1.0
- **Deduplication** is done via the `lead_url` field to ensure unique entries in the final outputs.
- **Date of extraction** is appended to each result for tracking and auditing purposes.
- **Engagement data** (e.g., likes, comments) is optional but improves the accuracy of scoring.
- Dummy data is used for testing, but the system is designed to work with real-time sources (e.g., web scraping or API integration).
- **JSON** is used for input and output.

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

