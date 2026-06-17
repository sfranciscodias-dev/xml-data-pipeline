import os
import shutil
import xml.etree.ElementTree as ET

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
# XML Namespace configuration standard for Brazilian NF-e
NS = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

def extract_nfe_key(xml_path):
    """
    Parses the XML and extracts the unique 44-digit NF-e Access Key,
    handling standard SEFAZ namespaces.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Attempt 1: Search for <chNFe> tag
        chNFe = root.find('.//nfe:chNFe', NS)
        if chNFe is not None and chNFe.text:
            return chNFe.text.strip()
        
        # Attempt 2: Search for 'Id' attribute in <infNFe> tag
        infNFe = root.find('.//nfe:infNFe', NS)
        if infNFe is not None and 'Id' in infNFe.attrib:
            id_attr = infNFe.attrib['Id']
            return id_attr[3:] if id_attr.startswith('NFe') else id_attr
            
    except Exception:
        return None
    return None

# ==========================================
# 2. DEDUPLICATION PROCESS (DATA CLEANING)
# ==========================================
def run_deduplication(source_folder="."):
    """
    Scans the folder for XML files, identifies duplicates based on the 
    internal Access Key (ignoring filenames), and isolates them.
    """
    duplicates_folder = os.path.join(source_folder, "Duplicated_XMLs")
    
    processed_keys = set()
    valid_count = 0
    duplicate_count = 0

    print("Starting XML deduplication process...")
    
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.xml'):
            full_path = os.path.join(source_folder, filename)
            
            nfe_key = extract_nfe_key(full_path)
            
            if not nfe_key:
                continue
                
            # If the key is already in our set, it's a duplicate document
            if nfe_key in processed_keys:
                os.makedirs(duplicates_folder, exist_ok=True)
                dest_path = os.path.join(duplicates_folder, filename)
                
                # Prevent overwriting if duplicate files have the same name
                if os.path.exists(dest_path):
                    base_name, ext = os.path.splitext(filename)
                    dest_path = os.path.join(duplicates_folder, f"{base_name}_name_conflict{ext}")
                
                shutil.move(full_path, dest_path)
                duplicate_count += 1
            else:
                # First time seeing this key, add to the tracking set
                processed_keys.add(nfe_key)
                valid_count += 1

    print("\n" + "="*40)
    print("      DATA CLEANING REPORT")
    print("="*40)
    print(f"Unique NF-e processed: {valid_count}")
    print(f"Duplicates isolated: {duplicate_count}")
    if duplicate_count > 0:
        print(f"Duplicates moved to: -> {duplicates_folder}")
    print("="*40)

if __name__ == "__main__":
    run_deduplication()
