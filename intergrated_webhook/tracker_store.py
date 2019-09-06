from rasa.core.tracker_store import SQLTrackerStore
from typing import  Optional, Text
from rasa.core.broker import EventChannel
from rasa.core.domain import Domain

class MySQLDjangoTrackerStore(SQLTrackerStore):
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class SQLEvent(Base):
        from sqlalchemy import Column, Integer, String, Float, Text

        __tablename__ = "ari_nlu_events"

        id = Column(Integer, primary_key=True)
        sender_id = Column(String(255), nullable=False, index=True)
        type_name = Column(String(255), nullable=False)
        timestamp = Column(Float)
        intent_name = Column(String(255))
        action_name = Column(String(255))
        data = Column(Text)

    def __init__(
        self,
        domain: Optional[Domain] = None,
        url: Optional[Text] = None,
        dialect: Text = "mysql+pymysql",
        db: Text = "rasa.db",
        username: Text = None,
        password: Text = None
    ) -> None:
        super(MySQLDjangoTrackerStore, self).__init__(
            domain=domain,
            dialect=dialect,
            db=db,
            username=username,
            password=password)