from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUERY_FILE = PROJECT_ROOT / "sql" / "monthly_sales.sql"


if __name__ == "__main__":
    query = QUERY_FILE.read_text(encoding="utf-8")
    duckdb.sql(query).show()