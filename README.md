# Anti-Keylogger

## Overview

Anti-Keylogger is a Python project that monitors CPU and memory usage of processes and can detect suspicious activity based on CPU usage spikes, while using a keyboard. It also includes a keylogger component for capturing keystrokes .This project is for educational purposes only.

## Features

- Monitor CPU and memory usage of processes.
- Detect processes with increased CPU usage, when key is pressed.
- Log keystrokes to a file (keylogger functionality).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/antikeylogger.git
    cd antikeylogger
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the keylogger:

    ```bash
    python antikeylogger/keylogger.py
    ```

2. Run the process monitoring:

    ```bash
    python antikeylogger/MonitorPids.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
