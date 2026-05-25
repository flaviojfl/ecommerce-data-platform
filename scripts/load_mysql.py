
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATA_DIR = Path("data/raw/olist")

CSV_TO_TABLE = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
}


def get_engine():
    """Cria a engine de conexão com o MySQL (via localhost:3307)."""
    user = os.getenv("MYSQL_USER", "spark_user")
    password = os.getenv("MYSQL_PASSWORD", "sparkpass123")
    database = os.getenv("MYSQL_DATABASE", "ecommerce")
    # Porta 3307 = acesso externo (da sua máquina pro container)
    url = f"mysql+pymysql://{user}:{password}@localhost:3307/{database}"
    return create_engine(url)


def main() -> None:
    engine = get_engine()

    for csv_name, table_name in CSV_TO_TABLE.items():
        csv_path = DATA_DIR / csv_name
        print(f"\nCarregando {csv_name} -> tabela '{table_name}'...")

        # Lê o CSV com pandas
        df = pd.read_csv(csv_path)
        print(f"  {len(df):,} linhas lidas")

        # Escreve no MySQL (substitui a tabela se já existir)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=5000,
        )
        print(f"  Inserido na tabela '{table_name}'")

    print("\nCarga concluída!")
    engine.dispose()


if __name__ == "__main__":
    main()