# Data discrepancy checker

This task mirrors a system we recently built internally, and will give you an
idea of the problems we need to solve.

Every quarter, new company data is provided to us in PDF format. We need to use
an external service to extract this data from the PDF, and then validate it
against data we have on file from another source.

Complete the API so that:

A user can provide a PDF and a company name data is extracted from the PDF via
the external service and compared to the data stored on file a summary of the
data is returned, containing all fields from both sources, noting which fields
did not match.

A selection of example PDFs have been uploaded, and the PDF
extraction service has been mocked for use in `src/pdf_service.py` - DO NOT
EDIT THIS FILE. There is simple documentation of the service in
`PDF_SERVICE_DOCS.md`. You can treat this as just another microservice.

The existing data we have on file is available in the `data/database.csv` file.

Treat this code as if it will be deployed to production, following best
practices where possible.

## Setup using Poetry

The easiest way to set up the repository is to use `python-poetry`. The lock file
was generated using version `1.8.3`

1. Ensure `poetry` is installed
2. Run `make install`

## Setup without Poetry

Alternatively it's possible to `pip install` directly using the
`pyproject.toml` or `requirements.txt`.


## Completed Test: For Lantern

Hi! I completed the following tasks for this take-home test:

- Implemented the `/upload-pdf` endpoint to extract data from a provided PDF file using the mocked PDF service, compare
  it with the data stored in the database, and return a summary of the comparison.
- Added error handling for invalid filenames, missing company data in the PDF or database, and potential exceptions.
- Refactored the code to follow best practices, including:
    - Moving config settings to a separate `config.py` file using `pydantic-settings`.
    - Breaking out the db loading and data comparison logic.
    - Adding type hints to improve code readability.
- Wrote unit tests for the API endpoints and core functionality using `pytest` and `fastapi.TestClient`.
- Updated the `Makefile` to run with Docker.
- Dockerized the app so anyone can run it on any platform without potential issues. 

- To run the app using Docker, follow these steps:
    1. Make sure you have Docker (Or Orbastack for M Series Macs) installed on your system.
    2. Build the Docker image:
       ```
       make build
       ```
    3. Start the Docker container:
       ```
       make up
       ```
  The API will now be accessible at `http://localhost:8000`.
  To stop the container:
  ```
  make down
  ```
  To run the tests in the Docker container:
  ```
  make test
  ```

Some low-hanging improvements and additional features to consider as the complexity of the app grows:

- Implement user authentication and authorisation to secure the API endpoints.
- Add input validation and sanitisation to prevent potential security vulnerabilities.
- Use a real database, eg Postgres, instead of a CSV file.
- Implement a caching layer, eg Redis, to improve performance by reducing the number of requests to the PDF
  microservice and db.
- Add logging and monitoring to track errors, performance metrics, and usage patterns.
- Use a message queue to process PDF extraction and comparison tasks asynchronously and improve the responsiveness of
  the API.
- Upload the assets to a blob storage for better scalability.
- Keep documentation up to date and add more details about the data sources and how the API works.
- Add `pre-commit` hooks to automatically run code formatting with `black`, linting with `flake8`, and sorting imports
  with `isort` - To standardise the codebase across contributors.
- If using `pip` with Docker, create separate `requirements.txt` files for dev and prod environments to
  keep the production image lean and secure.
