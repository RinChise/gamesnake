import json
import psycopg2
import os


class DBScore:
    def __init__(self, config_path=None):
        """
        Initialisiert die Datenbankverbindung mit Werten aus der JSON-Konfigurationsdatei.
        Falls die Datei nicht existiert oder fehlerhaft ist, werden Standardwerte verwendet.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

        self.config = self._load_config(config_path)

        # Konfigurationswerte setzen
        self.host = self.config.get("DB_HOST", "localhost")
        self.user = self.config.get("DB_USER", "testuser")
        self.password = self.config.get("DB_PASSWORD", "")
        self.database = self.config.get("DB_NAME", "neondb")
        self.port = self.config.get("DB_PORT", 5432)  # Standardport für PostgreSQL
        self.sslmode = self.config.get("DB_SSLMODE", "require")  # Standardmäßig SSL nutzen

    def _load_config(self, config_path):
        """
        Lädt die Konfigurationsdaten aus der JSON-Datei.
        Falls die Datei nicht existiert oder fehlerhaft ist, wird eine Standardkonfiguration geladen.
        """
        if not os.path.exists(config_path):
            print(f"⚠️ WARNUNG: {config_path} nicht gefunden! Standardwerte werden verwendet.")
            return {
                "DB_HOST": "localhost",
                "DB_USER": "testuser",
                "DB_PASSWORD": "",
                "DB_NAME": "neondb",
                "DB_PORT": 5432,
                "DB_SSLMODE": "require",
            }

        try:
            with open(config_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠️ Fehler: `config.json` ist ungültig! Standardwerte werden verwendet.")
            return {
                "DB_HOST": "localhost",
                "DB_USER": "testuser",
                "DB_PASSWORD": "",
                "DB_NAME": "neondb",
                "DB_PORT": 5432,
                "DB_SSLMODE": "require",
            }

    def _get_connection(self):
        """
        Erstellt und gibt eine Datenbankverbindung zurück.
        """
        try:
            return psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                sslmode=self.sslmode,
            )
        except psycopg2.Error as err:
            print(f"❌ Fehler beim Herstellen der Datenbankverbindung: {err}")
            return None

    def insert_score(self, player_name, score):
        """
        Fügt den übergebenen Score zusammen mit dem Spielernamen und dem aktuellen Zeitstempel in die Datenbank ein.
        """
        if score <= 0:
            return False

        query = """
             INSERT INTO gamescore (name, score, achieved_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
        """

        conn = self._get_connection()
        if conn is None:
            return False

        try:
            with conn, conn.cursor() as cursor:
                cursor.execute(query, (player_name, score))
                print("✅ Score erfolgreich eingefügt!")
                return True
        except psycopg2.Error as err:
            print(f"❌ Fehler beim Einfügen des Scores: {err}")
            return False

    def get_top_scores(self, limit=10):
        """
        Gibt die Top-Scores (Spielername, Score, Erreicht-Zeitpunkt) als Liste von Tupeln zurück,
        sortiert absteigend nach Score.
        """
        query = """
            SELECT name, score, TO_CHAR(achieved_at, 'YYYY-MM-DD HH24:MI') AS achieved_at
            FROM gamescore
            ORDER BY score DESC
            LIMIT %s
        """

        conn = self._get_connection()
        if conn is None:
            return []

        try:
            with conn, conn.cursor() as cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        except psycopg2.Error as err:
            print(f"❌ Fehler beim Abrufen der Highscores: {err}")
            return []
