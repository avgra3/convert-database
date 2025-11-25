from convert_database_tool.utils.utils import getTablesToConvert, alterTables
from convert_database_tool.utils.constants import LOGGER, get_config_file, get_data_file
from convert_database_tool.utils.update_config import update_field
from convert_database_tool.utils.update_sql import update_query
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="Database Conversion Tool",
        description="Make changes to every table in a database",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--db", help="Database name")
    group.add_argument(
        "-c",
        "--dbConfig",
        action="store_true",
        help="Flag to return location of dbConfig.toml",
    )
    group.add_argument(
        "-q",
        "--query",
        action="store_true",
        help="Get location of query ran by the app to make the update(s)",
    )
    group.add_argument(
        "-f",
        "--field_update",
        help="Update a field such as `username`, `password`, `hostname`, `port`",
    )
    group.add_argument(
        "-m",
        "--query_update",
        action="store_true",
        help="Update the SQL update file",
    )
    parser.add_argument(
        "-v",
        "--value",
        help="Field value or new SQL query file to set.",
    )
    args = parser.parse_args()
    if args.dbConfig:
        config_location()
        return
    if args.query:
        script_location()
        return
    if args.query_update:
        if args.value is None:
            LOGGER.warning("You did not provide a file to swap to")
            return
        update_query(file=args.value)
        return
    if args.field_update is not None:
        if args.value is not None:
            update_field(field_name=args.field_update, value=args.value)
        else:
            LOGGER.warning("You did not provide a value to change field to")
        return
    LOGGER.info("Starting process...")
    tables_to_alter = getTablesToConvert(database=args.db)
    alterTables(database=args.db, alters=tables_to_alter)
    LOGGER.info(
        "Finished. Please review the database and any errors which may have occurred."
    )


def config_location():
    file_location = get_config_file(name="dbConfig.toml")
    LOGGER.info(f"Location of dbConfig.toml => {file_location.as_posix()}")


def script_location():
    file_location = get_data_file(name="get_tables_to_convert.sql")
    LOGGER.info(f"Location of sql => {file_location.as_posix()}")


if __name__ == "__main__":
    main()
