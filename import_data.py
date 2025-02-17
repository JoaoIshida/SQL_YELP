import sqlite3
import pandas as pd
import os

DB_NAME = "yelp.db"
DATA_DIR = "data" #folder of my csv files

def import_csv_to_db(table_name, csv_file):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_csv(os.path.join(DATA_DIR, csv_file))

    df.to_sql(table_name, conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_csv_to_db("business", "business_table.csv")
    import_csv_to_db("checkin", "checkin_table.csv")
    import_csv_to_db("user_yelp", "user_yelp_table.csv")
    import_csv_to_db("tip", "tip_table.csv")
    import_csv_to_db("review", "review_table.csv")
    import_csv_to_db("friendship", "friendship_table.csv")

    print("All CSV files imported successfully.")
