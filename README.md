# FileCompressor: Compactação de arquivos - Huffman Algorithm

[![CI](https://github.com/AntonioNvs/file-compressor/actions/workflows/ci.yml/badge.svg)](https://github.com/AntonioNvs/file-compressor/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/AntonioNvs/file-compressor/graph/badge.svg)](https://codecov.io/gh/AntonioNvs/file-compressor)

## Membros do grupo
- Antônio Caetano Neves Neto
- Bernardo Dutra Lemos
- Raphael Aroldo Carreiro Mendes

## Descrição do sistema

Sistema de compactação de arquivos de texto feito em Python + Interface Gráfica (Flask) que funcionará em um sistema web, recebendo o arquivo a ser compactado e retornando ele compactado, disponível para download. O sistema será modular de forma a facilitar os testes para cada etapa do processo. O *coverage* será acima de 90%. O desenvolvimento seguirá a metodologia TDD, visando atingir tal *coverage* e modularidade do sistema.

## Explicação das tecnologias

- **Huffman**: Algoritmo central utilizado para realizar a compactação de texto baseada na frequência dos caracteres.
- **Flask**: Criação da API de submissão dos arquivos e download dos mesmos, atuando como o *backend* para execução do Huffman e *frontend* para as páginas HTML.
- **Pytest**: Automatiza os testes unitários e de integração do sistema.
- **Coverage**: Usado para medir a cobertura de testes do código fonte (meta de >90%).
- **Selenium**: Automatização de testes *end-to-end* da interface gráfica web, simulando interações reais de usuário no browser.
- **GitHub Actions**: Plataforma de CI/CD utilizada para rodar os testes automaticamente em uma matriz de múltiplos sistemas operacionais (Linux, macOS, Windows) e versões do Python.
- **Codecov**: Ferramenta integrada ao CI para armazenar, analisar e disponibilizar publicamente o relatório de cobertura gerado pelos testes.

## Como rodar os testes

Para executar a suíte de testes do projeto e verificar a cobertura do código localmente, siga as instruções abaixo:

1. **Instale as dependências** do projeto:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute os testes** com o Pytest:
   ```bash
   pytest
   ```

3. **Verifique a cobertura** de código:
   ```bash
   pytest --cov=src
   ```

### Testes End-to-End (E2E)

Para rodar os testes end-to-end simulando interações reais do usuário no navegador:

1. Certifique-se de que o **Chrome/Chromium** e o respectivo **ChromeDriver** estão instalados no seu sistema.
2. Com as dependências instaladas (`pip install -r requirements.txt`), inicie o servidor Flask em um terminal separado:
   ```bash
   python -m src.web.app
   ```
3. Em outro terminal, execute a suíte de testes E2E com o Pytest:
   ```bash
   pytest tests/e2e/ -v
   ```

*Nota: Os testes E2E estão configurados para executar o Chrome em modo headless por padrão, não abrindo uma janela visual do navegador.*
