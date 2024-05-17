  
import sqlite3

from DBService.Control.DatabaseConnection import DatabaseConnection

#from Model.tubeQrcode  import TubeQrcode
class DatabaseAdapter:
    

    @staticmethod
    def insert_data(tubeQrcode):
        DatabaseConnection.connect()
        DatabaseConnection.create_table()
        DatabaseConnection.cursor.execute("INSERT INTO TubeQrcode (qr_code, datum) VALUES (?, ?)", (tubeQrcode.qr_code, tubeQrcode.datum))
        DatabaseConnection.conn.commit()
        DatabaseConnection.close()


    @staticmethod
    def select_all_from_tubeqrcode():
        DatabaseConnection.connect()
        DatabaseConnection.cursor.execute("SELECT * FROM TubeQrcode")
        rows = DatabaseConnection.cursor.fetchall()
        for row in rows:
            print(row)
        DatabaseConnection.close()
DatabaseConnection.create_table()        
DatabaseAdapter.select_all_from_tubeqrcode()