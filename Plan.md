# Plan.md — FileCompressor: 54 Commits, Sequential

## Deadlines & Sequence

| Pessoa    | Tarefas    | % Tarefas | Início  | Prazo     |
|-----------|------------|-----------|---------|-----------|
| Antônio   | 01 — 22    | 40%       | Hoje    | 13/Jun    |
| Bernardo  | 23 — 38    | 30%       | 13/Jun  | 17/Jun    |
| Raphael   | 39 — 54    | 30%       | 17/Jun  | 20/Jun    |

**Regra:** apenas UMA pessoa trabalhando por vez (commits sequenciais).
Cada tarefa = **1 commit**. Total: 54 commits (≥50).

---

## Phase 1 — Antônio (22 tasks: foundation + Huffman core + CI + initial tests)

### #01 — `chore: create project directory structure`
**Resumo:** Criar a árvore de diretórios do projeto com todos os `__init__.py` necessários para tornar cada pacote importável. As pastas são: `src/huffman/` (algoritmo), `src/web/templates/` (HTML), `tests/unit/`, `tests/integration/`, `tests/e2e/` (testes) e `.github/workflows/` (CI). Cada `__init__.py` fica vazio — serve apenas para marcar o diretório como pacote Python. Isso garante que `from src.huffman.node import Node` funcione sem surpresas de path.

### #02 — `chore: add requirements.txt and .gitignore`
**Resumo:** Criar `requirements.txt` com as dependências exatas do projeto: `flask`, `pytest`, `pytest-cov` (para coverage), `coverage`, e `selenium`. Criar `.gitignore` cobrindo `venv/`, `__pycache__/`, `*.pyc`, `.coverage`, `.pytest_cache/`, `htmlcov/` e `*.huff` (arquivos comprimidos gerados localmente). Isso evita que arquivos gerados ou de ambiente virtual sejam commitados acidentalmente.

### #03 — `feat: implement Huffman Node class`
**Resumo:** Implementar a classe `Node` em `src/huffman/node.py`. A classe representa um nó da árvore de Huffman com atributos `char` (caractere, `None` para nós internos), `freq` (frequência), `left` e `right` (filhos, `None` para folhas). Implementar `__lt__` para permitir ordenação em min-heap (compara pela frequência). Esse é o bloco fundamental sobre o qual toda a árvore é construída.

### #04 — `feat: implement frequency counter for text input`
**Resumo:** Implementar `count_frequencies(text: str) -> dict[str, int]` em `src/huffman/counter.py`. A função recebe uma string, conta quantas vezes cada caractere aparece e retorna um dicionário `{caractere: frequência}`. É o primeiro passo do algoritmo de Huffman: antes de montar a árvore, precisamos saber a frequência de cada símbolo.

### #05 — `feat: implement Huffman Tree builder via min-heap`
**Resumo:** Implementar `build_tree(freqs: dict[str, int]) -> Node` em `src/huffman/tree.py`. Usando `heapq`, a função cria um nó folha para cada caractere e os insere em uma min-heap. Depois, em loop, remove os dois nós de menor frequência, cria um nó interno com a soma das frequências e os reinsere. Ao final, o único nó restante é a raiz da árvore de Huffman.

### #06 — `feat: implement code generator by tree traversal`
**Resumo:** Adicionar `generate_codes(root: Node) -> dict[str, str]` em `src/huffman/tree.py`. A função percorre a árvore em DFS: ao descer para a esquerda adiciona `'0'` ao prefixo, ao descer para a direita adiciona `'1'`. Ao atingir uma folha, salva o prefixo acumulado como o código Huffman daquele caractere. Retorna `{caractere: "sequência_de_bits"}`.

### #07 — `feat: implement Huffman text encoder`
**Resumo:** Implementar `encode(text: str) -> tuple[str, Node]` em `src/huffman/encoder.py`. A função (1) conta frequências com `count_frequencies`, (2) constrói a árvore com `build_tree`, (3) gera códigos com `generate_codes`, (4) substitui cada caractere do texto pelo seu código binário, concatenando tudo em uma única string de bits. Retorna a string de bits e a raiz da árvore (necessária para decodificar depois).

