import os
import xml.etree.ElementTree as ET
import pandas as pd

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
# XML Namespace configuration standard for Brazilian NF-e
ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

def extract_text(parent_element, tag_path):
    """Helper function to safely extract text from XML tags."""
    if parent_element is None:
        return ""
    found = parent_element.find(tag_path, ns)
    return found.text if found is not None else ""

# ==========================================
# 2. ETL PROCESS: EXTRACTION
# ==========================================
def process_xml_files(folder_path="."):
    print("Starting ETL Process...")
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    
    invoices_data = []

    for file in xml_files:
        try:
            tree = ET.parse(os.path.join(folder_path, file))
            root = tree.getroot()
        except ET.ParseError:
            print(f"Aviso: arquivo inválido ignorado -> {file}")
            continue
        
        infNFe = root.find('.//ns:infNFe', ns)
        if infNFe is None:
            continue
            
        # Extracting key elements
        ide = infNFe.find('ns:ide', ns)
        emit = infNFe.find('ns:emit', ns)
        total = infNFe.find('ns:total/ns:ICMSTot', ns)
        
        # Structuring data
        invoices_data.append({
            'Invoice_Key': (infNFe.get('Id') or "").replace("NFe", ""),
            'Issue_Date': extract_text(ide, 'ns:dhEmi')[:10],
            'Series': int(extract_text(ide, 'ns:serie') or 0),
            'Invoice_Number': int(extract_text(ide, 'ns:nNF') or 0),
            'Issuer_CNPJ': extract_text(emit, 'ns:CNPJ'),
            'Total_Value': float(extract_text(total, 'ns:vNF') or 0),
            'Tax_Value': float(extract_text(total, 'ns:vTotTrib') or 0)
        })
        
    return pd.DataFrame(invoices_data)

# ==========================================
# 3. ETL PROCESS: TRANSFORMATION & LOAD
# ==========================================
if __name__ == "__main__":
    # Extract
    df_invoices = process_xml_files()
    
    if not df_invoices.empty:
        # Transform: Mocking an aggregation by Issuer (Financial Summary)
        df_summary = df_invoices.groupby('Issuer_CNPJ')['Total_Value'].sum().reset_index()
        df_summary.rename(columns={'Total_Value': 'Aggregated_Total'}, inplace=True)
        
        # Load: Export to Excel
        output_file = "Relatorio_Showcase.xlsx"
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_invoices.to_excel(writer, sheet_name='Extracted_Data', index=False)
            df_summary.to_excel(writer, sheet_name='Financial_Summary', index=False)
            
        print(f"Success! Data processed and saved to {output_file}")
    else:
        print("No valid XML files found for processing.")
