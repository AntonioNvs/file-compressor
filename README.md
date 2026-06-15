# FileCompressor: Compactação de arquivos - Huffman Algorithm

[![codecov](https://codecov.io/gh/AntonioNvs/file-compressor/graph/badge.svg)](https://codecov.io/gh/AntonioNvs/file-compressor)

## Membros do grupo
- Antônio Caetano Neves Neto
- Bernardo Dutra Lemos
- Raphael Aroldo Carreiro Mendes

## Descrição do sistema

Sistema de compactação de arquivos de texto feito em Python + Interface Gráfica (Flask) que funcionará um sistema web, recebendo o arquivo a ser compactado e retornando ele compactado, disponível para download. O sistema será modular de forma a fazer o testes para cada etapa do processo. O *coverage* será acima de 90%. O desenvolvimento seguirá a metodologia TDD, visando atingir tal *coverage* e modularidade do sistema.

## Explicação das tecnologias

- [Huffman](https://pt.wikipedia.org/wiki/Codifica%C3%A7%C3%A3o_de_Huffman): Utilizado para gerar hashes ou assinaturas compactas de blocos de código, facilitando a comparação eficiente entre arquivos para identificar duplicatas.
- [Pytest](https://docs.pytest.org/en/stable/): Automatiza os testes unitários e de integração do seu pipeline de detecção, garantindo que o algoritmo identifique corretamente os clones e ignore os falsos positivos.
- [Selenium](https://www.selenium.dev/): Automatização de testes _end-to-end_ da interface gráfica web, testando a submissão de arquivos e toda a rotina de acesso, *import* de arquivos, compactação e download.
- [Flask](https://flask.palletsprojects.com/en/stable/): Criação da API de submissão dos arquivos e download dos mesmos, sendo como forma do *backend* para execução do Huffman, além do *frontend* para disponibilização das páginas HTML.
