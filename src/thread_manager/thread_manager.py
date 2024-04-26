import threading
import subprocess

class ThreadManager:
    def run_script(self, script_name):
        subprocess.run(["python", script_name])

    def run_thread(self, script_name):
        thread = threading.Thread(target=self.run_script, args=(script_name))
        thread.start()

if __name__ == "__main__":
    thread_manager = ThreadManager()
    thread_manager.run_thread("TCPSERVER.py")
