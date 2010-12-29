import pyramid_sqla as psa
import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
import transaction

Base = declarative.declarative_base()

#class MyModel(Base):
#    __tablename__ = 'models'
#    id = sa.Column(sa.Integer, primary_key=True)
#    name = sa.Column(sa.Unicode(255), nullable=False)
