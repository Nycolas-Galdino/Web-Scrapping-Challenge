import os
import csv
import time
import requests

from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor

from config import (
    TODAY, INVOICE_URL, SEED_URL, INVOICES_DIR,
    CSV_DELIMITER, CSV_ENCODING, CSV_COLUMNS, CSV_FULL_PATH_FILE
)


def get_invoices_data() -> list[dict[str: str]]:
    data = {'sendHash': 'false'}
    response = requests.post(SEED_URL, data=data)

    if response.status_code != 200:
        print(f'[{response.status_code}] - {response.text}')
        response.raise_for_status()

    return response.json()


def filter_invoices(invoices_data: list[dict]) -> list[dict]:
    return (
        x for x in invoices_data['data']
        if dt.strptime(x['duedate'], '%d-%m-%Y') >= TODAY
    )


def get_invoice_file(invoice_filename: str) -> bytes:
    response = requests.get(INVOICE_URL.format(invoice_filename=invoice_filename))

    if response.status_code != 200:
        print(f'[{response.status_code}] - {response.text}')
        response.raise_for_status()

    return response.content


def fetch_invoice(invoice_filename: str) -> None:
    invoice_file = get_invoice_file(invoice_filename)
    with open(os.path.join(INVOICES_DIR, invoice_filename), 'wb') as f:
        f.write(invoice_file)


def save_invoices(invoices_data: list[dict[str, str]]) -> None:
    with ThreadPoolExecutor() as executor:
        filenames = [invoice['invoice'].split('/')[-1].strip() for invoice in invoices_data]
        executor.map(fetch_invoice, filenames)


def generate_csv(invoices_data: list[dict[str, str]]) -> None:
    with open(CSV_FULL_PATH_FILE, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(CSV_COLUMNS)
        for invoice in invoices_data:
            writer.writerow(invoice.values())


def main():
    start = time.time()
    invoices_data = get_invoices_data()
    invoices_data = filter_invoices(invoices_data)
    save_invoices(invoices_data)
    generate_csv(invoices_data)
    end = time.time()
    print('\033[1;32mArquivo salvo com sucesso!\033[0m')
    print(f'\033[1;36mTempo de execução: {(end - start)*10**3:.03f}ms\033[0m')


if __name__ == '__main__':
    main()
