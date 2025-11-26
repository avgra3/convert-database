WITH get_all AS (
(SELECT
		"" AS table_name,
    SCHEMA_NAME,
    CONCAT('ALTER DATABASE `', SCHEMA_NAME, '` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;') AS sql_command
 FROM information_schema.SCHEMATA
 WHERE SCHEMA_NAME = @dbName
   AND (DEFAULT_CHARACTER_SET_NAME <> 'utf8mb4'
        OR DEFAULT_COLLATION_NAME <> 'utf8mb4_unicode_520_ci')
)

UNION ALL

(SELECT
		TABLE_NAME,
    TABLE_SCHEMA,
    CONCAT_WS('\n',
        CONCAT('ALTER TABLE `', TABLE_SCHEMA, '`.`', TABLE_NAME, '` ENGINE = MyISAM ROW_FORMAT=DYNAMIC PAGE_CHECKSUM=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;'),
        CONCAT('ALTER TABLE `', TABLE_SCHEMA, '`.`', TABLE_NAME, '` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;'),
        CONCAT('OPTIMIZE TABLE `', TABLE_SCHEMA, '`.`', TABLE_NAME, '`;')
    ) AS sql_command
 FROM information_schema.TABLES
 WHERE TABLE_SCHEMA = "<DATABASE_NAME>"
   AND TABLE_TYPE = 'BASE TABLE'
   AND (TABLE_COLLATION <> 'utf8mb4_unicode_520_ci'
        OR ENGINE <> 'MyISAM')
	 AND ENGINE NOT IN('CONNECT', 'FEDERATED')
)
UNION ALL
(SELECT
		TABLE_NAME,
    TABLE_SCHEMA,
    CONCAT(
        'ALTER TABLE `', TABLE_SCHEMA, '`.`', TABLE_NAME, '`\n    ',
        GROUP_CONCAT(
            CONCAT(
                'MODIFY COLUMN `', COLUMN_NAME, '` ',
                COLUMN_TYPE,
                ' CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci',
                IF(IS_NULLABLE = 'NO', ' NOT NULL', ''),
                IF(COLUMN_DEFAULT IS NOT NULL,
                   CONCAT(' DEFAULT ',
                          IF(COLUMN_DEFAULT REGEXP '^[0-9]+$|^CURRENT_TIMESTAMP$|^NULL$',
                             COLUMN_DEFAULT,
                             CONCAT("'", REPLACE(COLUMN_DEFAULT, "'", "\\'"), "'"))),
                   ''),
                IF(EXTRA != '', CONCAT(' ', EXTRA), '')
            )
            ORDER BY ORDINAL_POSITION
            SEPARATOR ',\n    '
        ),
        ';'
    ) AS sql_command
 FROM information_schema.COLUMNS
 WHERE TABLE_SCHEMA = "<DATABASE_NAME>"
   AND (CHARACTER_SET_NAME <> 'utf8mb4'
   OR COLLATION_NAME <> 'utf8mb4_unicode_520_ci')
 GROUP BY TABLE_SCHEMA, TABLE_NAME
)
)
SELECT GROUP_CONCAT(sql_command ORDER BY sql_command DESC SEPARATOR "; ") AS combined
FROM get_all
WHERE get_all.table_name NOT LIKE "000_%"
GROUP BY get_all.SCHEMA_NAME, get_all.table_name;
