import os
import pytest
import requests

from datetime import datetime as dt
from datetime import timedelta as td
from unittest.mock import MagicMock, patch, mock_open

from app.main import (
    get_invoices_data,
    filter_invoices,
    download_invoice,
    save_invoices,
    generate_csv,
    main
)

# Mock constantes
from app.config import (
    INVOICES_DIR,
    CSV_ENCODING,
    CSV_FULL_PATH_FILE
)


@pytest.fixture
def mock_session():
    with requests.Session() as session:
        yield session


@patch("requests.Session.post")
def test_get_invoices_data(mock_post, mock_session):
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": 1, "duedate": "28-01-2025"}]}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    invoices = get_invoices_data(mock_session)
    assert isinstance(invoices, dict)
    assert "data" in invoices


@patch("requests.Session.post")
def test_get_invoices_data_error(mock_post, mock_session):
    mock_post.side_effect = requests.exceptions.HTTPError("Server Error")

    with pytest.raises(requests.exceptions.HTTPError):
        get_invoices_data(mock_session)


def test_filter_invoices():
    invoices_data = {
        # Ajuste as datas para os testes conforme preferir
        "data": [
            {"id": 1, "duedate": (dt.today() - td(1)).strftime('%d-%m-%Y'), "invoice": "http://example.com/invoice1"},
            {"id": 2, "duedate": (dt.today() + td(1)).strftime('%d-%m-%Y'), "invoice": "http://example.com/invoice2"},
        ]
    }
    filtered = filter_invoices(invoices_data)
    print(filtered)
    assert len(filtered) == 1
    assert filtered[0]["id"] == 2


@patch("requests.Session.get")
def test_download_invoice(mock_get, mock_session):
    mock_response = MagicMock()
    mock_response.content = b"File content"
    mock_get.return_value = mock_response

    with patch("builtins.open", mock_open()) as mocked_file:
        download_invoice(mock_session, "test_invoice.pdf")
        mocked_file.assert_called_with(os.path.join(INVOICES_DIR, "test_invoice.pdf"), "wb")
        mocked_file().write.assert_called_once_with(b"File content")


@patch("requests.Session.get")
def test_download_invoice_error(mock_get, mock_session):
    mock_get.side_effect = requests.exceptions.HTTPError("Download Error")

    with pytest.raises(requests.exceptions.HTTPError):
        download_invoice(mock_session, "test_invoice.pdf")


@patch("app.main.download_invoice")
def test_save_invoices(mock_download_invoice, mock_session):
    invoices_data = [
        {"invoice": "http://example.com/invoices/invoice1.pdf"},
        {"invoice": "http://example.com/invoices/invoice2.pdf"},
    ]

    save_invoices(mock_session, invoices_data)
    assert mock_download_invoice.call_count == len(invoices_data)


@patch("builtins.open", new_callable=mock_open)
def test_generate_csv(mock_file):
    invoices_data = [
        {"id": 1, "duedate": "27-01-2025", "URL da fatura": "invoice1.pdf"},
        {"id": 2, "duedate": "28-01-2025", "URL da fatura": "invoice2.pdf"},
    ]

    generate_csv(invoices_data)

    mock_file.assert_called_once_with(CSV_FULL_PATH_FILE, "w", newline="", encoding=CSV_ENCODING)
    handle = mock_file()
    handle.write.assert_called()


@patch("app.main.get_invoices_data")
@patch("app.main.filter_invoices")
@patch("app.main.save_invoices")
@patch("app.main.generate_csv")
def test_main(mock_generate_csv, mock_save_invoices, mock_filter_invoices, mock_get_invoices_data, mock_session):
    mock_get_invoices_data.return_value = {
        "data": [
            {"id": 1, "duedate": "28-01-2025", "invoice": "http://example.com/invoice1.pdf"},
        ]
    }
    mock_filter_invoices.return_value = mock_get_invoices_data.return_value["data"]

    main()

    mock_get_invoices_data.assert_called_once()
    mock_filter_invoices.assert_called_once()
    mock_save_invoices.assert_called_once()
    mock_generate_csv.assert_called_once()
