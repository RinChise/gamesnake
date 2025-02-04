# db_score.py
import mysql.connector

class DBScore:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user        # Wird nur für die Verbindung genutzt
        self.password = password
        self.database = database

    def insert_score(self, player_name, score):
        """
        Fügt den übergebenen Score zusammen mit dem Spielernamen in die Datenbank ein.
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            sql = "INSERT INTO gamescores (player_name, score) VALUES (%s, %s)"
            values = (player_name, score)
            cursor.execute(sql, values)
            connection.commit()
            print("Score erfolgreich eingefügt!")
        except mysql.connector.Error as err:
            print("Fehler beim Einfügen des Scores:", err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_top_scores(self, limit=10):
        """
        Gibt die Top-Scores (Spielername und Score) als Liste von Tupeln zurück,
        sortiert absteigend nach Score.
        """
        results = []
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            sql = "SELECT player_name, score, achieved_at FROM gamescores ORDER BY score DESC LIMIT %s"
            cursor.execute(sql, (limit,))
            results = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Fehler beim Abrufen der Highscores:", err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return results
