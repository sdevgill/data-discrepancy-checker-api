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

--------------------------------------------------------------------------------------

## Completed Test

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

### Setup using Docker

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

### API Endpoint

The API has a single endpoint for uploading a PDF and comparing its data with the database:

- `POST /upload-pdf`
    - Request body: The PDF file to upload (form-data)
    - Response: A JSON object containing the company name and a summary of the data comparison

Example response:

```json
{
  "company_name": "RetailCo",
  "summary": {
    "Company Name": {
      "database": "RetailCo",
      "pdf": "RetailCo",
      "match": true
    }
  }
}
```

### Testing the API

You can use Postman or cURL to test the `/upload-pdf` endpoint.

#### Postman

1. Create a new POST request in Postman
2. Set the request URL to `http://localhost:8000/upload-pdf`
3. In the "Body" tab, select "form-data"
4. Add a new key named "file" and set its type to "File"
5. Select the PDF file you want to upload
6. Click "Send" to make the request

#### cURL

Run the following command in your terminal, replacing `<path_to_pdf>` with the path to your PDF file:

```bash
curl -X POST -F "file=@<path_to_pdf>" http://localhost:8000/upload-pdf
```

For example:

```bash
curl -X POST -F "file=@assets/retailco.pdf" http://localhost:8000/upload-pdf
```

### Final Comments

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
- Set up a CI/CD pipeline to automate testing, building, and deployment processes. Use different envs for test, dev, and
  prod.

--------------------------------------------------------------------------------------

## Pair Programming - Task 2

Now that we have an API for checking the discrepancies between the database and company PDFs, we want to expand on our
application.

- The data in the database is sourced from an external API, which we pull data from on a weekly basis. This is done
  using separate tools and a separate codebase.
- If there are discrepancies between the PDF and the database, the user of our application needs a way to amend the
  value.

### The Task

Add an API endpoint that allows users to modify the data in the database if there is a discrepancy against the PDF.

- Discuss what data we need to store and its shape
- The data can be stored in-memory for the purposes of the exercise. It does not have to be written into a file or DB,
  but you may choose to do that.

### Task 2 Comments

For Task 2, we implemented a new API endpoint that allows users to modify the data in the database when there is a
discrepancy against the PDF. Here's what we did and why:

- New API Endpoint:
  We added a new endpoint /update-db to handle database updates. This endpoint accepts POST requests with the following
  parameters:

    - company_name: The name of the company to update
    - field: The field to be updated
    - new_value: The new value for the field

We chose this structure because it allows for flexible updates to any field in the database, making it easy to correct
discrepancies as they are found.

- Data Storage:
  For this exercise, we continued to use the CSV file (data/database.csv) as our database. In a production environment,
  we
  would recommend using a proper database system for better performance, concurrency control, and data integrity.
  However,
  using the CSV file allows us to maintain consistency with the existing implementation and avoid introducing new
  dependencies for this task.

- Update Function:
  We implemented an update function that handles the logic for updating the database. This function:

    - Checks if the company exists in the database
    - Updates the specified field with the new value
    - Saves the updated data back to the CSV file

- Error Handling:
  We added appropriate error handling to deal with cases such as:

- Company not found in the database
- Invalid field names
- General exceptions during the update process

For future improvements:

- Implementing authentication and authorization to ensure only authorized users can make changes to the database
- Adding a logging system to track all changes made to the database
- Implementing a more robust database solution for better data management and performance
- Adding validation rules for the updated data to ensure data integrity

To test the new endpoint, you can use cURL or Postman:

```bash
curl -X POST "http://localhost:8000/update-db?company_name=RetailCo&field=Revenue&new_value=1000000"```
```
