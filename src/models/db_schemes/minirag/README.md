## Run Alembic Migration

###  Configuration


```bash
cp alembic.ini.example alembic.ini
```

- Update the `alembic.ini` with your database credentials (`sqlalchemy.url`)

### Upgrade the database

```bash
alembic upgrafe head
```