from typing import Text
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, update
from sqlalchemy.orm import Session, registry, relationship

engine = create_engine('sqlite+pysqlite:///:memory:', future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Objeto que representa la tabla User en la base de datos
class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    def __repr__(self):
        return f'User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})'

Base.metadata.create_all(engine)

# Anadimos dos registros a la tabla User
with Session(engine) as session:
    session.execute(
        insert(User),
        [
            {'name': 'sandy', 'fullname': 'Sandy Cheeks'},
            {'name':'spongebob', 'fullname':'Spongebob Squarepants'},
            {'name': 'patrik', 'fullname': 'Patrick Star'},      
        ]
    )
    session.commit()

print("\nRealizamos un select en todos los registros de la tabla User")
with Session(engine) as session:
    stmt = select(User)
    for row in session.execute(stmt):
        print(row)

print("\nRealizamos un select en los registros de la tabla User que tengan un valor en el campo 'name' equivalente a 'spongebob'")
with Session(engine) as session:
    stmt = select(User).where(User.name=='spongebob')
    for row in session.execute(stmt):
        print(row)
    

print("\nRealizamos un select en los registros de la tabla User que tengan un valor en el campo 'name' equivalente a 'spongebob', ")
print("y eliminamos los registros de la base de datos que arrojo el select")
with Session(engine) as session:
    stmt = select(User).where(User.name=='spongebob')
    for row in session.execute(stmt):
        session.delete(row[0])

    # Imprimimos los registros actualizados de la tabla    
    stmt = select(User)
    for row in session.execute(stmt):
        print(row)

    session.commit()

print("\nActualizamos los registros de la tabla User que contegan 'patrik' en el campo 'name', ")
print("modifcando el valor de 'name' de 'patrik' a 'patrick'")
with Session(engine) as session:
    stmt = (
    update(User).
    where(User.name=='patrik').
    values(name='patrick')
    )
    session.execute(stmt)
    
    # Imprimimos los registros actualizados de la tabla    
    stmt = select(User)
    for row in session.execute(stmt):
        print(row)
    session.commit()

print("\nRealizamos un select en todos los registros de la tabla User y ordenamos en base al campo 'fullname'")
with Session(engine) as session:
    stmt = select(User).order_by(User.fullname)
    for row in session.execute(stmt):
        print(row)