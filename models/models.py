from datetime import datetime, timezone
from enum import Enum

import bcrypt
from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAlchEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserDepartment(Enum):
    """User role defined by departement team type"""

    MANAGEMENT = "MANAGEMENT"
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"


class User(Base):
    """User created, modified/updated and deleted by management"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAlchEnum(UserDepartment, name="user_department"), nullable=False)

    # Relationships
    clients = relationship("Client", back_populates="commercial_contact")
    contracts = relationship("Contract", back_populates="commercial_contact")
    events_as_support = relationship("Event", back_populates="support_contact")

    @staticmethod
    def hash_password(password: str) -> str:
        """Salt and hash the plain text password."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """Check if the hashed password matches the plain password."""
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.password.encode("utf-8"))


class Client(Base):
    """Client created, modified/updated by commercial"""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_update_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
    commercial_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")


class Contract(Base):
    """Contract created and updated by management,
    modified and filter accessed by commercial"""

    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="contracts")
    commercial_contact = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    """Event created by commercial for signed contract,
    updated by management for support assignation,
    updated and filter accessed by support"""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    _start_date = Column("start_date", DateTime, nullable=False)
    _end_date = Column("end_date", DateTime, nullable=False)
    support_contact_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String)

    # Relationships
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="events_as_support")

    # Getter for start_date to display the date as "17 Feb 2011 @ 5AM"
    @property
    def start_date(self):
        return self._start_date.strftime("%d %b %Y @ %I%p") if self._start_date else None

    # Setter for start_date to convert "17 Feb 2011 @ 5AM" to normal datetime 2011/02/17 05:00:00
    @start_date.setter
    def start_date(self, value):
        if isinstance(value, str):
            # Conversion "string" -> datetime
            self._start_date = datetime.strptime(value, "%d %b %Y @ %I%p")
        elif isinstance(value, datetime):
            self._start_date = value
        else:
            raise ValueError("start_date must be a datetime object or a formatted string")

    # Getter for end_date (see start_date)
    @property
    def end_date(self):
        return self._end_date.strftime("%d %b %Y @ %I%p") if self._end_date else None

    # Setter for end_date (see start_date)
    @end_date.setter
    def end_date(self, value):
        if isinstance(value, str):
            # Conversion "string" -> datetime
            self._end_date = datetime.strptime(value, "%d %b %Y @ %I%p")
        elif isinstance(value, datetime):
            self._end_date = value
        else:
            raise ValueError("end_date must be a datetime object or a formatted string")
