# Fotoparadies Status Checker 📸⁉️ [![PyPI version](https://badge.fury.io/py/fotoparadies.svg)](https://badge.fury.io/py/fotoparadies)

📝 Der Fotoparadies Status Checker ermöglicht das Überprüfen des aktuellen Status von abgegebenen Fotoaufträgen (beispielsweise im DM).

![](https://github.com/hija/fotoparadies/raw/main/doc/img/01_status.png)

## Installation
Am einfachsten installierst du das Tool mit pip:

`pip install fotoparadies`

Danach öffnest du ein neues Terminal / CMD / Shell / ... Fenster und kannst den `fotoparadies`-Befehl verwenden.
Beispiele findest du im folgenden:

## Funktionsweise
1. **Neue Aufträge hinzufügen**
   
    Ein neuer Auftrag wird hinzugefügt, indem das Tool mit `fotoparadies add [Filial-Nummer] [Auftragsnummer] (Name)` aufgerufen wird.
    Der Parameter Name ist optional, er hilft aber die Aufträge voneinander zu unterscheiden.

    ![](https://github.com/hija/fotoparadies/raw/main/doc/img/00_add.png)

2. **Status der Aufträge anzeigen**

    Den Status der Aufträge, lässt sich mit `fotoparadies status` anzeigen:

    ![](https://github.com/hija/fotoparadies/raw/main/doc/img/01_status.png)

3. **Gelieferte Aufträge löschen**
   
   Gelieferte Aufträge (Status "Delivered") lassen sich automatisch mit dem `fotoparadies cleanup` Befehl löschen:

   ![](https://github.com/hija/fotoparadies/raw/main/doc/img/02_cleanup.png)

4. **Auftrag manuell löschen**

    Ein Auftrag lässt sich mit dem `fotoparadies remove [Name]` Befehl manuell löschen. Name ist entweder der in Schritt 1 gesetzter Name oder alternativ die Auftragsnummer.

    ![](https://github.com/hija/fotoparadies/raw/main/doc/img/03_remove.png)

## FAQ

**Q: Wieso ist der Status ERROR?**

A: Der Status ist ERROR, wenn der Auftrag noch nicht im Großlabor angekommen und eingescannt wurde.