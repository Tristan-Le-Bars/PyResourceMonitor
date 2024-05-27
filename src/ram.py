import psutil

class RAM:
    def __init__(self):
        self._ram_process_dict = {}

    def fill_process_list(self):
        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'memory_info', 'memory_percent', 'num_threads']):
            try:
                mem_info = proc.info['memory_info']
                self._ram_process_dict[proc.info['pid']] = {
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'create_time': proc.info['create_time'],
                    'rss': mem_info.rss,
                    'vms': mem_info.vms,
                    'shared': mem_info.shared if hasattr(mem_info, 'shared') else None,
                    'data': mem_info.data if hasattr(mem_info, 'data') else None,
                    'memory_percent': proc.info['memory_percent'],
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavailable.")


    @property
    def ram_process_list(self):
        return self._ram_process_dict

    def __repr__(self):
        return f"RAM(process_list={self._ram_process_dict})"