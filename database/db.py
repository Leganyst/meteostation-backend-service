from sqlalchemy import create_engine

from config import Config

try:
    engine = create_engine(
        f"postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
        echo=True
    )
except Exception as e:
    print(e, " )))))))")
    