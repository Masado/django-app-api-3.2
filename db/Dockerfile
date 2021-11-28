FROM postgres:13.0-alpine

RUN echo "Postgres is building"

COPY ./db-groundwork.sql db-groundwork.sql
RUN psql -U next_django next_django_dev < db-groundwork.sql