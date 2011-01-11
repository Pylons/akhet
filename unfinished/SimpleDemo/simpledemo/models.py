import pyramid_sqla as psa
import sqlalchemy as sa
import sqlalchemy.orm as orm
import transaction

Base = psa.get_base()
Session = psa.get_session()

class Page(Base):
    __tablename__ = 'pages'

    title = sa.Column(sa.String, primary_key=True)
    content = sa.Column(sa.Text, nullable=False)
