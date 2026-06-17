import pytest
import xml.etree.ElementTree as ET
from etl_showcase import extract_text, process_xml_files

# ==========================================
# SETUP: XML de teste em memória
# ==========================================
ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

VALID_XML = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
  <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
    <infNFe Id="NFe35260100000000000191550010000015001234567890" versao="4.00">
      <ide>
        <nNF>1500</nNF>
        <serie>1</serie>
        <dhEmi>2026-01-10T10:00:00-03:00</dhEmi>
      </ide>
      <emit>
        <CNPJ>00000000000191</CNPJ>
      </emit>
      <total>
        <ICMSTot>
          <vNF>5000.00</vNF>
          <vTotTrib>750.00</vTotTrib>
        </ICMSTot>
      </total>
    </infNFe>
  </NFe>
</nfeProc>"""

# ==========================================
# TESTES
# ==========================================

def test_extract_text_retorna_valor_correto():
    """Verifica se extract_text lê o valor de uma tag corretamente."""
    root = ET.fromstring(VALID_XML)
    emit = root.find('.//ns:emit', ns)
    assert extract_text(emit, 'ns:CNPJ') == '00000000000191'

def test_extract_text_com_elemento_none():
    """Verifica se extract_text retorna string vazia quando elemento é None."""
    assert extract_text(None, 'ns:qualquer') == ''

def test_extract_text_com_tag_inexistente():
    """Verifica se extract_text retorna string vazia quando a tag não existe."""
    root = ET.fromstring(VALID_XML)
    emit = root.find('.//ns:emit', ns)
    assert extract_text(emit, 'ns:tagquenaoexiste') == ''

def test_process_xml_retorna_dataframe_com_dados(tmp_path):
    """Verifica se o pipeline processa um XML válido e retorna dados corretos."""
    xml_file = tmp_path / "nfe_teste.xml"
    xml_file.write_text(VALID_XML, encoding='utf-8')

    df = process_xml_files(str(tmp_path))

    assert not df.empty
    assert df.iloc[0]['Issuer_CNPJ'] == '00000000000191'
    assert df.iloc[0]['Total_Value'] == 5000.00
    assert df.iloc[0]['Invoice_Number'] == 1500

def test_process_xml_ignora_arquivo_corrompido(tmp_path):
    """Verifica se o pipeline ignora XMLs inválidos sem travar."""
    xml_invalido = tmp_path / "corrompido.xml"
    xml_invalido.write_text("isso não é um xml válido <<<", encoding='utf-8')

    df = process_xml_files(str(tmp_path))

    assert df.empty  # Não travou e retornou DataFrame vazio
