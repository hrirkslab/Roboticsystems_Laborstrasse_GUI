import sqlite3

class DatabaseConnection:
    db_name = 'laborstreet_management'
    conn = None
    cursor = None

    @staticmethod
    def connect():
        """Stellt eine Verbindung zur Datenbank her."""
        DatabaseConnection.conn = sqlite3.connect(DatabaseConnection.db_name)
        DatabaseConnection.cursor = DatabaseConnection.conn.cursor()
        return DatabaseConnection.conn

    @staticmethod
    def close():
        """Schließt die Verbindung zur Datenbank."""
        if DatabaseConnection.conn:
            DatabaseConnection.conn.close()

    @staticmethod
    def create_table():
        """Erstellt die Tabelle, falls sie nicht existiert."""
        DatabaseConnection.connect()  # Verbindung herstellen
        DatabaseConnection.cursor.execute('''
        CREATE TABLE IF NOT EXISTS TubeQrcode (
            qr_code INTEGER PRIMARY KEY,
            datum DATE
        )
        ''')
        DatabaseConnection.conn.commit()
        DatabaseConnection.close()  # Verbindung schließen


