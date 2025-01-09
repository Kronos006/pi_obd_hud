###################################################################################################
## Description: 
##
##
###################################################################################################
##  Version      Author           Date              Description
##  1.0          Rufus Brandes    09.01.2025        Initial revision
##
##
###################################################################################################

#!/bin/bash

# MAC-Adresse des Ziel-Bluetooth-Geräts
TARGET_MAC="XX:XX:XX:XX:XX:XX"

# Endlosschleife für die Verbindung
while true; do
    echo "Versuche, eine Verbindung zu $TARGET_MAC herzustellen..."
    
    # Bluetooth-Gerät koppeln (falls nicht bereits gekoppelt)
    echo "Pairing mit $TARGET_MAC..."
    bluetoothctl pair "$TARGET_MAC" || echo "Pairing fehlgeschlagen."

    # Bluetooth-Gerät verbinden
    echo "Verbinden mit $TARGET_MAC..."
    bluetoothctl connect "$TARGET_MAC"
    
    # Warte, bis die Verbindung unterbrochen wird
    sleep 5
    CONNECTED=$(bluetoothctl info "$TARGET_MAC" | grep -i "connected: yes")
    
    if [[ -z "$CONNECTED" ]]; then
        echo "Verbindung verloren. Erneuter Versuch in 5 Sekunden..."
    else
        echo "Verbindung erfolgreich. Warte auf Verbindungsabbruch..."
    fi
    
    # Warte, bis die Verbindung unterbrochen ist
    while [[ -n "$CONNECTED" ]]; do
        sleep 5
        CONNECTED=$(bluetoothctl info "$TARGET_MAC" | grep -i "connected: yes")
    done
done
