from dataclasses import dataclass, asdict, field
from datetime import datetime
from uuid import uuid4

# 📝 Dataclass representing a journal entry
@dataclass
class JournalEntry:
    title: str
    content: str
    date: str = field(default_factory=lambda: datetime.now().isoformat())
    tags_list: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))