from sqlalchemy import Column, DateTime, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func

# NOTE: This is very important or else you'd have errors in your migration without appropriate contraint naming which will cause
# migration(alembic) downgrade errors.

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata
    # id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid4())
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime(timezone=True), default=None, nullable=True)
    __name__: str

    # Generate __tablename__ automatically in plural form.
    # i.e 'Post' model will generate table name 'posts'
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