### #08 — `feat: implement Huffman text decoder`
**Resumo:** Implementar `decode(bitstring: str, root: Node) -> str` em `src/huffman/decoder.py`. A função percorre a string de bits: começa na raiz, para cada `'0'` vai para o filho esquerdo, para cada `'1'` vai para o filho direito. Ao atingir uma folha, emite o caractere e volta à raiz. O texto original é reconstruído caractere por caractere, sem ambiguidade graças à propriedade prefix-free dos códigos de Huffman.

### #09 — `feat: implement binary file writer (header + body)`
**Resumo:** Implementar `write_compressed(path: str, tree: Node, bitstring: str)` em `src/huffman/io.py`. A função serializa a árvore e a string de bits em um arquivo binário `.huff`. O formato: (1) header com a árvore serializada (permite reconstrução na leitura), (2) padding bits (últimos bits do último byte que não formam um byte completo), (3) corpo com os bits empacotados em bytes. Isso é o que torna a compressão real: converter a string de bits em bytes no disco.

### #10 — `feat: implement binary file reader (header + body)`
**Resumo:** Implementar `read_compressed(path: str) -> tuple[Node, str]` em `src/huffman/io.py`. A função lê o arquivo `.huff` no formato definido em `write_compressed`: extrai a árvore do header, lê o padding e os bytes do corpo, desempacota os bits de volta para uma string de `'0'`/`'1'`. Retorna a árvore reconstruída e a string de bits pronta para decodificação.

### #11 — `feat: add tree serialization to binary format`
**Resumo:** Adicionar `serialize_tree(root: Node) -> bytes` e `deserialize_tree(data: bytes) -> Node` em `src/huffman/io.py`. A serialização percorre a árvore em pré-ordem: para folhas escreve um bit `1` seguido do caractere (1 byte), para nós internos escreve um bit `0` e recursivamente os filhos. A desserialização lê bit a bit reconstruindo a estrutura. Essencial para que o header do arquivo comprimido contenha a árvore de forma compacta.

### #12 — `chore: add pytest.ini and .coveragerc configuration`
**Resumo:** Criar `pytest.ini` com `testpaths = tests`, configuração de markers (`unit`, `integration`, `e2e`) e opções padrão (`--strict-markers`, `-v`). Criar `.coveragerc` com `source = src` (mede cobertura apenas do código fonte, não dos testes), `branch = True` (cobertura de branches, não só linhas), e exclusão de `__init__.py` e imports. Isso padroniza a execução de testes e a medição de cobertura.

### #13 — `test: add unit tests for Huffman Node class`
**Resumo:** Escrever `tests/unit/test_node.py` com 4 testes. (1) `test_create_leaf_node`: cria nó folha e verifica `char` e `freq`. (2) `test_create_internal_node`: cria nó interno com filhos e verifica que `char is None`. (3) `test_node_comparison`: cria dois nós com frequências diferentes e verifica que `<` funciona corretamente (necessário para heap). (4) `test_node_equality`: verifica que nós com mesmos atributos são considerados iguais.

### #14 — `test: add unit tests for frequency counter`
**Resumo:** Escrever `tests/unit/test_counter.py` com 4 testes. (1) `test_empty_string`: entrada `""` retorna `{}`. (2) `test_single_char`: entrada `"a"` retorna `{"a": 1}`. (3) `test_repeated_chars`: entrada `"aaabb"` retorna `{"a": 3, "b": 2}`. (4) `test_mixed_chars`: entrada com espaços, números e letras — verifica contagem correta de cada símbolo distinto.

### #15 — `test: add unit tests for Huffman Tree builder`
**Resumo:** Escrever `tests/unit/test_tree.py` com 3 testes. (1) `test_single_char`: frequências `{"x": 5}` — a raiz deve ser folha com `char='x'`. (2) `test_two_chars`: `{"a": 1, "b": 2}` — raiz interna, folhas corretas, frequência da raiz = 3. (3) `test_multiple_chars`: 4+ caracteres com frequências variadas — verifica que a árvore tem estrutura válida (raiz com freq = soma total).

