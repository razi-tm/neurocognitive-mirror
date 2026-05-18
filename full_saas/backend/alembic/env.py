from alembic import context
from app.core.db import Base
from app.models import entities

target_metadata = Base.metadata

def run_migrations_online():
    from sqlalchemy import create_engine
    from app.core.config import settings
    with create_engine(settings.database_url).connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction(): context.run_migrations()
run_migrations_online()
