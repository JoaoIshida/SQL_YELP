import sqlite3

def execute_sql_script(db_name="yelp.db"):    
    sql_files = ["sql/trigger1.sql", "sql/trigger2.sql"]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    for sql_file in sql_files:
        with open(sql_file, "r") as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        print(f"Executed {sql_file} successfully.")

    conn.commit()
    conn.close()
    print("Triggers setup complete!")

if __name__ == "__main__":
    execute_sql_script()