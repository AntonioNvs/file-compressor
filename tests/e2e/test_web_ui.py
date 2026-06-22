import os
import time
import pytest
from src.huffman.io import read_compressed
from src.huffman.decoder import decode
from src.huffman.rle import rle_decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_upload_file_via_web_ui(driver, base_url, tmp_path):
    # (1) Cria um arquivo de texto de teste
    test_file = tmp_path / "test_upload.txt"
    test_file.write_text("Hello, this is a test file for Huffman compression! It needs to have some text.")
    
    # (1) Acessa a página index
    driver.get(base_url)
    
    # Seleciona a categoria Texto (já selecionada por padrão)
    
    # (2) Localiza o <input type="file"> e envia o caminho de um arquivo de texto
    file_input = driver.find_element(By.ID, "file-input")
    file_input.send_keys(str(test_file))
    
    # (3) Clica no botão submit
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    
    # (4) Aguarda o redirecionamento para a página de resultado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "original-size"))
    )
    
    # (5) Verifica que a página mostra estatísticas (tamanho original, comprimido)
    original_size = driver.find_element(By.ID, "original-size").text
    compressed_size = driver.find_element(By.ID, "compressed-size").text
    
    assert "bytes" in original_size
    assert "bytes" in compressed_size
    assert len(original_size.strip()) > 0
    assert len(compressed_size.strip()) > 0

def test_download_compressed_file_via_web_ui(driver, base_url, tmp_path, download_dir):
    # (1) Cria um arquivo e faz upload
    test_file = tmp_path / "test_download.txt"
    test_file.write_text("This text will be compressed and then downloaded.")
    
    driver.get(base_url)
    file_input = driver.find_element(By.ID, "file-input")
    file_input.send_keys(str(test_file))
    
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    
    # Aguarda redirecionamento para página de resultado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "download-btn"))
    )
    
    # (2) Clica no botão de download
    download_btn = driver.find_element(By.ID, "download-btn")
    download_btn.click()
    
    # (3) Verifica que o arquivo .huff é salvo no diretório de download
    downloaded_file = None
    # Wait up to 5 seconds for the download to finish
    for _ in range(10):
        files = os.listdir(download_dir)
        huff_files = [f for f in files if f.endswith(".huff")]
        if huff_files:
            downloaded_file = os.path.join(download_dir, huff_files[0])
            # Wait for file to have some size (download complete)
            if os.path.getsize(downloaded_file) > 0:
                break
        time.sleep(0.5)
        
    # (4) Verifica que não está vazio e tem extensão .huff
    assert downloaded_file is not None, "File was not downloaded"
    assert downloaded_file.endswith(".huff")
    assert os.path.getsize(downloaded_file) > 0, "Downloaded file is empty"

def test_error_case_on_invalid_upload(driver, base_url):
    # (1) Acessa página index
    driver.get(base_url)
    
    # (2) Clica submit sem selecionar arquivo
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    
    # (3) Verifica que uma mensagem de erro é exibida na página
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error-message"))
    )
    
    error_msg = driver.find_element(By.ID, "error-message").text
    assert len(error_msg) > 0

def test_full_happy_path_end_to_end(driver, base_url, tmp_path, download_dir):
    original_text = "This is a full happy path test for Huffman compression. Repeating some characters to ensure compression is effective: aaaaa bbbbb ccccc 11111 22222."
    
    # (1) Acessa index e prepara arquivo
    test_file = tmp_path / "happy_path.txt"
    test_file.write_text(original_text)
    
    driver.get(base_url)
    
    # (2) Faz upload de um arquivo de texto com conteúdo conhecido
    file_input = driver.find_element(By.ID, "file-input")
    file_input.send_keys(str(test_file))
    
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    
    # (3) Verifica estatísticas na página de resultado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "original-size"))
    )
    original_size = driver.find_element(By.ID, "original-size").text
    compressed_size = driver.find_element(By.ID, "compressed-size").text
    assert "bytes" in original_size
    assert "bytes" in compressed_size
    
    # (4) Faz download do arquivo comprimido
    download_btn = driver.find_element(By.ID, "download-btn")
    download_btn.click()
    
    downloaded_file = None
    for _ in range(10):
        files = os.listdir(download_dir)
        huff_files = [f for f in files if f.endswith(".huff")]
        if huff_files:
            downloaded_file = os.path.join(download_dir, huff_files[0])
            if os.path.getsize(downloaded_file) > 0:
                break
        time.sleep(0.5)
        
    assert downloaded_file is not None, "File was not downloaded in happy path"
    
    # (5) Lê o arquivo baixado, descomprime programaticamente e verifica
    tree, bitstring, original_name = read_compressed(downloaded_file)
    decoded_data = rle_decode(decode(bitstring, tree))
    
    assert decoded_data == original_text.encode("utf-8"), "Decompressed data does not match original"

