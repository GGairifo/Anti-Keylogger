import threading
import time
import psutil
from Pid import Pid  # Import the Pid class

cpu_usage_data_first_interval = {}
cpu_usage_data_second_interval = {}

def monitor_pid(pid, data_storage, interval_duration):
    """
    Monitors the CPU usage of a process with the given PID for a specified duration.
    
    This function collects CPU usage data at 1-second intervals and stores the data in 
    the `data_storage` dictionary under the provided PID.

    Args:
        pid (int): The process ID to monitor.
        data_storage (dict): A dictionary to store the CPU usage data, with PIDs as keys.
        interval_duration (int): The duration in seconds to monitor the process.

    Returns:
        None

    Raises:
        ValueError: If there is an issue with accessing the process or if it is no longer available.
    """
    try:
        monitor = Pid(pid)
    except ValueError as e:
        print(f"Error initializing monitoring for PID {pid}: {e}")
        return
    data_storage[pid] = []
    start_time = time.time()
 
    try:
        while True:
            cpu_usage = monitor.get_cpu_usage()
            timestamp = time.time() - start_time
            data_storage[pid].append((timestamp, cpu_usage))
            time.sleep(1)  
            
            if time.time() - start_time >= interval_duration:
                break
    except ValueError as e:
        print(f"Error monitoring PID {pid}: {e}")

def run_monitoring(pids, interval_duration, data_storage):
    """
    Runs CPU usage monitoring for multiple processes concurrently using threads.
    
    Each process is monitored for the specified interval duration, and data is stored 
    in the provided `data_storage` dictionary.

    Args:
        pids (list of int): A list of PIDs to monitor.
        interval_duration (int): The duration in seconds to monitor each process.
        data_storage (dict): A dictionary to store the CPU usage data, with PIDs as keys.

    Returns:
        None
    """
    threads = []
    for pid in pids:
        thread = threading.Thread(target=monitor_pid, args=(pid, data_storage, interval_duration))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # Wait for all threads to complete

def calculate_average_cpu_usage(cpu_usage_data):
    """
    Calculates the average CPU usage for each process based on collected data.
    
    The average is computed by summing up the CPU usage percentages and dividing by
    the number of recorded data points.

    Args:
        cpu_usage_data (dict): A dictionary with PIDs as keys and lists of (timestamp, cpu_usage) tuples as values.

    Returns:
        dict: A dictionary with PIDs as keys and average CPU usage percentages as values.
    """
    avg_cpu_usage = {}
    for pid, data in cpu_usage_data.items():
        if data:
            total_usage = sum(usage for _, usage in data)
            avg_cpu_usage[pid] = total_usage / len(data)
    return avg_cpu_usage

if __name__ == "__main__":
    """
    Main script execution:
    - Retrieves all current PIDs.
    - Monitors CPU usage of all processes for two 15-second intervals.
    - Calculates and displays average CPU usage for each interval.
    - Identifies and reports processes with increased CPU usage in the second interval.
    """
    pids = psutil.pids()  # Get all PIDs
    print(f"Total number of PIDs: {len(pids)}")

    try:
        print("Measuring CPU usage for the first 15 seconds...")
        run_monitoring(pids, interval_duration=15, data_storage=cpu_usage_data_first_interval)

        print("Starting the second measurement period, please press a key...")
        time.sleep(2)
        run_monitoring(pids, interval_duration=15, data_storage=cpu_usage_data_second_interval)
        
    finally:
        print("Monitoring complete. Collected CPU usage data:")

        avg_usage_first_interval = calculate_average_cpu_usage(cpu_usage_data_first_interval)
        avg_usage_second_interval = calculate_average_cpu_usage(cpu_usage_data_second_interval)

        print("\nFirst 15 seconds average CPU usage:")
        for pid, avg_usage in avg_usage_first_interval.items():
            print(f"PID: {pid} - Average CPU Usage: {avg_usage:.2f}%")

        print("\nSecond 15 seconds average CPU usage:")
        for pid, avg_usage in avg_usage_second_interval.items():
            print(f"PID: {pid} - Average CPU Usage: {avg_usage:.2f}%")

        print("\nPIDs with increased CPU usage during the second interval, possible keyloggers:")
        for pid in avg_usage_second_interval:
            first_interval_usage = avg_usage_first_interval.get(pid, 0)
            second_interval_usage = avg_usage_second_interval[pid]
            if second_interval_usage > first_interval_usage:
                increase_percentage = ((second_interval_usage - first_interval_usage) / first_interval_usage) * 100 if first_interval_usage > 0 else float('inf')
                print(f"PID: {pid}, Name: {psutil.Process(pid).name()} - Increased CPU Usage: {second_interval_usage:.2f}% (Increase: {increase_percentage:.2f}%)")
