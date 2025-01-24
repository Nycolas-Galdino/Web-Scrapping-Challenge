import os
import csv
import requests
from time import perf_counter
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor

from config import (
    TODAY, INVOICE_URL, SEED_URL, INVOICES_DIR,
    CSV_DELIMITER, CSV_ENCODING, CSV_COLUMNS, CSV_FULL_PATH_FILE
)


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f'\033[1;34mFunção "{func.__name__}" executada em {(end - start) * 1000:.2f}ms\033[0m')
        return result
    return wrapper


def get_invoices_data(session: requests.Session) -> list[dict]:
    """Retrieve invoice data from the server.

    Sends a POST request to the SEED_URL with specific data to obtain
    invoice information. The function raises an exception if the
    request fails and returns the JSON response as a list of dictionaries.

    Args:
        session (requests.Session): The session object used to make the request.

    Returns:
        list[dict]: A list of dictionaries containing invoice data.
    """

    data = {'sendHash': 'false'}
    response = session.post(SEED_URL, data=data)
    response.raise_for_status()
    return response.json()


def filter_invoices(invoices_data: list[dict]) -> list[dict]:
    """Filter invoices based on their due date.

    Filters out invoices whose due date is earlier than today from
    the provided list of invoice data. Only invoices with a due date
    on or after today are included in the result.

    Args:
        invoices_data (list[dict]): A list of dictionaries containing
        invoice data, where each dictionary has a 'duedate' key.

    Returns:
        list[dict]: A list of dictionaries for invoices with due dates
        on or after today.
    """

    return [
        x for x in invoices_data['data']
        if dt.strptime(x['duedate'], '%d-%m-%Y') >= TODAY
    ]


def download_invoice(session: requests.Session, invoice_filename: str) -> None:
    """Download the invoice file with the specified name.

    Request the invoice file with the name specified via GET and saves
    The content in the INVOICES_DIR folder.

    args:
        session (Requests.Session): The session used to make the request.
        invoice_filename (str): The file name of the invoice to be downloaded.
    """
    url = INVOICE_URL.format(invoice_filename=invoice_filename)
    response = session.get(url, timeout=10)
    response.raise_for_status()
    file_path = os.path.join(INVOICES_DIR, invoice_filename)
    with open(file_path, 'wb') as f:
        f.write(response.content)


def save_invoices(session: requests.Session, invoices_data: list[dict]) -> None:
    """Download all invoice files from the provided list of invoice data.

    Downloads the invoice files whose URLs are stored in the 'invoice' key
    in the dictionaries of the provided list. The files are saved in the
    INVOICES_DIR folder with the same name as the URL's last part.

    The function uses a ThreadPoolExecutor to download the files in parallel,
    with a maximum of 5 concurrent threads.

    Args:
        session (requests.Session): The session object used to make the requests.
        invoices_data (list[dict]): A list of dictionaries containing invoice
        data, where each dictionary has an 'invoice' key with the URL of the
        invoice.
    """
    filenames = [invoice['invoice'].split('/')[-1].strip() for invoice in invoices_data]
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(lambda filename: download_invoice(session, filename), filenames)


def generate_csv(invoices_data: list[dict]) -> None:
    """Generate a CSV file from the provided list of invoice data.

    The function takes the provided list of invoice data and generates
    a CSV file with the specified filename. The CSV file has the same
    columns as the invoice data, and the values are written in the same
    order. If the value is missing from the invoice data, an empty string
    is written instead.

    Args:
        invoices_data (list[dict]): A list of dictionaries containing invoice
        data, where each dictionary has the columns specified in the
        CSV_COLUMNS variable.
    """
    with open(CSV_FULL_PATH_FILE, 'w', newline='', encoding=CSV_ENCODING) as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(CSV_COLUMNS)
        for invoice in invoices_data:
            writer.writerow([invoice.get(col, '') for col in CSV_COLUMNS])


@measure_time
def main():
    """Run the entire process of getting invoice data, filtering them, downloading
    the corresponding files and generating a CSV file.

    The function uses a requests Session to make the requests to the server and
    a ThreadPoolExecutor to download the invoice files in parallel. The
    generate_csv function is used to generate a CSV file from the filtered
    invoice data.

    The function prints a message when the process is finished and the
    @measure_time decorator is used to measure the time it takes to run the
    function.
    """
    with requests.Session() as session:
        invoices_data = get_invoices_data(session)
        filtered_invoices = filter_invoices(invoices_data)
        save_invoices(session, filtered_invoices)
        generate_csv(filtered_invoices)
        print('\033[1;32mProcessamento concluído com sucesso!\033[0m')


if __name__ == '__main__':
    main()
