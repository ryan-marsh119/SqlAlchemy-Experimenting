from sqlalchemy import String, Uuid
from sqlalchemy import create_engine, select
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column

# The engine declares where the database is as well as the credentials to use it
engine = create_engine("postgresql://postgres:Coder119!@localhost:5435/userdb", echo=False)

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


    def __repr__(self) -> str:
        return f"User(id = {self.id!r}), name = {self.name!r}, email = {self.email!r}"
    
    def __str__(self) -> str:
        return f"User(id = {self.id!r}), name = {self.name!r}, email = {self.email!r}"
    
Base.metadata.create_all(engine)


def get_all(session: Session):
    stmt = select(Users)
    return session.scalars(stmt).all()

def get_by_id(session: Session, uuid: UUID):
    return session.get(Users, uuid)

def get_by_email(session: Session, email: str):
    return session.scalars(select(Users).where(Users.email == email)).one_or_none()

def add_user(session: Session, name: str, email: str):
    new_user = Users(name=name, email=email)
    session.add(new_user)
    session.commit()

def update_user(session: Session, id: UUID, name: str | None = None, email: str | None = None):
    u = session.get(Users, id)

    if u is not None:
        if name is not None:
            u.name = name

        if email is not None:
            u.email = email

        session.commit()

    else:
        print(f"No user with id {id} found.")

def delete_user(session: Session, id: UUID):
    user = session.get(Users, id)

    if user is not None:
        session.delete(user)
        session.commit()

    else:
        print(f"No user with id {id} found.")

# with Session(engine) as session:

#     new_user = "Aaron"
#     email = "aaron@email.com"

#     # add_user(session, new_user, email)

#     aaron_id = '77b88e48-6118-477a-8fe3-35f7b5803afc'

#     print(get_by_id(session, aaron_id))

#     new_email = "aaron@microsoft.com"

#     update_user(session, aaron_id, email=new_email)

#     print(get_by_id(session, aaron_id))

#     delete_user(session, aaron_id)

#     print(get_by_id(session, aaron_id))