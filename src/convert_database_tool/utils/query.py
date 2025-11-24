import mariadb
from multiprocessing import cpu_count, Process
from .constants import LOGGER
from logging import Logger


class Conversion:
    def __init__(self, dbCons: dict[str, any], log: Logger = LOGGER):
        self.pool_size = cpu_count() // 2
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
        for tup in queries:
            for q in tup:
                split_results = q.split(";")
                for split in split_results:
                    if split.strip() == "":
                        continue
                    try:
                        with mariadb.connect(**self.dbCons) as conn:
                            cur = conn.cursor()
                            cur.execute(split)
                    except Exception as e:
                        self.log.critical(
                            "An exception occured. Please review the error given"
                        )
                        self.log.critical(e)

    def run_alters_mp(self, alters: list[tuple[str]]):
        mp = []
        for chunk in self.__chunks(alters=alters):
            process = Process(target=self.run_queries, args=(chunk,))
            mp.append(process)
            process.start()

        for p in mp:
            p.join()
