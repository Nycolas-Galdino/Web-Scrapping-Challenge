# Guia para Rodar o Script e os Testes

Este documento explica como configurar, executar o script principal e rodar os testes automatizados. 

---

## Pré-requisitos

Certifique-se de que os seguintes itens estão instalados no seu ambiente:

1. **[Python 3.11+](https://www.python.org/)**
2. **[GIT](https://git-scm.com/)**
3. **[Poetry](https://python-poetry.org/docs/)** (gerenciador de dependências do Python)

---

## Configuração do Ambiente

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/Nycolas-Galdino/Web-Scrapping-Challenge.git
   cd Web-Scrapping-Challenge
   ```

2. **Instale as Dependências com o Poetry**:
   ```bash
   poetry install
   ```

---

## Estrutura do Projeto

```plaintext
.
├── app/                 # Contém o script principal
│   ├── __init__.py      # Arquivo para tornar o diretório um módulo
│   ├── main.py          # O código principal
│   ├── config.py        # Configurações do script
├── tests/               # Contém os testes
│   ├── __init__.py      # Arquivo para tornar o diretório um módulo
│   ├── test_main.py     # Arquivo com os testes
├── pyproject.toml       # Configurações do Poetry e dependências
├── poetry.lock          # Arquivo de bloqueio de dependências
└── README.md            # Este guia
```

---

## Executando o Script Principal

1. **Navegue até a pasta do script**:
   ```bash
   cd app
   ```

2. **Execute o script**:
   ```bash
   poetry run python script.py
   ```

3. **Saída Esperada**:
   O script realiza as seguintes tarefas:
   - Obtém dados de faturas a partir de uma API.
   - Filtra as faturas com vencimento igual ou posterior à data atual.
   - Faz o download dos arquivos de fatura.
   - Gera um arquivo CSV com as informações processadas.

   Se tudo ocorrer corretamente, você verá uma mensagem de sucesso no console:
   ```plaintext
   Processamento concluído com sucesso!
   ```

---

## Executando os Testes Automatizados

Os testes estão localizados na pasta `tests/` e cobrem todas as funções do script principal.

1. **Navegue para o diretório raiz do projeto**:
   ```bash
   cd <RAIZ_DO_PROJETO>
   ```

2. **Execute os testes com o pytest usando Poetry**:
   ```bash
   poetry run pytest
   ```

3. **Saída Esperada**:
   Você verá um resumo dos testes executados, semelhante a este:
   ```plaintext
   ============================= test session starts =============================
   collected 8 items

   tests/test_invoices.py ........                                        [100%]

   ============================== 8 passed in 1.23s ==============================
   ```

---

## Dicas

- **Erro de Dependências**:
  Se encontrar problemas ao instalar dependências, tente atualizar o Poetry:
  ```bash
  pip install --upgrade poetry
  ```

- **Ambiente Virtual**:
  Certifique-se de ativar o ambiente virtual gerenciado pelo Poetry sempre que trabalhar no projeto.

- **Limpeza**:
  Para limpar os arquivos de fatura gerados, exclua o conteúdo da pasta `INVOICES_DIR` especificada no arquivo `config.py`.

- **Testes detalhados**:
  Caso queira ver um detalhamento maior durante os testes, utilize o comando `pytest -v`.

---

## Configurações

* `TODAY`: Data atual utilizada para filtrar as faturas.
* `SEED_URL`: URL do servidor para obter os dados iniciais.
* `INVOICE_URL`: URL do servidor para obter os arquivos das faturas.
* `INVOICES_DIR`: Diretório onde os arquivos das faturas serão salvos.
* `CSV_FULL_PATH_FILE`: Caminho completo do arquivo CSV que será gerado.
* `CSV_DELIMITER`: Delimitador utilizado no arquivo CSV.
* `CSV_ENCODING`: Codificação utilizada no arquivo CSV.
* `CSV_COLUMNS`: Colunas que serão incluídas no arquivo CSV.

## Dependências

* `csv`: Biblioteca para gerar arquivos CSV.
* `pytest`: Ferramenta de testes de métodos do script.
* `poetry`: Ferramenta de gerenciamento de dependências.
* `requests`: Biblioteca para fazer requisições ao servidor.
* `datetime`: Biblioteca para controle de datas.
* `concurrent`: Biblioteca para a otimização de downloads usando multi-threads.


***Se encontrar problemas ou tiver dúvidas, abra uma issue no repositório!***