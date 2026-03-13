import oracledb

conn = None

try:
    conn = oracledb.connect(
        user="system",
        password="1404",
        dsn="localhost:1521/XEPDB1"
    )
    print("Connected successfully (Thin mode)")
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        conn.close()
        print("Connection closed")