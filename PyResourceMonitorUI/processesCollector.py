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

        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'cpu_times', 
                                         'status', 'cpu_percent', 'num_threads', 'open_files',
                                         'memory_info', 'memory_percent', 'connections', 'io_counters']):
            try:
                if proc.info['pid'] == 0:
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

                mem_info = proc.info['memory_info']
                self._ram_process_dict[proc.info['pid']] = {
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'create_time': proc.info['create_time'],
                    'rss': mem_info.rss,
                    'vms': mem_info.vms,
                    'shared': getattr(mem_info, 'shared', None),
                    'data': getattr(mem_info, 'data', None),
                    'memory_percent': proc.info['memory_percent'],
                }

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

                connections = proc.info['connections']
                if connections:
                    for conn in connections:
                        if conn.status == psutil.CONN_ESTABLISHED:
                            self._network_process_dict[proc.info['pid']] = {
                                'name': proc.info['name'],
                                'user': proc.info['username'],
                                'create_time': proc.info['create_time'],
                                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}",
                                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                                'status': conn.status
                            }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

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
