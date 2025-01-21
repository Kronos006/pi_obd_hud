###################################################################################################
## Description:  Starts obd_hud_gui connects to OBD device via serial, fetches and displays data.
##              
##              
###################################################################################################
##  Version      Author           Date              Description
##  1.0          Rufus Brandes    09.01.2025        Initial revision
##
##
###################################################################################################

import serial.tools.list_ports  # Zum Scannen der verfügbaren Ports
import obd
import tkinter as tk


# Funktion zum Aufbau der Verbindung
def connect_to_obd():
    ports = [port.device for port in serial.tools.list_ports.comports()]  # Verfügbare Ports scannen
    print("Gefundene Ports:", ports)
    if ports:
        try:
            # Verbindung mit Port und Baudrate
            return obd.OBD(portstr=ports[0], baudrate=38400)  
        except Exception as e:
            print(f"Fehler beim Verbinden mit dem Adapter: {e}")
            return None
    else:
        print("Kein OBD-II Adapter gefunden!")
        return None


# Erzeuge die Verbindung zum OBD-II-Adapter
connection = connect_to_obd()


class OBDHud:
    def __init__(self, root):
        self.root = root
        self.root.title("OBD HUD")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")

        # Setze das Layout der GUI mit tk-Widgets
        frame = tk.Frame(self.root, bg="black")
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.rpm_label = tk.Label(frame, text="RPM: 0", font=("Arial", 56), bg="black", fg="white")
        self.rpm_label.pack(side=tk.LEFT, padx=20, pady=20)

        self.speed_label = tk.Label(frame, text="Speed: 0 km/h", font=("Arial", 56), bg="black", fg="white")
        self.speed_label.pack(side=tk.RIGHT, padx=20, pady=20)


        # Start des OBD-Update-Timers
        self.update_values()

    def update_values(self):
        """Diese Methode holt die OBD-Daten und aktualisiert die GUI."""
        if not connection or connection.status() != obd.OBDStatus.CAR_CONNECTED:
            self.root.after(1000, self.update_values)
            self.speed_label.config(text="Speed: N/A")
            self.rpm_label.config(text="RPM: N/A")
        else:
            # Geschwindigkeit abrufen
            speed_command = connection.query(obd.commands['SPEED'])
            if speed_command and speed_command.value is not None:
                self.speed_label.config(text=f"{speed_command.value.to('km/h')}")
            else:
                self.speed_label.config(text="N/A")

            # RPM abrufen
            rpm_command = connection.query(obd.commands.RPM)
            if rpm_command and rpm_command.value is not None:
                self.rpm_label.config(text=f"{rpm_command.value.to('rpm')}")
            else:
                self.rpm_label.config(text="N/A")

        self.root.after(1000, self.update_values)  # Timer fortsetzen


if __name__ == "__main__":
    root = tk.Tk()
    app = OBDHud(root)
    root.mainloop()
