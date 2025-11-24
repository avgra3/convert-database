from convert_database_tool.utils.utils import getTablesToConvert, alterTables
from convert_database_tool.utils.constants import LOGGER, get_config_file, get_data_file
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
    args = parser.parse_args()
    if args.dbConfig:
        config_location()
        return
    if args.query:
        script_location()
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
