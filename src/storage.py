import psutil

class Storage:
    def __init__(self):
        self.processes = self.get_storage_processes()
        self._disk_io_info = {}
        self._storage_processes = {}

    def get_disk_io(self):
        '''
        Put all the detected storage devices in a list.
        '''
        io_counters = psutil.disk_io_counters(perdisk=True)
        for disk, counters in io_counters.items():
            try:
                self._disk_io_info[disk] = counters
            except Exception:
                print(f"The disk {disk} is unavalable.")

    def get_storage_processes(self):
        '''
        Get all the processes running on storage devices.
        '''
        # iterate through all processes
        for proc in psutil.process_iter(['pid', 'name', 'open_files', 'io_counters']):
            try:
                # check if the process have opened files
                if proc.info['open_files']:
                    # get all the opened files of the process
                    open_files_paths = [file.path for file in proc.info['open_files']]
                    self._storage_processes[proc.info['pid']] = {
                        'name': proc.info['name'],
                        'user': proc.info['username'],
                        'create_time': proc.info['create_time'],
                        'files': open_files_paths,
                        'read_count': proc.info['io_counters'].read_count if proc.info['io_counters'] else None,
                        'write_count': proc.info['io_counters'].write_count if proc.info['io_counters'] else None,
                        'read_bytes': proc.info['io_counters'].read_bytes if proc.info['io_counters'] else None,
                        'write_bytes': proc.info['io_counters'].write_bytes if proc.info['io_counters'] else None
                    }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"The process with PID {proc.info['pid']} is unavalable.")

    @property
    def disk_io_info(self):
        return self._disk_io_info
    
    @property
    def storage_processes(self):
        return self._storage_processes

    def __repr__(self):
        return (f"disk_io={self.disk_io},\n"
                f"processes={self.processes})")