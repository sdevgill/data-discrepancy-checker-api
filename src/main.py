from collections import OrderedDict

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from src.config import settings
from src.pdf_service import PdfService

app = FastAPI()

DATABASE_FILE = settings.DATABASE_FILE
PDF_SERVICE_KEY = settings.PDF_SERVICE_KEY
FILE_NAME_TO_PATH = settings.FILE_NAME_TO_PATH

pdf_service = PdfService(key=PDF_SERVICE_KEY)


def load_database() -> pd.DataFrame:
    """
    Load the database from a CSV file.

    Raises:
        RuntimeError: If the database file cannot be loaded.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        return pd.read_csv(DATABASE_FILE)
    except Exception as e:
        raise RuntimeError(f"Error loading database: {e}") from e


def compare_data(
    db_data: dict[str, str | int | float | None],
    pdf_data: dict[str, str | int | float | None],
) -> OrderedDict[str, dict[str, str | int | float | None]]:
    """
    Compare data between the database and the extracted PDF data.

    Args:
        db_data: Data from the database.
        pdf_data: Data extracted from the PDF.

    Returns:
        OrderedDict: A comparison summary of the two data sources, maintaining
        the order of fields as they appear in the PDF.
    """
    summary = OrderedDict()

    # Add fields from pdf_data first to maintain their order
    for field, pdf_value in pdf_data.items():
        db_value = db_data.get(field)
        match = db_value == pdf_value or (db_value is None and pdf_value is None)
        summary[field] = {
            "database": db_value,
            "pdf": pdf_value,
            "match": match,
        }

    # Add remaining fields from db_data that are not in pdf_data
    for field, db_value in db_data.items():
        if field not in summary:
            summary[field] = {
                "database": db_value,
                "pdf": None,
                "match": db_value is None,
            }

    return summary


def save_data_to_db(database_df: pd.DataFrame) -> None:
    """
    Save the DataFrame to a CSV file.

    Args:
        database_df (pd.DataFrame): The DataFrame to be saved.

    Returns:
        None
    """
    database_df.to_csv(DATABASE_FILE, index=False)


def update(
    database_df: pd.DataFrame, company_name: str, field: str, new_value: str
) -> None:
    """
    Update a specific field for a company in the DataFrame.

    Args:
        database_df (pd.DataFrame): The DataFrame containing the company data.
        company_name (str): The name of the company to update.
        field (str): The field to be updated.
        new_value (str): The new value for the field.

    Raises:
        HTTPException: If the company name is not found in the DataFrame.

    Returns:
        None
    """
    if not database_df["Company Name"].isin([company_name]).any():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid '{company_name}' not found",
        )

    database_df.loc[database_df["Company Name"] == company_name, field] = new_value
    save_data_to_db(database_df)


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)) -> JSONResponse:
    """
    Upload a PDF and compare its data with the database.

    Args:
        file: The uploaded PDF file.

    Raises:
        HTTPException: If any errors occur during processing.

    Returns:
        JSONResponse: The result of the data comparison.
    """
    try:
        original_filename = file.filename.lower()
        if original_filename not in FILE_NAME_TO_PATH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename provided",
            )

        mapped_file_path = FILE_NAME_TO_PATH[original_filename]

        try:
            extracted_data = pdf_service.extract(file_path=mapped_file_path)
        except FileNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        database = load_database()
        company_name = extracted_data.get("Company Name")

        if not company_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company name not found in the PDF",
            )

        db_data = database[database["Company Name"] == company_name]
        if db_data.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for company: {company_name}",
            )

        db_data = db_data.iloc[0].to_dict()

        summary = compare_data(db_data, extracted_data)
        return JSONResponse(content={"company_name": company_name, "summary": summary})

    except HTTPException:  # Pass through HTTP exceptions correctly
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/update-db")
async def update_db(company_name: str, field: str, new_value: str) -> JSONResponse:
    """
    Update a specific field for a company in the database.

    Args:
        company_name (str): The name of the company to update.
        field (str): The field to be updated.
        new_value (str): The new value for the field.

    Raises:
        HTTPException: If an error occurs while updating the database.

    Returns:
        JSONResponse: A JSON response indicating the success of the update.
    """
    try:
        database_df = load_database()
        update(database_df, company_name, field, new_value)
        return JSONResponse(content={"message": "DB updated successfully"})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the database: {str(e)}",
        )


@app.get("/")
async def read_root() -> dict[str, str]:
    """
    Read the root endpoint.

    Returns:
        dict[str, str]: A welcoming message.
    """
    return {"message": "Welcome to the Data Discrepancy Checker API"}
