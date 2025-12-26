"""
PySystemMonitor
A comprehensive system monitoring tool
"""

import argparse
import sys
import threading
from core.monitor import SystemMonitor
from interfaces.gui import GUIInterface
from interfaces.cli import CLIInterface
from config.settings import Config

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description=f"{Config.APP_NAME} v{Config.VERSION}")
    parser.add_argument('--gui', action='store_true', help='Start with GUI (default)')
    parser.add_argument('--cli', action='store_true', help='Start with CLI')
    parser.add_argument('--no-ui', action='store_true', help='Start without UI (background mode)')
    
    args = parser.parse_args()
    
    # Initialize monitor
    try:
        monitor = SystemMonitor()
    except Exception as e:
        print(f"Error initializing system monitor: {e}")
        sys.exit(1)
        
    # Determine mode
    if args.cli:
        print("Starting CLI mode...")
        cli = CLIInterface(monitor)
        try:
            cli.run_interactive()
        except KeyboardInterrupt:
            print("\nStopping...")
    elif args.no_ui:
        print("Starting background mode...")
        # Just run the monitor loop
        import time
        try:
            while True:
                monitor.update_all()
                time.sleep(Config.PROCESS_UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping...")
    else:
        # Default to GUI
        print("Starting GUI mode...")
        gui = GUIInterface(monitor)
        try:
            gui.run()
        except KeyboardInterrupt:
            print("\nStopping...")
        except Exception as e:
            print(f"GUI Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
