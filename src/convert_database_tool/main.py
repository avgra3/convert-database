from convert_database_tool.utils.constants import DBCONS
from neil import NeilPool, NeilConfig
from convert_database_tool.utils.utils import run_conversions, verbose_level
from convert_database_tool.utils.constants import (
    LOGGER,
    get_config_file,
    get_data_file,
)
from convert_database_tool.utils.update_sql import update_query
from convert_database_tool.utils.update_config import update_field
import argparse
from pathlib import Path
import json


def main():
    parser = argparse.ArgumentParser(
        prog="Database Conversion Tool",
        description="Make changes to every table in a database",
        add_help=True,
    )
    # Shared Argument across other parsers
    shared_parser = argparse.ArgumentParser(add_help=False)
    shared_parser.add_argument(
        "--verbosity",
        type=verbose_level,
        required=False,
        default="info",
        help="Levels of logging: info, debug, warning, error, critical",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Information
    info_parser = subparsers.add_parser(
        "info",
        help="Information about your SQL or config file",
        parents=[shared_parser],
    )
    info_parser.add_argument(
        "-d", "--db", action="store_true", help="Current Database name"
    )
    info_parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="Return location of dbConfig.toml",
    )
    info_parser.add_argument(
        "-q",
        "--query",
        action="store_true",
        help="Get location of SQL query to run",
    )

    # Update items
    update_parser = subparsers.add_parser(
        "update",
        help="Information about your SQL or config file",
        parents=[shared_parser],
    )
    update_parser.add_argument(
        "-m",
        "--querry-update",
        type=Path,
        help="Update the SQL file with a file",
    )
    update_parser.add_argument(
        "-c",
        "--config-update",
        type=parse_dict,
        # type=str,
        # nargs="+",
        help="Update the config file with a new value: key=value",
    )

    # Run alterations
    run_parser = subparsers.add_parser(
        "run", help="Run the desired alterations"
    )
    run_parser.add_argument(
        "-d",
        "--database",
        type=str,
        default=DBCONS.get("database", ""),
        help="Database we are performing updates to. Defaults to database defined in config file.",
    )
    run_parser.add_argument(
        "-p",
        "--pool-size",
        type=int,
        default=3,
        help="Number of available connections for our pool.",
    )

    args = parser.parse_args()
    match args.command:
        case "info":
            if args.db:
                current_db()
            if args.config:
                config_location()
            if args.query:
                script_location()
        case "update":
            if args.querry_update:
                update_query(file=args.query)
            if args.config_update:
                map(
                    update_field,
                    args.config_update.keys(),
                    args.config_update.values(),
                )
        case "run":
            dbcons = DBCONS
            dbcons["database"] = args.database
            config: NeilConfig = NeilConfig(**dbcons)
            pool: NeilPool = NeilPool(
                conns=config, logger=LOGGER, pool_size=args.pool_size
            )
            run_conversions(dbPool=pool)
        case _:
            parser.print_help()


def parse_dict(input: str) -> dict:
    try:
        out = json.loads(
            input.replace("'", '"')
            .replace("True", "true")
            .replace("False", "false")
        )
        return out
    except Exception as e:
        LOGGER.critical(f"Unable to parse input: `{input}`")
        LOGGER.critical(e)
        return {}


def current_db():
    LOGGER.info(f"Current db: {DBCONS['database']}")


def config_location():
    file_location = get_config_file(name="dbConfig.toml")
    LOGGER.info(f"Location of dbConfig.toml => {file_location.as_posix()}")


def script_location():
    file_location = get_data_file(name="get_tables_to_convert.sql")
    LOGGER.info(f"Location of sql => {file_location.as_posix()}")


if __name__ == "__main__":
    main()
