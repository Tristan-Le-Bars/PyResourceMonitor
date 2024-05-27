import psutil

class CPU:
    def  __init__(self):
        self._num_cpus = psutil.cpu_count(logical=True)
        self._cpus_process_dict = {}

    def fill_process_list(self):
        for cpu in range(self._num_cpus):
            pid_list = psutil.Process().cpu_affinity(percpu=True)[cpu]

            # set all the cpus process in a dict
            for pid in pid_list:
                try:
                    process = psutil.Process(pid)
                    self._cpus_process_dict[pid] = {
                        'name': process.name(),
                        'user': process.username(),
                        'create_time': process.create_time(),
                        'uptime': process.cpu_times(),
                        'status': process.status(),
                        'cpu_usage': process.cpu_percent(),
                        'threads': process.threads()
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print(f"The process with PID {pid} is unavalable.")
    
    # those values must not be overwritten, so we use the property decorator
    @property
    def num_cpus(self):
        return self._num_cpus
    
    @property
    def cpu_process_list(self):
        return self._cpus_process_dict

    def __repr__(self):
        return(f"num_cpus={self._num_cpus}")