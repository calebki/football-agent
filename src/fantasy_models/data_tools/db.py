import duckdb
from pathlib import Path

DB_PATH = Path("data/fantasy.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def init_db():
    """Initialize master player identity and weekly raw projections tables"""
    with get_connection() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id VARCHAR PRIMARY KEY,
                first_name VARCHAR,
                last_name VARCHAR,
                position VARCHAR
            )
    """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS weekly_projections (
                player_id VARCHAR REFERENCES players(player_id),
                season INT NOT NULL,
                week INT NOT NULL,
                team VARCHAR,
                opponent VARCHAR,

                -- Passing
                proj_pass_yds FLOAT DEFAULT 0.0,
                proj_pass_td FLOAT DEFAULT 0.0,
                proj_pass_int FLOAT DEFAULT 0.0,

                -- Rushing
                proj_rush_yds FLOAT DEFAULT 0.0,
                proj_rush_td FLOAT DEFAULT 0.0,

                -- Receiving
                proj_rec FLOAT DEFAULT 0.0,
                proj_rec_yds FLOAT DEFAULT 0.0,
                proj_rec_td FLOAT DEFAULT 0.0,

                -- Turnovers
                proj_fum_lost FLOAT DEFAULT 0.0,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (player_id, season, week)
            )
        """)


if __name__ == "__main__":
    init_db()
    print("DuckDB initialized successfully at data/fantasy.duckdb")
