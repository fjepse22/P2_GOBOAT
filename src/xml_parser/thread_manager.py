import threading
import subprocess
import sys 

class ThreadManager:
    def run_script(self, script_name):
        subprocess.run(["python", script_name])

    def run_thread(self, script_name):
        thread = threading.Thread(target=self.run_script, args=(script_name,))
        thread.start()

if __name__ == "__main__":
    print("Thread manager is running.")
    thread_manager = ThreadManager()
    thread_manager.run_thread(str("/home/Gruppe250/test/TCPSERVER.py",))
