import psutil

class Network:
    def __init__(self):
        self._network_process_dict = {}

    def fill_process_list(self):
        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'connections', 'io_counters']):
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
                                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}", # local adresse (IP and port)
                                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None, # local adresse (IP and port)
                                'bytes_sent': io_counters.bytes_sent if io_counters else None,
                                'bytes_recv': io_counters.bytes_recv if io_counters else None
                            }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavailable.")

    @property
    def network_process_list(self):
        return self._network_process_dict

    def __repr__(self):
        return f"Network(process_list={self._network_process_dict})"