### #16 — `test: add unit tests for code generator`
**Resumo:** Adicionar 3 testes em `tests/unit/test_tree.py`. (1) `test_codes_are_prefix_free`: gera códigos e verifica que nenhum código é prefixo de outro (propriedade fundamental de Huffman). (2) `test_codes_unique`: cada caractere tem um código distinto. (3) `test_variable_length`: caracteres mais frequentes recebem códigos mais curtos (verifica que `max(freq)` tem código de comprimento mínimo).

### #17 — `test: add unit tests for Huffman text encoder`
**Resumo:** Escrever `tests/unit/test_encoder.py` com 4 testes. (1) `test_simple_phrase`: codifica `"hello"` e verifica que a string de bits não é vazia e a árvore retornada é válida. (2) `test_single_char`: codifica `"aaaa"` — cada `'a'` deve ser codificado com 1 bit (caso ótimo). (3) `test_unicode`: codifica texto com acentos e caracteres especiais (`"coração"`). (4) `test_empty_string`: codifica `""` — espera-se string de bits vazia como resultado.

### #18 — `test: add unit tests for Huffman text decoder`
**Resumo:** Escrever `tests/unit/test_decoder.py` com 4 testes. (1) `test_roundtrip_simple`: codifica e decodifica `"hello world"`, verifica que o resultado é idêntico. (2) `test_roundtrip_phrase`: roundtrip com frase longa incluindo pontuação e espaços. (3) `test_roundtrip_unicode`: roundtrip com `"coração é vida!"` — acentos e caracteres latinos preservados. (4) `test_empty_input`: decodificar string de bits vazia retorna `""`.

### #19 — `ci: add GitHub Actions workflow with Linux matrix`
**Resumo:** Criar `.github/workflows/ci.yml` com um workflow que dispara em `push` e `pull_request` para a branch `main`. Define uma job `test` com `strategy.matrix.python-version: ["3.10", "3.12"]` rodando em `ubuntu-latest`. Passos: checkout, setup Python, instala dependências via `pip install -r requirements.txt`, executa `pytest --cov=src --cov-report=xml`, e faz upload do relatório de coverage como artefato.

### #20 — `ci: add macOS and Windows to CI matrix`
**Resumo:** Expandir o `ci.yml` adicionando `os: [ubuntu-latest, macos-latest, windows-latest]` à matrix. Isso faz com que o mesmo job de testes rode em 3 sistemas operacionais × 2 versões de Python = 6 combinações. O objetivo é atender ao requisito de CI multi-OS e garantir que o código funciona em todos os ambientes (cuidado com paths no Windows: usar `pathlib` ou `os.path.join`).

### #21 — `ci: integrate Codecov coverage upload`
**Resumo:** Adicionar ao `ci.yml` um step que executa `codecov/codecov-action@v4` após `pytest --cov` ter gerado `coverage.xml`. O step faz upload do relatório para o Codecov usando o token configurado como secret `CODECOV_TOKEN` no repositório. Incluir também o badge do Codecov no topo do README para visibilidade da cobertura.

### #22 — `docs: update README with all required sections`
**Resumo:** Reescrever o `README.md` com as 4 seções obrigatórias do trabalho: (1) **Membros do grupo** — Antônio, Bernardo, Raphael. (2) **Descrição do sistema** — compactador de arquivos via Huffman com interface web Flask. (3) **Tecnologias** — Huffman, Flask, Pytest, Coverage, Selenium, GitHub Actions, Codecov. (4) **Como rodar os testes** — instruções passo a passo: `pip install -r requirements.txt`, `pytest`, `pytest --cov=src`. Adicionar badges de CI (GitHub Actions) e coverage (Codecov).

---

## Phase 2 — Bernardo (16 tasks: Flask web app + integration tests + more unit tests)

### #23 — `feat: create Flask app factory with configuration`
**Resumo:** Criar `src/web/app.py` com a função `create_app()`. Usar o padrão application factory do Flask: criar a instância `Flask(__name__)`, configurar `UPLOAD_FOLDER` (pasta temporária para uploads), `MAX_CONTENT_LENGTH` (limite de tamanho de arquivo, ex: 16MB), e registrar o blueprint de rotas. A factory facilita testes (cada teste cria uma app limpa) e é a forma recomendada pelo Flask.

