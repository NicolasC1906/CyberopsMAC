import subprocess
import re
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    header = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                     MAC Address Changer                        ║
    ║              - Creado Por: Nicolas Ceron Alfonso               ║
    ║              - Curso: CyberOps Associate                       ║
    ║              - Release: 08/07/2024  - v1.0                     ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(header)
    print("Cualquier acción relacionada con este programa es únicamente su responsabilidad")
    print("=" * 70)

def list_network_interfaces():
    interfaces = {}
    try:
        output = subprocess.check_output("ifconfig", stderr=subprocess.STDOUT)
        for line in output.decode('utf-8').split('\n'):
            if 'flags' in line:
                interface = line.split(':')[0]
            if 'ether' in line:
                mac = line.split()[1]
                interfaces[interface] = mac
        return interfaces
    except subprocess.CalledProcessError as e:
        print("Error al obtener las interfaces de red")
        print(e.output.decode())
        return None

def change_mac(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    current_mac = list_network_interfaces().get(interface, None)
    if current_mac == new_mac:
        print(f"La dirección MAC ha sido cambiada a: {current_mac}")
    else:
        print("No se pudo cambiar la dirección MAC.")

def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def print_menu(interfaces):
    print("\n[0] Cambiar la dirección MAC manualmente")
    print("[1] Cambiar la dirección MAC automáticamente")
    print("[99] Salir")
    print("\nInterfaces disponibles:")
    for idx, (interface, mac) in enumerate(interfaces.items(), 2):
        print(f"[{idx}] {interface} - {mac}")

def main_menu():
    try:
        while True:
            clear_screen()
            print_header()
            
            interfaces = list_network_interfaces()
            if not interfaces:
                print("No se encontraron interfaces con dirección MAC.")
                input("Presione Enter para salir...")
                return
            
            print_menu(interfaces)
            
            choice = input("\n[*] Elige una opción: ")
            
            if choice == '99':
                confirm = input("¿Está seguro de que desea salir? (sí/no): ")
                if confirm.lower() == 'si' or confirm.lower() == 's':
                    print("Gracias por usar el programa. ¡Hasta luego!")
                    break
            elif choice in ['0', '1']:
                interface_choice = input("Ingrese el número de la interfaz de red que desea modificar: ")
                try:
                    interface = list(interfaces.keys())[int(interface_choice) - 2]
                except (ValueError, IndexError):
                    print("Selección no válida. Intente de nuevo.")
                    input("Presione Enter para continuar...")
                    continue
                
                if choice == '0':
                    new_mac = input("Ingrese la nueva dirección MAC (formato XX:XX:XX:XX:XX:XX): ")
                    change_mac(interface, new_mac)
                else:
                    random_mac = generate_random_mac()
                    print(f"Generando y aplicando dirección MAC aleatoria: {random_mac}")
                    change_mac(interface, random_mac)
            else:
                print("Opción no válida. Intente de nuevo.")
            
            input("Presione Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido. Saliendo de manera segura...")

if __name__ == "__main__":
    main_menu()
