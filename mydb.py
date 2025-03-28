import mysql.connector

try:
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root'
    )
    
    cursorObject = dataBase.cursor()
    cursorObject.execute("CREATE DATABASE IF NOT EXISTS alnaser")
    print("Database created successfully")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'dataBase' in locals() and dataBase.is_connected():
        cursorObject.close()
        dataBase.close()