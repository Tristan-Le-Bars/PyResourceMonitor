import psutil

class Process:
    def  __init__(self):
        pass
        # _private_variable
        # get _process_name
        # get _Pid

    @property
    def process_name(self):
        return self._process_name
    
    @property
    def pid(self):
        return self._pid
    
class CPU(Process):
    def __init__(self):
        pass
        # get _description
        # get _threads_number
    
    @property
    def description(self):
        return self._descrition
    
    @property
    def threads_number(self):
        return self._threads_number
    
    def get_process(self):
        pid_list = psutil.Process().cpu_affinity(percpu=True)[cpu_number]

        for pid in pid_list:
            try:
                process = psutil.Process(pid)
                print(f"Processus PID: {pid}, Nom: {process.name()}, Utilisateur: {process.username()}")
            except psutil.NoSuchProcess:
                print(f"Le processus avec PID {pid} n'existe pas ou n'est pas accessible.")




    
class Storage(Process):
    def __init__(self):
        pass
        # get _filepath
        # get _reading
        # get _writing
        # get _priority
    
    @property
    def filepath(self):
        return self._filepath
    
    @property
    def reading(self):
        return self._reading
    
    @property
    def writing(self):
        return self._writing
    
    @property
    def priority(self):
        return self._priority
    
class Network(Process):
    def __init__(self):
        pass
        # get _address
        # get _upload
        # get _download
    
    @property
    def address(self):
        return self._address
    
    @property
    def upload(self):
        return self._upload
    
    @property
    def download(self):
        return self._download
    

class RAM(Process):
    def __init__(self):
        pass
        # get _validation
        # get _work_range
        # get _shared
        # get _private
    
    @property
    def validation(self):
        return self._validation
    
    @property
    def work_range(self):
        return self._work_range
    
    @property
    def shared(self):
        return self._shared
    
    @property
    def private(self):
        return self._private