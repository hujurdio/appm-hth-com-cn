from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://appm-hth.com.cn"
SAMPLE_KEYWORDS = ["华体会", "活动运营", "用户增长"]


@dataclass
class KeywordNote:
    """A note associated with a keyword, optionally linked to a URL."""
    keyword: str
    note: str
    url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def display(self) -> str:
        """Return a formatted single-line representation."""
        timestamp = self.created_at.strftime("%Y-%m-%d %H:%M")
        if self.url:
            return f"[{timestamp}] {self.keyword}: {self.note} ({self.url})"
        return f"[{timestamp}] {self.keyword}: {self.note}"


@dataclass
class KeywordNoteGroup:
    """A group of keyword notes sharing a common category or context."""
    category: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, url: Optional[str] = None) -> None:
        """Add a keyword note to this group."""
        self.notes.append(KeywordNote(keyword=keyword, note=note, url=url))

    def format_all(self, separator: str = "\n---\n") -> str:
        """Return all notes in the group as a formatted block."""
        lines = [f"Category: {self.category}"]
        lines.extend(note.display() for note in self.notes)
        return separator.join(lines)

    def filter_by_keyword(self, keyword: str) -> "KeywordNoteGroup":
        """Return a new group containing only notes matching the given keyword."""
        filtered = [n for n in self.notes if keyword.lower() in n.keyword.lower()]
        return KeywordNoteGroup(category=self.category, notes=filtered)


def build_sample_group() -> KeywordNoteGroup:
    """Create and return a KeywordNoteGroup with sample data."""
    group = KeywordNoteGroup(category="Marketing Insights")
    group.add_note(
        keyword="华体会",
        note="用户活跃度提升策略：结合社区活动和积分体系。",
        url=SAMPLE_URL,
    )
    group.add_note(
        keyword="活动运营",
        note="周期性主题活动有助于增强品牌认知，建议每两周一次。",
    )
    group.add_note(
        keyword="用户增长",
        note="通过裂变分享机制，单次活动能带来约20%的新用户增长。",
    )
    group.add_note(
        keyword="华体会",
        note="注意合规要求，所有用户数据需脱敏处理。",
        url=SAMPLE_URL,
    )
    return group


def print_report(group: KeywordNoteGroup) -> None:
    """Print a structured report of the keyword notes group."""
    print("=== Keyword Notes Report ===")
    print(group.format_all())
    print("=== End of Report ===")


def filter_and_display(group: KeywordNoteGroup, keyword: str) -> None:
    """Filter notes by keyword and print them."""
    filtered = group.filter_by_keyword(keyword)
    print(f"\nFiltered notes for '{keyword}':")
    if not filtered.notes:
        print("(No matches found.)")
    else:
        for note in filtered.notes:
            print(f"  - {note.display()}")


if __name__ == "__main__":
    sample = build_sample_group()
    print_report(sample)
    filter_and_display(sample, "华体会")