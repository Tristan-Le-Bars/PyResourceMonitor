from processesCollector import ProcessesCollector
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
    processes_collector = ProcessesCollector()
    while True:
        # time.sleep(1)
        start_time = time.time()
        processes_collector.fill_processes_dicts()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'iteration time = {elapsed_time}')
        # processes_collector.print_cpu_process_dict()


if __name__ == "__main__":
    main()
