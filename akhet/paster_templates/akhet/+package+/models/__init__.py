import logging

import sqlahelper
import sqlalchemy as sa
import sqlalchemy.orm as orm
import transaction

log = logging.getLogger(__name__)

Base = sqlahelper.get_base()
Session = sqlahelper.get_session()


#class MyModel(Base):
#    __tablename__ = "models"
#
#    id = sa.Column(sa.Integer, primary_key=True)
#    name = sa.Column(sa.Unicode(255), nullable=False)
