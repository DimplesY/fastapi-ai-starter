#!/bin/bash
msg=${1:-"auto migration"}
echo "Generating alembic migration: '$msg'"
alembic revision --autogenerate -m "$msg"
status=$?
if [ $status -eq 0 ]; then
  echo "Migration generated successfully."
else
  echo "Alembic failed. Check your model/database."
  exit $status
fi