### #24 — `feat: add index.html template with file upload form`
**Resumo:** Criar `src/web/templates/index.html` com um formulário HTML simples e funcional. Deve conter: `<form method="POST" enctype="multipart/form-data">`, `<input type="file" name="file">`, e um botão de submit ("Comprimir"). Estilização mínima com CSS inline — o foco é funcionalidade, não design. Essa é a página inicial que o usuário vê ao acessar o sistema web.

### #25 — `feat: implement upload route — receive file and compress`
**Resumo:** Adicionar rota `POST /upload` em `src/web/routes.py`. A rota recebe o arquivo via `request.files["file"]`, lê o conteúdo como texto, chama `encode()` do módulo Huffman para comprimir, e salva o arquivo `.huff` resultante na pasta de upload. Redireciona para a página de resultado com o nome do arquivo comprimido e estatísticas de compressão como parâmetros.

### #26 — `feat: implement download route — serve compressed file`
**Resumo:** Adicionar rota `GET /download/<filename>` em `src/web/routes.py`. A rota recebe o nome do arquivo comprimido como parâmetro na URL, localiza-o na pasta de upload, e o envia ao navegador usando `flask.send_file()` com `as_attachment=True` e o header `Content-Disposition` apropriado. Incluir validação básica: se o arquivo não existe, retornar 404.

### #27 — `feat: add result.html template with compression stats`
**Resumo:** Criar `src/web/templates/result.html` que exibe as estatísticas da compressão: tamanho do arquivo original (em bytes), tamanho do arquivo comprimido, taxa de compressão (percentual), e um botão/link para download do arquivo `.huff`. A página recebe os dados via `render_template` com variáveis passadas pela rota. Layout simples e funcional.

### #28 — `feat: add error handling for invalid file uploads`
**Resumo:** Adicionar tratamento de erros em `src/web/routes.py` para os casos: (1) requisição sem arquivo anexado, (2) arquivo com nome vazio, (3) arquivo com extensão ou tipo MIME não suportado (ex: binário não-texto), (4) arquivo vazio (0 bytes). Cada caso retorna uma mensagem de erro amigável em uma página HTML simples (ou flash message + redirect para index). Evita crash da aplicação em entradas inválidas.

### #29 — `feat: add compression ratio calculation to encoder`
**Resumo:** Adicionar `get_stats(text: str) -> dict` em `src/huffman/encoder.py`. A função retorna um dicionário com: `original_size` (tamanho do texto original em bytes), `compressed_size` (tamanho estimado da string de bits em bytes), `ratio` (percentual de redução), e `tree_size` (número de nós na árvore). Essas estatísticas são exibidas na página de resultado e também úteis para debugging e testes.

### #30 — `test: add unit tests for binary I/O serialization`
**Resumo:** Escrever `tests/unit/test_io.py` com 4 testes. (1) `test_write_read_roundtrip`: comprime um texto simples, escreve `.huff`, lê de volta, verifica que árvore e bitstring são idênticas. (2) `test_tree_serialization`: serializa e desserializa uma árvore complexa, verifica estrutura idêntica. (3) `test_empty_input`: write/read com texto vazio (edge case). (4) `test_large_input`: roundtrip com 5000+ caracteres — testa robustez do formato binário.

### #31 — `test: add unit tests for edge cases (empty, single char, special)`
**Resumo:** Ampliar `tests/unit/test_encoder.py` e `tests/unit/test_decoder.py` com 4 novos testes focados em edge cases. (1) `test_only_spaces`: texto composto apenas de espaços e whitespace. (2) `test_only_newlines`: texto com `\n` e `\r\n`. (3) `test_binary_like_text`: texto contendo caracteres `'0'` e `'1'` (garantir que não confunde com bitstring). (4) `test_single_char_repeated`: 1000× o mesmo caractere — decodificação deve ser exata.

