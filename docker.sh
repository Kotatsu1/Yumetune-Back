docker run -d \
  --name yumetune-pg \
  --restart always \
  -e POSTGRES_USER=kotatsu \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=yumetune \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:latest
