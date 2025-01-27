# README

Este projeto é um raspador de dados de faturas que utiliza a biblioteca `requests` para fazer requisições ao servidor e a biblioteca `csv` para gerar um arquivo CSV com os dados das faturas.

## Arquivos do Projeto

* `pyproject.toml`: Este arquivo contém as dependências do projeto.
* `app/sync_scrapping.py`: Este arquivo contém a lógica principal do projeto, incluindo a função `main` que executa o processo de raspagem de dados.
* `app/config.py`: Este arquivo contém as configurações do projeto, incluindo as URLs do servidor e os caminhos dos arquivos.

## Funcionalidades

* Raspagem de dados de faturas do servidor
* Geração de um arquivo CSV com os dados das faturas
* Utilização de threads para download de arquivos em paralelo
* Utilização de um decorator para medir o tempo de execução das funções

## Funções

* `get_invoices_data`: Função que faz uma requisição ao servidor para obter os dados das faturas.
* `filter_invoices`: Função que filtra as faturas com base na data de vencimento.
* `save_invoices`: Função que salva os arquivos das faturas no diretório especificado.
* `generate_csv`: Função que gera um arquivo CSV com os dados das faturas.
* `main`: Função principal que executa o processo de raspagem de dados.

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
* `poetry`: Ferramenta de gerenciamento de dependências.
* `requests`: Biblioteca para fazer requisições ao servidor.
* `datetime`: Biblioteca para controle de datas.
* `concurrent`: Biblioteca para a otimização de downloads usando multi-threads.