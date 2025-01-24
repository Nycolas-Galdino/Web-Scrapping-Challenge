import os
import logging

from datetime import datetime as dt


# General
TODAY = dt.today()


# Directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICES_DIR = os.path.join(CURRENT_DIR, 'faturas')

if not os.path.exists(INVOICES_DIR):
    os.makedirs(INVOICES_DIR)


# Urls
API_URL = 'https://rpachallengeocr.azurewebsites.net/'
SEED_URL = API_URL + 'seed'
INVOICE_URL = API_URL + 'invoices/{invoice_filename}'


# CSV
CSV_FILENAME = 'faturas.csv'
CSV_FULL_PATH_FILE = os.path.join(CURRENT_DIR, CSV_FILENAME)
CSV_DELIMITER = ';'
CSV_ENCODING = 'utf-8'
CSV_COLUMNS = ['Número da Fatura', 'Data da Fatura', 'URL da fatura']
