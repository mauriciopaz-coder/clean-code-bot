"""User service module refactored to follow SOLID principles."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# --- Domain Model ---

@dataclass
class User:
    """Represents a user in the system."""

    name: str
    email: str
    age: int
    role: str


# --- Validation (Single Responsibility) ---

class UserValidator:
    """Validates user data before creation."""

    MIN_AGE = 0
    MAX_AGE = 150

    def validate(self, name: str, email: str, age: int) -> list[str]:
        """Return a list of validation error messages (empty if valid)."""
        errors: list[str] = []
        if not name:
            errors.append("Name cannot be empty.")
        if not email or "@" not in email:
            errors.append("A valid email address is required.")
        if not self.MIN_AGE <= age <= self.MAX_AGE:
            errors.append(f"Age must be between {self.MIN_AGE} and {self.MAX_AGE}.")
        return errors


# --- Notification (Interface Segregation + Dependency Inversion) ---

class Notifier(ABC):
    """Abstract interface for sending notifications."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Send a message to the given recipient."""


class EmailNotifier(Notifier):
    """Sends email notifications via SMTP."""

    def __init__(self, host: str, port: int, sender: str) -> None:
        self.host = host
        self.port = port
        self.sender = sender

    def send(self, recipient: str, message: str) -> bool:
        """Send an email to the recipient."""
        import smtplib
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.sendmail(self.sender, recipient, message)
            return True
        except smtplib.SMTPException:
            logger.error("Failed to send email to %s", recipient)
            return False


class LogNotifier(Notifier):
    """Logs notifications instead of sending them (useful for testing)."""

    def send(self, recipient: str, message: str) -> bool:
        logger.info("Notification to %s: %s", recipient, message)
        return True


# --- Persistence (Single Responsibility) ---

class UserLogger:
    """Handles logging of user-related events to a file."""

    def __init__(self, log_path: str = "users.log") -> None:
        self.log_path = Path(log_path)

    def log(self, message: str) -> None:
        """Append a message to the log file."""
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")


# --- User Repository (Single Responsibility) ---

@dataclass
class UserRepository:
    """In-memory storage for users with basic CRUD operations."""

    _users: list[User] = field(default_factory=list)

    def add(self, user: User) -> None:
        self._users.append(user)

    def remove(self, email: str) -> bool:
        """Remove a user by email. Returns True if found and removed."""
        for i, user in enumerate(self._users):
            if user.email == email:
                del self._users[i]
                return True
        return False

    def find_by_email(self, email: str) -> User | None:
        """Find a user by email."""
        return next((u for u in self._users if u.email == email), None)

    def find_by_role(self, role: str) -> list[User]:
        """Get all users with a given role."""
        return [u for u in self._users if u.role == role]

    def all(self) -> list[User]:
        """Return all users."""
        return list(self._users)

    def export_json(self, filepath: str) -> None:
        """Export all users to a JSON file."""
        data = [
            {"name": u.name, "email": u.email, "age": u.age, "role": u.role}
            for u in self._users
        ]
        Path(filepath).write_text(json.dumps(data, indent=2), encoding="utf-8")


# --- User Service (Orchestration with Dependency Injection) ---

class UserService:
    """High-level user management service.

    Dependencies are injected via the constructor (Dependency Inversion Principle),
    making the service easy to test and extend.
    """

    def __init__(
        self,
        repository: UserRepository,
        validator: UserValidator,
        notifier: Notifier,
        user_logger: UserLogger,
    ) -> None:
        self.repository = repository
        self.validator = validator
        self.notifier = notifier
        self.user_logger = user_logger

    def add_user(self, name: str, email: str, age: int, role: str) -> bool:
        """Validate, store, notify, and log a new user."""
        errors = self.validator.validate(name, email, age)
        if errors:
            for err in errors:
                logger.warning("Validation failed: %s", err)
            return False

        user = User(name=name, email=email, age=age, role=role)
        self.repository.add(user)
        self.notifier.send(email, f"Welcome {name}")
        self.user_logger.log(f"Added user: {name}")
        return True

    def delete_user(self, email: str) -> bool:
        """Remove a user and log the action."""
        removed = self.repository.remove(email)
        if removed:
            self.user_logger.log(f"Deleted user: {email}")
        return removed

    def broadcast(self, message: str) -> None:
        """Send a message to all users."""
        for user in self.repository.all():
            self.notifier.send(user.email, message)