### #32 — `test: add unit tests for large input and unicode boundary`
**Resumo:** Adicionar 3 testes em `tests/unit/test_encoder.py`. (1) `test_large_text_10k`: roundtrip com 10.000 caracteres de texto variado — garante que não há perda. (2) `test_emoji`: roundtrip com emojis (`😀🎉👍`), verificando que multi-byte characters são preservados. (3) `test_mixed_scripts`: texto com latim, cirílico, chinês e árabe misturados — teste de robustez Unicode.

### #33 — `test: add integration test for Flask upload route`
**Resumo:** Escrever `tests/integration/test_flask_routes.py` com um teste de integração para a rota `POST /upload`. Usar o `app.test_client()` do Flask para simular uma requisição multipart com um arquivo de texto real anexado. Verificar que a resposta tem status 200 (ou redirect 302), que o arquivo `.huff` foi criado no disco, e que a resposta contém as estatísticas de compressão esperadas. Teste de integração = testa a rota real com o algoritmo real, sem mocks.

### #34 — `test: add integration test for Flask download route`
**Resumo:** Adicionar teste em `tests/integration/test_flask_routes.py` para `GET /download/<filename>`. Primeiro faz upload de um arquivo para gerar o `.huff`, depois faz GET na rota de download com o nome do arquivo gerado. Verifica status 200, header `Content-Disposition: attachment`, e que o corpo da resposta contém dados binários (não vazio). Confirma que o fluxo upload→download funciona integrado.

### #35 — `test: add integration test for full compress-decompress pipeline`
**Resumo:** Escrever `tests/integration/test_full_pipeline.py` com um teste que cobre o pipeline completo sem interface web. Lê um arquivo de texto, codifica com Huffman, escreve arquivo `.huff` binário em disco, lê o arquivo de volta, decodifica, e verifica que o texto resultante é idêntico ao original. Testa a integração dos módulos `encoder`, `io`, e `decoder` como um sistema coeso.

### #36 — `test: add integration test for error handling routes`
**Resumo:** Adicionar 2-3 testes em `tests/integration/test_flask_routes.py` para os cenários de erro da aplicação web. (1) POST `/upload` sem anexar arquivo — espera 400 com mensagem de erro. (2) POST com arquivo de nome vazio — espera 400. (3) POST com arquivo não-texto (ex: binário) — espera 400 ou mensagem de erro tratada. Garante que o servidor não crasha e responde com erros adequados.

### #37 — `test: add unit tests for compression ratio stats`
**Resumo:** Adicionar 3 testes em `tests/unit/test_encoder.py` para a função `get_stats()`. (1) `test_stats_on_normal_text`: verifica que `original_size > compressed_size` e `ratio > 0` para texto típico. (2) `test_stats_on_single_char`: original 100 bytes, comprimido ≈ 13 bytes (100 bits / 8) — ratio de ~87%. (3) `test_stats_on_empty`: texto vazio retorna `original_size = 0` e trata divisão por zero adequadamente.

### #38 — `test: add supplementary unit tests to reach 30+ minimum`
**Resumo:** Varredura final da suíte de testes unitários: adicionar 3-4 testes pontuais para funções ou branches ainda não cobertos. Possíveis alvos: `__lt__` do Node com frequências iguais, `build_tree` com dicionário vazio, `generate_codes` com árvore de nó único, `deserialize_tree` com bytes corrompidos. Objetivo: garantir que o total de testes unitários ultrapasse 30 (somando Fase 1 + Fase 2).

---

## Phase 3 — Raphael (16 tasks: Selenium E2E + coverage push + polish)

### #39 — `chore: add Selenium WebDriver fixtures and configuration`
**Resumo:** Criar `tests/e2e/conftest.py` com fixtures pytest para Selenium. A fixture `driver` configura um Chrome headless (`--headless`, `--no-sandbox`, `--disable-dev-shm-usage`), define timeout implícito de 10s, e faz `yield` do driver (com `driver.quit()` no teardown). A fixture `base_url` fornece a URL base para os testes (padrão `http://localhost:5000`). Essas fixtures serão reutilizadas por todos os testes E2E.

