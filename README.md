
# Snake Game

Ein klassisches Snake-Spiel in Python mit **Singleplayer**, **Multiplayer** und **Highscore-Funktion**.  

## Installation

1. **Repository klonen:**
   ```sh
   git clone https://github.com/RinChise/gamesnake.git
   ```
2. **Benötigte Abhängigkeiten installieren (falls erforderlich):**
   ```sh
   pip install -r requirements.txt
   ```
3. **Spiel starten:**
   ```sh
   python3 main.py
   ```

## Spielmodi

### **Hauptmenü**
Wähle zwischen **Singleplayer**, **Multiplayer** oder **Highscore**.

### **Singleplayer**
- Du steuerst eine Schlange und musst wachsen, ohne den **Rand oder deinen eigenen Schwanz** zu berühren.  
- Sobald du dich selbst oder den Rand berührst, **verlierst du**.  

### **Multiplayer (Lokal)**
- Zwei Spieler teilen sich **eine Tastatur** und steuern ihre Schlangen.
- Der Rand ist **"wrapped"**, das heißt, du spawnst auf der gegenüberliegenden Seite, wenn du rausgehst.
- Eine **stärkere Schlange kann eine schwächere fressen**.
- Du verlierst, wenn du:
  - in deinen eigenen Schwanz läufst,
  - in eine **stärkere** Schlange kollidierst.

### **Highscore**
- Die **Top 10 Spieler-Scores** werden aus der **Datenbank** abgerufen und angezeigt.
- Punkte werden basierend auf der Spiellänge und gefressenem Essen berechnet.

## Steuerung

| Spieler | Steuerung   |
|---------|-------------|
| **Spieler 1** | Pfeiltasten |
| **Spieler 2** | W, S, A, D  |

## Highscore-System

- Highscores werden in einer **Datenbank gespeichert**.
- Nur die **Top 10 Spieler** werden im Highscore-Bildschirm angezeigt.
- Punkte werden basierend auf dem gefressenem Essen berechnet.