def test_ui_elements_and_navigation(driver, base_url, tmp_path):
    # (1) Verifica elementos na página index
    driver.get(base_url)
    
    # Verifica título principal
    h1 = driver.find_element(By.TAG_NAME, "h1")
    assert "FileCompressor" in h1.text
    
    # Verifica presença do formulário e seus componentes
    assert driver.find_element(By.ID, "upload-form").is_displayed()
    
    # Verifica botões de modo
    compress_btn = driver.find_element(By.ID, "mode-compress")
    decompress_btn = driver.find_element(By.ID, "mode-decompress")
    assert compress_btn.is_displayed()
    assert decompress_btn.is_displayed()
    
    # Verifica cards de categoria
    category_section = driver.find_element(By.ID, "category-section")
    assert category_section.is_displayed()
    
    submit_btn = driver.find_element(By.ID, "submit-btn")
    assert submit_btn.is_displayed()
    assert submit_btn.is_enabled()
    
    # (2) Realiza o upload para navegar até a página de resultado
    test_file = tmp_path / "nav_test.txt"
    test_file.write_text("Testing navigation")
    
    file_input = driver.find_element(By.ID, "file-input")
    file_input.send_keys(str(test_file))
    submit_btn.click()
    
    # Aguarda o carregamento da página de resultado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "back-btn"))
    )
    
    # Verifica elementos na página de resultado
    assert driver.find_element(By.ID, "original-size").is_displayed()
    assert driver.find_element(By.ID, "compressed-size").is_displayed()
    assert driver.find_element(By.ID, "filename").is_displayed()
    
    download_btn = driver.find_element(By.ID, "download-btn")
    assert download_btn.is_displayed()
    assert download_btn.is_enabled()
    
    back_btn = driver.find_element(By.ID, "back-btn")
    assert back_btn.is_displayed()
    assert back_btn.is_enabled()
    
    # (3) Navega de volta para index
    back_btn.click()
    
    # Aguarda retornar ao index
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "upload-form"))
    )
    
    # Verifica que retornou ao index
    index_h1 = driver.find_element(By.TAG_NAME, "h1")
    assert "FileCompressor" in index_h1.text

# --- New E2E tests for mode toggle and categories ---

def test_mode_toggle_changes_ui(driver, base_url):
    """Testa que o toggle compactar/descompactar muda a UI dinamicamente."""
    driver.get(base_url)
    
    # Modo compactar (padrão): cards de categoria devem estar visíveis
    category_section = driver.find_element(By.ID, "category-section")
    assert category_section.is_displayed()
    
    decompress_info = driver.find_element(By.ID, "decompress-info")
    assert not decompress_info.is_displayed()
    
    # Clica no botão descompactar
    decompress_btn = driver.find_element(By.ID, "mode-decompress")
    decompress_btn.click()
    
    time.sleep(0.3)  # Wait for JS
    
    # Cards devem sumir, info de descompactação deve aparecer
    assert not category_section.is_displayed()
    assert decompress_info.is_displayed()
    
    # Volta para compactar
    compress_btn = driver.find_element(By.ID, "mode-compress")
    compress_btn.click()
    
    time.sleep(0.3)
    
    assert category_section.is_displayed()
    assert not decompress_info.is_displayed()

def test_category_selection_changes_accept(driver, base_url):
    """Testa que selecionar uma categoria muda o accept do input file."""
    driver.get(base_url)
    
    file_input = driver.find_element(By.ID, "file-input")
    
    # Padrão: categoria texto
    assert ".txt" in file_input.get_attribute("accept")
    
    # Clica na categoria PDF
    pdf_card = driver.find_element(By.CSS_SELECTOR, '[data-category="pdf"]')
    pdf_card.click()
    
    time.sleep(0.3)
    
    assert file_input.get_attribute("accept") == ".pdf"
    
    # Clica na categoria Imagem
    image_card = driver.find_element(By.CSS_SELECTOR, '[data-category="image"]')
    image_card.click()
    
    time.sleep(0.3)
    
    assert ".png" in file_input.get_attribute("accept")
    assert ".jpg" in file_input.get_attribute("accept")
