from collections import OrderedDict

import pytest
from fastapi.testclient import TestClient

from src.main import app, compare_data, load_database

client = TestClient(app)


class TestAPI:
    """
    API Tests for the PDF data discrepancy checker
    """

    def test_root_endpoint(self):
        """
        Test the root endpoint is working and returns the correct message.
        """
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Welcome to the Data Discrepancy Checker API"
        }

    def test_upload_pdf_valid(self):
        """
        Test uploading a valid PDF file and check for correct processing.
        """
        with open("assets/retailco.pdf", "rb") as pdf_file:
            response = client.post(
                "/upload-pdf",
                files={"file": ("retailco.pdf", pdf_file, "application/pdf")},
            )
            assert response.status_code == 200
            result = response.json()
            assert result["company_name"] == "RetailCo"
            assert "summary" in result

    def test_upload_pdf_invalid_filename(self):
        """
        Test uploading a PDF file with an invalid filename.
        """
        with open("assets/retailco.pdf", "rb") as pdf_file:
            response = client.post(
                "/upload-pdf",
                files={"file": ("invalid.pdf", pdf_file, "application/pdf")},
            )
            assert response.status_code == 400
            assert response.json() == {"detail": "Invalid filename provided"}

    def test_load_database(self):
        """
        Test that the database is loaded correctly.
        """
        database = load_database()
        assert not database.empty
        assert "Company Name" in database.columns

    def test_compare_data_with_missing_fields(self):
        """
        Test the data comparison logic for cases with missing fields in PDF and database.
        """
        db_data = {
            "Company Name": "RetailCo",
            "Location": "Chicago",
            "Debt (in millions)": 100,
            "Net Income Margin (%)": 5.0,
            "CEO": None,
            "Number of Employees": None,
        }

        pdf_data = {
            "Company Name": "RetailCo",
            "Debt (in millions)": 110,
        }

        expected_summary = OrderedDict(
            [
                (
                    "Company Name",
                    {"database": "RetailCo", "pdf": "RetailCo", "match": True},
                ),
                (
                    "Debt (in millions)",
                    {"database": 100, "pdf": 110, "match": False},
                ),
                (
                    "Location",
                    {"database": "Chicago", "pdf": None, "match": False},
                ),
                (
                    "Net Income Margin (%)",
                    {"database": 5.0, "pdf": None, "match": False},
                ),
                (
                    "CEO",
                    {"database": None, "pdf": None, "match": True},
                ),
                (
                    "Number of Employees",
                    {"database": None, "pdf": None, "match": True},
                ),
            ]
        )

        assert compare_data(db_data, pdf_data) == expected_summary

    def test_compare_data_with_additional_fields(self):
        """
        Test the data comparison logic for cases with additional fields in PDF.
        """
        db_data = {
            "Company Name": "RetailCo",
            "Location": "Chicago",
            "Debt (in millions)": 100,
        }

        pdf_data = {
            "Company Name": "RetailCo",
            "Location": "Chicago, IL",
            "Debt (in millions)": 110,
            "Extra Field": "Extra Value",
        }

        expected_summary = OrderedDict(
            [
                (
                    "Company Name",
                    {"database": "RetailCo", "pdf": "RetailCo", "match": True},
                ),
                (
                    "Location",
                    {"database": "Chicago", "pdf": "Chicago, IL", "match": False},
                ),
                (
                    "Debt (in millions)",
                    {"database": 100, "pdf": 110, "match": False},
                ),
                (
                    "Extra Field",
                    {"database": None, "pdf": "Extra Value", "match": False},
                ),
            ]
        )

        assert compare_data(db_data, pdf_data) == expected_summary


if __name__ == "__main__":
    pytest.main()
