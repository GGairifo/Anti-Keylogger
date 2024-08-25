import psutil

class Pid:
    """
    A class to represent and monitor a process by its PID (Process ID).
    
    Attributes:
        pid (int): The process ID to monitor.
        process (psutil.Process): The psutil.Process object for the given PID.

    Methods:
        __init__(pid):
            Initializes the Pid object and checks if the process with the given PID exists.
        get_cpu_usage():
            Returns the CPU usage percentage of the process.
        get_memory_usage():
            Returns the memory usage of the process in megabytes (MB).
    """

    def __init__(self, pid):
        """
        Initializes the Pid object by verifying the existence of the process with the given PID.
        
        Args:
            pid (int): The process ID to monitor.

        Raises:
            ValueError: If the process with the given PID does not exist or is not accessible.
        """
        self.pid = pid
        if not psutil.pid_exists(pid):
            raise ValueError(f"Process with PID {pid} does not exist.")
        try:
            self.process = psutil.Process(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            raise ValueError(f"Process with PID {pid} is not accessible: {e}")

    def get_cpu_usage(self):
        """
        Returns the CPU usage percentage of the monitored process.
        
        The CPU usage percentage is calculated over a 1-second interval.

        Returns:
            float: The CPU usage percentage of the process.

        Raises:
            ValueError: If the process with the PID is no longer available or not accessible.
        """
        try:
            return self.process.cpu_percent(interval=1)  # Get CPU usage percentage over 1 second
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            raise ValueError(f"Process with PID {self.pid} is no longer available: {e}")

    def get_memory_usage(self):
        """
        Returns the memory usage of the monitored process in megabytes (MB).

        Returns:
            float: The memory usage of the process in MB.

        Raises:
            ValueError: If the process with the PID is no longer available or not accessible.
        """
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / (1024 ** 2)  # RSS in MB
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            raise ValueError(f"Process with PID {self.pid} is no longer available: {e}")
