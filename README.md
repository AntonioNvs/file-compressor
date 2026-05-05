# FileCompressor: Compactação de arquivos - Huffman Algorithm

## Membros do grupo
- Antônio Caetano Neves Neto
- Bernardo Dutra Lemos
- Raphael Aroldo Carreiro Mendes

## Descrição do sistema

Sistema de compactação de arquivos de texto feito em Python que funcionará via linha de comando, recebendo o arquivo a ser compactado e o caminho do destino do resultado. O sistema será modular de forma a fazer o testes para cada etapa do processo. O *coverage* será acima de 90%. O desenvolvimento seguirá a metodologia TDD, visando atingir tal *coverage* e modularidade do sistema.

## Explicação das tecnologias

- [Huffman](https://pt.wikipedia.org/wiki/Codifica%C3%A7%C3%A3o_de_Huffman): Utilizado para gerar hashes ou assinaturas compactas de blocos de código, facilitando a comparação eficiente entre arquivos para identificar duplicatas.
- [Pytest](https://docs.pytest.org/en/stable/): Automatiza os testes unitários e de integração do seu pipeline de detecção, garantindo que o algoritmo identifique corretamente os clones e ignore os falsos positivos.
- [python-fire](https://github.com/google/python-fire): Transforma funções de análise em ferramentas de linha de comando para facilitar a execução de testes e automações.
