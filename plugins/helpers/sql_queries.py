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
        SELECT d.city, d.state, d.state_code, i.travel_mode,
               i.gender, d.foreign_born, d.race, i.visa_type
        FROM staging_imm i
        JOIN staging_dem d ON d.state_code = i.dest_state
    """)

    city_table_insert = ("""
        SELECT DISTINCT city, state, state_code, race
        FROM staging_dem
        ORDER BY state
    """)

    entry_port_table_insert = ("""
        SELECT DISTINCT entry_port,
               CAST(travel_mode AS INT), dest_state, visa_type
        FROM staging_imm
        WHERE dest_state != "null"
        ORDER BY 1
    """)

    state_table_insert = ("""
        SELECT DISTINCT state,
               CAST(SUM(male_pop) AS INT),
               CAST(SUM(female_pop) AS INT),
               CAST(SUM(foriegn_born) AS INT)
        FROM staging_dem
        GROUP BY 1
        ORDER BY 1, 4 DESC
    """)
