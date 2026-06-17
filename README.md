# 📊 Automated Tax Document (NF-e) ETL & Auditing Pipeline

> **Disclaimer:** This repository contains a simplified "showcase" version of an ETL pipeline. The full production code contains proprietary business logic and is securely maintained in a private environment.

![Tests](https://github.com/sfranciscodias-dev/xml-data-pipeline/actions/workflows/tests.yml/badge.svg)

---

## 🎯 Project Overview

This project demonstrates the core architecture of an automated ETL (Extract, Transform, Load) pipeline built with Python. It was designed to solve bottlenecks in financial and tax auditing by replacing manual data entry with an automated, scalable solution that processes complex XML files (Brazilian NF-e standard).

---

## 🚀 Key Features (Production Architecture)

While this showcase demonstrates the core extraction, the full production version performs advanced business and compliance validations:

- **Tax Compliance Auditing:** Automatically groups invoices by entity (CNPJ) and series to detect missing sequential numbers, preventing compliance risks and tax penalties.
- **Relational Cross-Referencing:** Identifies and links return/cancellation invoices with their original sales documents using advanced Pandas filtering and lambda functions.
- **Multi-level Aggregation:** Generates consolidated financial reports grouped by operation type (CFOP/Natureza da Operação).
- **High-Volume Processing:** Successfully parses, validates, and loads over 5,000 XML files per month, outputting structured multi-sheet Excel reports.
- **Intelligent Data Deduplication:** Identifies and isolates duplicate XML files not by their physical filenames, but by parsing the underlying 44-digit Access Key — ensuring data integrity before the ETL pipeline even begins.

---

## 🛠️ Technologies Used

- **Python 3.11** — Core programming language
- **Pandas** — Data manipulation, grouping, boolean indexing, and aggregation
- **xml.etree.ElementTree** — Parsing complex and deeply nested XML structures
- **openpyxl** — Multi-sheet Excel report generation
- **pytest** — Automated testing with 4 test cases covering core pipeline logic
- **GitHub Actions** — CI/CD pipeline that runs tests automatically on every commit

---

## 📁 Project Structure

```
xml-data-pipeline/
├── etl_showcase.py          # Main ETL pipeline (Extract, Transform, Load)
├── xml_deduplicator.py      # Deduplication engine based on NF-e Access Key
├── test_etl.py              # Automated tests (pytest)
├── mock_data/
│   ├── mock_nfe_001.xml     # Sample NF-e: Empresa Vitrine Ltda
│   ├── mock_nfe_002.xml     # Sample NF-e: Comercial Exemplo S.A.
│   └── mock_nfe_003_DUPLICATE.xml  # Intentional duplicate for deduplication demo
├── requirements.txt         # Pinned dependencies
└── .github/
    └── workflows/
        └── tests.yml        # GitHub Actions CI workflow
```

---

## ⚙️ How to Run the Showcase

**1. Clone this repository:**
```bash
git clone https://github.com/sfranciscodias-dev/xml-data-pipeline.git
cd xml-data-pipeline
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the ETL pipeline:**
```bash
python etl_showcase.py
```
The script will read the files in `mock_data/` and generate a `Relatorio_Showcase.xlsx` file.

**4. Run the automated tests:**
```bash
pytest test_etl.py -v
```

---

## 🧪 Test Coverage

| Test | Description |
|---|---|
| `test_extract_text_retorna_valor_correto` | Validates correct tag value extraction |
| `test_extract_text_com_elemento_none` | Ensures no crash when element is None |
| `test_extract_text_com_tag_inexistente` | Handles missing tags gracefully |
| `test_process_xml_retorna_dataframe_com_dados` | Full pipeline integration test |
| `test_process_xml_ignora_arquivo_corrompido` | Validates resilience to malformed XML |
