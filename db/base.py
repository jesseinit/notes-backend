from uuid import uuid4

import inflect
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=lambda: uuid4().hex
    )
    __name__: str

    # Generate __tablename__ automatically in plural form.
    # i.e 'Post' model will generate table name 'posts'
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
