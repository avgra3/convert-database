import mariadb
from multiprocessing import cpu_count, Pool
from .constants import LOGGER
from logging import Logger


class Conversion:
    def __init__(self, dbCons: dict[str, any], log: Logger = LOGGER):
        self.pool_size = min(cpu_count() // 2, 16)
        self.log = log
        self.dbCons = dbCons

    def getTablesToConvert(self, script: str) -> list[tuple[str]]:
        results = []
        try:
            with mariadb.connect(**self.dbCons) as conn:
                cur = conn.cursor()
                cur.execute(script)
                results = cur.fetchall()
        except Exception as e:
            self.log.critical("An exception occured, please review the error given")
            self.log.critical(e)
        return results

    def __chunks(self, alters: list[tuple[str]]):
        for i in range(0, len(alters), self.pool_size):
            yield alters[i : i + self.pool_size]

    def run_queries(self, queries: list[tuple[str]]) -> None:
        pool = mariadb.ConnectionPool(
            pool_name=f"query_runner_{self.pool_number:02}",
            pool_size=1,
            **self.dbCons,
        )

        for sql_scripts in queries:
            split = sql_scripts.split(";")
            for split in split:
                if split.strip() == "":
                    continue
                try:
                    with pool.get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(statement=split)
                        cur.close()
                except mariadb.ProgrammingError as e:
                    self.log.warning(
                            "An exception occured."
                    )
                    self.log.warning("Exception occured while running:")
                    self.log.warning(split)
                    self.log.warning("Please review the error given.")
                    self.log.warning(e)
                except mariadb.Error as e:
                    error_message = "An occured while running the previous sql. Review the error message for detauls"
                    self.log.error(error_message)
                    self.log.error(e)

    def run_alters_mp(self, alters: list[tuple[str]]):
        max_workers = min(cpu_count() // 2, 16)
        with Pool(processes=max_workers) as pool:
            pool.map(self.run_queries, alters)

