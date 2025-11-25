from convert_database_tool.utils.constants import get_data_file, LOGGER
from pathlib import Path


def update_query(file: Path) -> None:
    # get current config file location
    current_file = get_data_file(name="get_tables_to_convert.sql")
    # save old file with appended name of OLD and timestamp
    renamed_file = move_and_rename(
        src=current_file,
        target_dir=current_file.parent,
        new_name="get_tables_to_convert_old.sql",
    )
    LOGGER.info(f"Renamed previous sql to => `{renamed_file.as_posix()}`")
    # save new file to old's name sans OLD and timestamp
    with open("get_tables_to_convert.sql", "w") as f:
        f.write(file.read_text())
    LOGGER.info("Successfully updated file")


def move_and_rename(src: Path, target_dir: Path, new_name: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / new_name
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while dest.exists():
        candidate = f"{stem}_old{i if i > 1 else ''}{suffix}"
        dest = target_dir / candidate
        i += 1
    return src.rename(dest)
