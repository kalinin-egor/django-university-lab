# Car Rental Service

## Local setup

1. Copy the sample environment file and adjust if needed:
   ```bash
   cp .env.example .env
   ```
2. Start the PostgreSQL container:
   ```bash
   docker compose up -d
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a Django superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

The Django settings use the `POSTGRES_*` variables from the environment. When the Docker container is running with the default credentials from `.env.example`, migrations and the development server can connect to PostgreSQL at `127.0.0.1:5432`.