### #40 — `test: add Selenium E2E test — upload file via web UI`
**Resumo:** Escrever `tests/e2e/test_web_ui.py` com o primeiro teste E2E: (1) acessa a página index, (2) localiza o `<input type="file">` e envia o caminho de um arquivo de texto de teste via `.send_keys()`, (3) clica no botão submit, (4) aguarda o redirecionamento para a página de resultado, (5) verifica que a página mostra estatísticas (tamanho original, comprimido). Teste ponta-a-ponta real: browser → servidor Flask → algoritmo Huffman → resposta HTML.

### #41 — `test: add Selenium E2E test — download compressed file`
**Resumo:** Adicionar teste em `tests/e2e/test_web_ui.py`: (1) faz upload de um arquivo de texto, (2) na página de resultado, clica no link/botão de download, (3) verifica que o download é iniciado (o arquivo `.huff` é salvo no diretório de download configurado), (4) verifica que o arquivo baixado não está vazio e tem a extensão `.huff`. Testa o ciclo completo de interação do usuário com o sistema.

### #42 — `test: add Selenium E2E test — error case on invalid upload`
**Resumo:** Adicionar teste em `tests/e2e/test_web_ui.py`: (1) acessa página index, (2) clica submit sem selecionar arquivo, (3) verifica que uma mensagem de erro é exibida na página (não um crash/500). Opcionalmente testar também o upload de um arquivo com extensão inválida ou de 0 bytes. Valida que o tratamento de erro funciona na camada de UI, não apenas na API.

### #43 — `test: add Selenium E2E test — full happy path end-to-end`
**Resumo:** Adicionar teste completo em `tests/e2e/test_web_ui.py` que simula a jornada completa do usuário: (1) acessa index, (2) faz upload de um arquivo de texto com conteúdo conhecido, (3) verifica estatísticas na página de resultado, (4) faz download do arquivo comprimido, (5) (opcional) lê o arquivo baixado, descomprime programaticamente e verifica que o conteúdo é idêntico ao original. O teste mais completo — valida o sistema de ponta a ponta como o usuário final o experimenta.

### #44 — `test: add Selenium E2E test — UI elements and navigation`
**Resumo:** Adicionar teste em `tests/e2e/test_web_ui.py` focado nos elementos de UI: (1) verifica que todos os elementos esperados estão presentes no index (título, formulário, input file, botão submit), (2) verifica navegação entre páginas (index → resultado → voltar para index), (3) verifica que os botões e links são clicáveis e visíveis. Garante que a interface web está íntegra e navegável em diferentes resoluções de viewport.

### #45 — `test: add unit tests for uncovered branches (part 1)`
**Resumo:** Executar `pytest --cov=src --cov-report=term-missing` para identificar branches não cobertos no encoder e decoder. Adicionar 2-3 testes específicos para cobrir esses branches. Exemplos típicos: caminho de erro na leitura de arquivo inexistente, comportamento com árvore degenerada (só nó esquerdo), decodificação com bitstring que termina em nó interno (erro).

### #46 — `test: add unit tests for uncovered branches (part 2)`
**Resumo:** Continuar a varredura de cobertura, agora focando em `src/huffman/tree.py` e `src/huffman/io.py`. Adicionar 2-3 testes para cobrir branches como: desserialização de árvore com dados truncados, `serialize_tree` com árvore de um único nó, `read_compressed` com arquivo vazio. O objetivo é subir a cobertura de branches (não só linhas) para próximo de 90%.

### #47 — `test: add missing test cases to push coverage above 80%`
**Resumo:** Ponto de verificação: rodar `pytest --cov=src --cov-report=html` e inspecionar o relatório HTML para encontrar os módulos com menor cobertura. Adicionar testes direcionados para elevar a cobertura de cada módulo acima de 80%. Possíveis alvos: `src/web/routes.py` (caminhos de erro do Flask), `src/web/app.py` (factory com diferentes configs).

### #48 — `test: finalize coverage to ≥90% as per project README goal`
**Resumo:** Última iteração de cobertura: adicionar os testes restantes para atingir pelo menos 90% de cobertura de linhas e branches. Executar `pytest --cov=src --cov-report=term` e verificar o número final. Se ainda houver gaps, focar nos trechos de menor complexidade restantes (exceções, caminhos alternativos). O README do projeto estabelece 90% como meta, acima dos 80% exigidos.

