from neil import NeilResult
from neil import NeilPool
from concurrent.futures import ThreadPoolExecutor


class Conversion:
    def __init__(self, dbPool: NeilPool):
        self.dbPool = dbPool
        self.log = self.dbPool.log

    def getTablesToConvert(self, script: str) -> list[str]:
        query_result: NeilResult = self.dbPool.execute_sql(sql=script)
        for err in query_result.errors:
            self.dbPool.log.critical(err)
        if query_result.returnedData is None:
            return []
        results: list[str] = [
            "".join((str(s) for s in sql)) for sql in query_result.returnedData
        ]
        return results

    def run_queries(self, queries: list[str]) -> None:
        with ThreadPoolExecutor(max_workers=self.dbPool.pool_size) as executor:
            _ = executor.map(self.dbPool.execute_sql, queries)

    def run_all(self, *, getting_sql_tables: str) -> None:
        tables_to_convert = self.getTablesToConvert(script=getting_sql_tables)
        if tables_to_convert is None or len(tables_to_convert) == 0:
            self.dbPool.log.warning("no data returned")
            return
        self.run_queries(
            queries=[
                sql
                for sql in tables_to_convert
                if sql.strip() != "" and sql.strip() != ";"
            ]
        )
