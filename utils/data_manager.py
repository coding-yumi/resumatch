import json
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EXPERIENCES_FILE = DATA_DIR / "experiences.json"
BACKUP_FILE = DATA_DIR / "experiences_backup.json"


def _ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not EXPERIENCES_FILE.exists():
        EXPERIENCES_FILE.write_text("[]", encoding="utf-8")


def _notify_corruption() -> None:
    try:
        import streamlit as st

        if not st.session_state.get("data_corruption_notified"):
            st.session_state.data_corruption_notified = True
            st.warning(
                "经历数据文件（experiences.json）已损坏，"
                "已自动备份为 data/experiences_backup.json 并重置为空列表。"
                "请检查备份文件后重新录入经历。"
            )
    except Exception:
        pass


def load_experiences() -> list:
    _ensure_data_file()
    try:
        with open(EXPERIENCES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("experiences.json root must be a JSON array")
        return data
    except (json.JSONDecodeError, ValueError):
        corrupted = EXPERIENCES_FILE.read_text(encoding="utf-8")
        BACKUP_FILE.write_text(corrupted, encoding="utf-8")
        EXPERIENCES_FILE.write_text("[]", encoding="utf-8")
        _notify_corruption()
        return []


def save_experiences(experiences: list) -> None:
    _ensure_data_file()
    with open(EXPERIENCES_FILE, "w", encoding="utf-8") as f:
        json.dump(experiences, f, ensure_ascii=False, indent=2)


def add_experience(exp_dict: dict) -> dict:
    experiences = load_experiences()
    if "id" not in exp_dict:
        exp_dict["id"] = str(uuid4())
    experiences.append(exp_dict)
    save_experiences(experiences)
    return exp_dict


def delete_experience(exp_id: str) -> bool:
    experiences = load_experiences()
    new_experiences = [e for e in experiences if e.get("id") != exp_id]
    if len(new_experiences) == len(experiences):
        return False
    save_experiences(new_experiences)
    return True
