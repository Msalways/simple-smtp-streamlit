
from sqlalchemy import Column, Integer, String
from db.config import Base


class SMTPConfig(Base):
    __tablename__ = "smtp_config"
    id = Column(Integer,primary_key=True, default=1)
    smtp_host = Column(String,nullable=False)
    smtp_port = Column(Integer,nullable=False)
    smtp_email = Column(String,nullable=False)
    smtp_password = Column(String,nullable=False)