import json
import os
import logging
from typing import Optional, List, Tuple
import psycopg2
from psycopg2 import pool

# Logger für Fehler und Warnungen
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBScore:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialisiert die Datenbankverbindung mit Werten aus der JSON-Konfigurationsdatei.
        Die Konfigurationsdatei muss alle erforderlichen Werte enthalten.

        :param config_path: Pfad zur Konfigurationsdatei (optional)
        :raises FileNotFoundError: Wenn die Konfigurationsdatei nicht gefunden wird.
        :raises json.JSONDecodeError: Wenn die Konfigurationsdatei ungültig ist.
        :raises KeyError: Wenn ein erforderlicher Konfigurationswert fehlt.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

        self.config = self._load_config(config_path)
        self._validate_config()

        # Konfigurationswerte setzen
        self.host = self.config["DB_HOST"]
        self.user = self.config["DB_USER"]
        self.password = self.config["DB_PASSWORD"]
        self.database = self.config["DB_NAME"]
        self.port = self.config["DB_PORT"]
        self.sslmode = self.config["DB_SSLMODE"]

        # Connection Pool für bessere Leistung
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            sslmode=self.sslmode,
        )

    def _load_config(self, config_path: str) -> dict:
        """
        Lädt die Konfigurationsdaten aus der JSON-Datei.

        :param config_path: Pfad zur Konfigurationsdatei
        :return: Konfigurationsdaten als Dictionary
        :raises FileNotFoundError: Wenn die Datei nicht gefunden wird.
        :raises json.JSONDecodeError: Wenn die Datei ungültig ist.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Konfigurationsdatei {config_path} nicht gefunden!")

        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _validate_config(self) -> None:
        """
        Validiert die Konfigurationsdaten.

        :raises KeyError: Wenn ein erforderlicher Konfigurationswert fehlt.
        """
        required_keys = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "DB_PORT", "DB_SSLMODE"]
        for key in required_keys:
            if key not in self.config:
                raise KeyError(f"Fehlender Konfigurationswert: {key}")

    def _get_connection(self):
        """
        Gibt eine Datenbankverbindung aus dem Connection Pool zurück.

        :return: Datenbankverbindung oder None bei Fehlern
        """
        try:
            return self.connection_pool.getconn()
        except psycopg2.Error as err:
            logger.error(f"❌ Fehler beim Herstellen der Datenbankverbindung: {err}")
            return None

    def insert_score(self, player_name: str, score: int) -> bool:
        """
        Fügt den übergebenen Score zusammen mit dem Spielernamen und dem aktuellen Zeitstempel in die Datenbank ein.

        :param player_name: Name des Spielers
        :param score: Score des Spielers
        :return: True bei Erfolg, False bei Fehlern
        """
        if score <= 0:
            logger.warning("⚠️ Score muss größer als 0 sein!")
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
                logger.info("✅ Score erfolgreich eingefügt!")
                return True
        except psycopg2.Error as err:
            logger.error(f"❌ Fehler beim Einfügen des Scores: {err}")
            return False
        finally:
            self.connection_pool.putconn(conn)

    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, str]]:
        """
        Gibt die Top-Scores (Spielername, Score, Erreicht-Zeitpunkt) als Liste von Tupeln zurück,
        sortiert absteigend nach Score.

        :param limit: Maximale Anzahl der zurückgegebenen Scores
        :return: Liste der Top-Scores
        """
        query = """
            SELECT name, score, TO_CHAR(achieved_at AT TIME ZONE 'UTC' 
            AT TIME ZONE 'Europe/Berlin', 'YYYY-MM-DD HH24:MI') AS achieved_at
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
            logger.error(f"❌ Fehler beim Abrufen der Highscores: {err}")
            return []
        finally:
            self.connection_pool.putconn(conn)