### #49 — `ci: add Selenium to GitHub Actions (headless on all 3 OS)`
**Resumo:** Atualizar `.github/workflows/ci.yml` para incluir os testes E2E com Selenium na pipeline de CI. Adicionar steps para instalar o Chrome/Chromium e o ChromeDriver adequado em cada OS (Linux: `sudo apt-get install chromium-browser`, macOS: `brew install chromium`, Windows: `choco install chromium`). Configurar a variável `HEADLESS=true` e garantir que os testes E2E rodam em modo headless nos 3 sistemas operacionais.

### #50 — `docs: add instructions for running e2e tests to README`
**Resumo:** Adicionar ao `README.md` uma seção ou subseção explicando como rodar os testes end-to-end: (1) instalar Chrome/Chromium, (2) instalar dependências (`pip install -r requirements.txt`), (3) iniciar o servidor Flask (`flask run` ou `python -m src.web.app`), (4) executar `pytest tests/e2e/ -v`. Incluir nota sobre a necessidade do ChromeDriver e modo headless.

### #51 — `docs: finalize README with coverage badge and CI badge`
**Resumo:** Revisar e finalizar o `README.md` com os badges no topo: badge do GitHub Actions (status do workflow de CI) e badge do Codecov (percentual de cobertura). Verificar que todas as 4 seções obrigatórias estão completas e bem formatadas. Adicionar o link do repositório e garantir que as instruções de execução de testes estão claras e reproduzíveis.

### #52 — `test: final integration test for large file pipeline`
**Resumo:** Adicionar um último teste de integração em `tests/integration/test_full_pipeline.py` com um arquivo de texto grande (≥ 100KB, gerado programaticamente com texto repetido + aleatório). O teste cobre: compressão → escrita binária → leitura binária → descompressão → verificação de integridade. Mede também que a taxa de compressão é significativa (> 40% para texto natural). Garante que o sistema escala para arquivos realistas.

### #53 — `refactor: final code cleanup and inline documentation`
**Resumo:** Revisão final de todo o código fonte: (1) remover imports não utilizados, variáveis mortas, e comentários de desenvolvimento, (2) garantir que todos os nomes de funções e variáveis seguem snake_case (PEP 8), (3) adicionar docstrings curtas (uma linha) em funções públicas, (4) verificar que não há `print()` solto ou código de debug, (5) garantir consistência de estilo com `black` ou inspeção visual. Nenhuma mudança de lógica — apenas limpeza.

### #54 — `chore: final .gitignore update and repository verification`
**Resumo:** Verificação final do repositório: (1) checar que `.gitignore` cobre todos os artefatos gerados (`.huff`, `.coverage`, `htmlcov/`, `geckodriver.log`, screenshots de teste, `__pycache__`), (2) rodar `git status` para confirmar que nada indesejado está tracked, (3) verificar que `requirements.txt` está completo e as versões são reproduzíveis, (4) opcional: adicionar `Makefile` com targets `test`, `test-cov`, `test-e2e`, `run` para conveniência. Commit final que fecha o projeto.

---

## Resumo dos Requisitos Atendidos

| Requisito                | Mínimo        | Planejado            |
|--------------------------|---------------|----------------------|
| Commits                  | ≥ 50          | 54 (exatos)          |
| Unit tests               | ≥ 30          | ~38 (13 + 18 + 7)    |
| Integration/E2E tests    | ≥ 5           | ~10 (4 + 6)          |
| Coverage                 | ≥ 80%         | ≥ 90%                |
| CI operating systems     | 3             | Linux, macOS, Windows|
| Codecov                  | obrigatório   | Task #21             |
| README sections          | 4             | Tasks #22, #50, #51  |

---

## Nota sobre Linhas por Pessoa

Antônio tem 22 tarefas (40%) vs 16 (30%) de Bernardo e Raphael. As tarefas de
Antônio são de setup/infra (commits menores em linhas), enquanto Bernardo e
Raphael fazem implementações mais densas (Flask app, Selenium suite, testes
extensivos). O total de linhas commitadas por pessoa tende a se equilibrar,
atendendo ao requisito de igualdade aproximada no `git diff --stat`.
