
### Run migrations

```bash
# command for initial configuration, no need to run again
# cd pi-consulting/src
# alembic init migrations
# alembic revision --autogenerate -m "init"

# Undo migration. Use to undo a migration, can replace `-1` for revision code
alembic downgrade -1

# Make migrations: Use to make a migration
alembic revision --autogenerate -m "000x_action_model"

# apply migrate
alembic upgrade head

```