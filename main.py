from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import String, select, Uuid
import uuid

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


    def __repr__(self) -> str:
        return f"User(id = {self.id!r}), name = {self.name!r}, email = {self.email!r}"
    
def add_user(engine, name: str, email: str):
    session = Session(engine)

    new_user = Users(id=uuid.uuid4(), name=name, email=email)

    session.add(new_user)
    session.commit()
    session.close()

def get_all(engine):
    session = Session(engine)
    stmt = select(Users)

    return session.scalars(stmt)

def get_by_id(engine, id: str):
    session = Session(engine)

    return session.get(Users,id)

def update_user(engine, id: str, name: str = '', email: str = ''):
    session = Session(engine)

    stmt = session.execute(select(Users).filter_by(id=id)).scalar_one()

    if name != '':
        stmt.name = name

    if email != '':
        stmt.email = email
    
    session.commit()
    session.close()

def delete_user(engine, id: str):
    session = Session(engine)

    user = session.get(Users, id)

    session.delete(user)

    session.commit()
    session.close()


engine = create_engine("postgresql://postgres:Coder119!@localhost:5435/userdb", echo=False)
    
Base.metadata.create_all(engine)

# session = Session(engine)

# add_user(engine, 'Ryan456', 'notarealemail@ymail.com')

session = Session(engine)

get_user = get_by_id(engine, '7b6745e2-19ee-4984-b139-927bdff5e836')

print(get_user)

delete_user(engine, '7b6745e2-19ee-4984-b139-927bdff5e836')

get_user = get_by_id(engine, '7b6745e2-19ee-4984-b139-927bdff5e836')

print(get_user)