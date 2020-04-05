class SqlQueries:
    """
    Contains SQL queries to run.

    Attributes
    ----------
    imm_dem_table_insert : str
        Immigration_demographic table insert query
    city_table_insert : str
        City table insert query
    entry_port_table_insert : str
        Entry port table insert query
    state_table_insert : str
        State table insert query
    """
    imm_dem_table_insert = ("""
        SELECT d.City, d.State, d.`State Code`, i.`Travel Mode`,
               i.Gender, d.`Foreign-born`, d.Race, i.`Visa Type`
        FROM imm_data i
        JOIN dem_data d ON d.`State Code` = i.`Dest State`
    """)

    city_table_insert = ("""
        SELECT DISTINCT City, State, `State Code`, Race
        FROM dem_data
        ORDER BY State
    """)

    entry_port_table_insert = ("""
        SELECT DISTINCT `Entry Port`,
               CAST(`Travel Mode` AS INT), `Dest State`, `Visa Type`
        FROM imm_data
        WHERE `Dest State` != "null"
        ORDER BY 1
    """)

    state_table_insert = ("""
        SELECT DISTINCT State,
               CAST(SUM(`Male Population`) AS INT) AS `Male Pop Total`,
               CAST(SUM(`Female Population`) AS INT) AS `Fem Pop Total`,
               CAST(SUM(`Foreign-born`) AS INT) AS `Foreign-born Tot`
        FROM dem_data
        GROUP BY 1
        ORDER BY State, `Foreign-born tot` DESC
    """)
