# The ODP Accounts API

Back-office API providing DOI related functions.

## Installation

### System dependencies

* Python 3.7

## Configuration

The system is configured using environment variables. For a local / non-containerised deployment,
these may be loaded from a `.env` file located in the project root directory. See `.env.example`
for an example configuration.

### Environment variables

- **`SERVER_ENV`**: deployment environment; `development` | `testing` | `staging` | `production`
- **`PATH_PREFIX`**: (optional) URL path prefix at which the API is mounted, e.g. `/api`
- **`DATABASE_URL`**: URL of the DOI Db, e.g. `postgresql://odp_user:pwd@host/odp_accounts`
- **`DATABASE_ECHO`**: set to `True` to emit SQLAlchemy database calls to stderr (default `False`)

## Development quick start

Install the Uvicorn ASGI server into the project's virtual environment:

    pip install uvicorn

Run the server:

    uvicorn accountsapi:app --reload
