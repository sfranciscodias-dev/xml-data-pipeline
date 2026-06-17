# 📊 Automated Tax Document (NF-e) ETL & Auditing Pipeline

**Disclaimer:** *This repository contains a simplified "showcase" version of an ETL pipeline. The full production code contains proprietary business logic and is securely maintained in a private environment.*

## 🎯 Project Overview
This project demonstrates the core architecture of an automated ETL (Extract, Transform, Load) pipeline built with Python. It was designed to solve bottlenecks in financial and tax auditing by replacing manual data entry with an automated, scalable solution that processes complex XML files (Brazilian NF-e standard).

## 🚀 Key Features (Production Architecture)
While this showcase demonstrates the core extraction, the full production version performs advanced business and compliance validations:
* **Tax Compliance Auditing:** Automatically groups invoices by entity (CNPJ) and series to detect missing sequential numbers, preventing compliance risks and tax penalties.
* **Relational Cross-Referencing:** Identifies and links return/cancellation invoices with their original sales documents using advanced Pandas filtering and lambda functions.
* **Multi-level Aggregation:** Generates consolidated financial reports grouped by operation type (CFOP/Natureza da Operação).
* **High-Volume Processing:** Successfully parses, validates, and loads over **5,000 XML files** per month, outputting structured multi-sheet Excel reports.
* Intelligent Data Deduplication: Identifies and isolates duplicate XML files not by their physical filenames, but by parsing the underlying 44-digit Access Key. This acts as a robust data-cleaning layer, ensuring data integrity before the ETL pipeline even begins.

## 🛠️ Technologies Used
* **Python 3:** Core programming language.
* **Pandas:** Advanced data manipulation, grouping (`groupby`), boolean indexing, and aggregation.
* **xml.etree.ElementTree:** For parsing complex and deeply nested XML structures.
* **AI-Assisted Coding:** Developed with the assistance of LLMs for pair programming and code optimization.

## ⚙️ How to Run the Showcase
1. Clone this repository.
2. Run `python etl_showcase.py`. 
3. The script will read the provided `mock_data.xml` and generate a `Relatorio_Showcase.xlsx` file, demonstrating the extraction and structuring of the data.
