import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_upload_file_via_web_ui(driver, base_url, tmp_path):
    # (1) Cria um arquivo de texto de teste
    test_file = tmp_path / "test_upload.txt"
    test_file.write_text("Hello, this is a test file for Huffman compression! It needs to have some text.")
    
    # (1) Acessa a página index
    driver.get(base_url)
    
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
    
    # Verifica que o título de sucesso apareceu
    header = driver.find_element(By.TAG_NAME, "h1").text
    assert "Compressão Concluída" in header

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
