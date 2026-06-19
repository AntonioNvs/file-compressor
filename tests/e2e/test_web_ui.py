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
