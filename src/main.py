from processesCollector import ProceccesCollector
import ctypes
import time

# obtenir tout les processes avec un seul objet
# ram ok
# network ok
# cpu ok
# storage ok
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    processes_collector = ProceccesCollector()
    while True:
        # time.sleep(1)
        processes_collector.fill_processes_dicts()
        # processes_collector.print_cpu_process_dict()
        print("test")


if __name__ == "__main__":
    main()