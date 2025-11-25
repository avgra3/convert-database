from convert_database_tool.utils.constants import db_config_toml, LOGGER, db_config_file
from tomlkit import dumps, document


def update_field(field_name: str, value: str | int) -> None:
    current_config = db_config_toml()
    allowed_keys = [key.strip().lower() for key in current_config.keys()]
    if field_name.strip().lower() not in allowed_keys:
        LOGGER.warning(f"`{field_name.strip().lower()}` is not a valid field to update.")
        return
    current_config[field_name.strip().lower()] = value
    config_file = db_config_file()
    doc = document()
    doc.update({"database_config": current_config})
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(dumps(doc))
    LOGGER.info("Succesffully updated config.")
    LOGGER.info(f"Wrote to => `{config_file.as_posix()}`")

