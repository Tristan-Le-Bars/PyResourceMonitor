import psutil

class ProcessesCollector:
    def __init__(self):
        self._cpu_process_dict = {}
        self._ram_process_dict = {}
        self._storage_process_dict = {}
        self._disk_io_info = {}
        self._network_process_dict = {}

    def fill_processes_dicts(self):
        self._cpu_process_dict.clear()
        self._ram_process_dict.clear()
        self._storage_process_dict.clear()
        self._network_process_dict.clear()
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time','cpu_times',
                                         'status', 'cpu_percent', 'num_threads', 'open_files',
                                         'memory_info', 'memory_percent', 'connections', 'io_counters']):
            # CPU
            try:
                if proc.info['pid'] == 0:  # Ignorer le System Idle Process
                    continue
                self._cpu_process_dict[proc.info['pid']] = {
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'create_time': proc.info['create_time'],
                    'cpu_times': proc.info['cpu_times'],
                    'status': proc.info['status'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'num_threads': proc.info['num_threads']
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavailable.")

            # RAM
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

            # Storage
            try:
                if proc.info['open_files']:
                    open_files_paths = [file.path for file in proc.info['open_files']]
                    io_counters = proc.info['io_counters']
                    self._storage_process_dict[proc.info['pid']] = {
                        'name': proc.info['name'],
                        'user': proc.info['username'],
                        'create_time': proc.info['create_time'],
                        'files': open_files_paths,
                        'read_count': io_counters.read_count if io_counters else None,
                        'write_count': io_counters.write_count if io_counters else None,
                        'read_bytes': io_counters.read_bytes if io_counters else None,
                        'write_bytes': io_counters.write_bytes if io_counters else None
                    }       
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavailable.")

            # Network
            try:
                connections = proc.info['connections']
                io_counters = proc.info['io_counters']
                if connections:
                    for conn in connections:
                        # check if the connection is established
                        if conn.status == psutil.CONN_ESTABLISHED:
                            self._network_process_dict[proc.info['pid']] = {
                                'name': proc.info['name'],
                                'user': proc.info['username'],
                                'create_time': proc.info['create_time'],
                                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}",
                                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                                'status': conn.status,
                                'bytes_sent': getattr(io_counters, 'bytes_sent', None) if io_counters else None, # getattr check if io_counter have the attribute 'byte_sent'
                                'bytes_recv': getattr(io_counters, 'bytes_recv', None) if io_counters else None
                            }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavailable.")
        
    def print_cpu_process_dict(self):
        for key, value in self._cpu_process_dict.items():
            print(f"PID {key}: {value}")

    def print_ram_process_dict(self):
        for key, value in  self._ram_process_dict.items():
            print(f"PID {key}: {value}")

    def print_storage_process_dict(self):
        for key, value in self._storage_process_dict.items():
            print(f"PID {key}: {value}")

    def get_disk_io(self):
        io_counters = psutil.disk_io_counters(perdisk=True)
        for disk, counters in io_counters.items():
            try:
                self._disk_io_info[disk] = counters
            except Exception:
                print(f"The disk {disk} is unavailable.")

    def print_network_process_dict(self):
        for key, value in  self._network_process_dict.items():
            print(f"PID {key}: {value}")

    @property
    def cpu_process_dict(self):
        return self._cpu_process_dict
    
    @property
    def ram_process_dict(self):
        return self._ram_process_dict

    @property
    def storage_process_dict(self):
        return self._storage_process_dict

    @property
    def disk_io_info(self):
        return self._disk_io_info
    
    @property
    def network_process_dict(self):
        return self._network_process_dict

    def __repr__(self):
        return (f"Storage(disk_io_info={self._disk_io_info}, "
                f"storage_process_dict={self._storage_process_dict})")