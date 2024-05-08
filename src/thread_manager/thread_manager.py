#Version 0.10 | Encoding UTF-8
#Created 26-04-2024
#Created by: Ib Leminen Mohr Nielsen
#Modified by: Frederik B. B. Jepsen, Ib Leminen Mohr Nielsen
#Last modified 1-05-2024

import threading
from TCPSERVER import SQL_socket

class ThreadManager:
    """
    The class ThreadManager is used to run the TCPSERVER on a thread.\n 

    List of class methods:\n
    - run_server(self, directory): Runs the server on a thread, uses directory to specify what folder it is running from.\n

    """

    def run_server(self, directory="/home/Gruppe250/test"):
        """
        Runs the server on a thread, uses directory to specify what folder it is running from.\n
        \n
        ------------
        PARAMETERS\n
        directory = The path of the file to check xml-integrety.\n
    
        self:\n
        ------------
        RETURNS\n
        \n
        Returns "None"\n
        Return None\n
        """

        server=SQL_socket(user="testuser",password="testpassword", host="127.0.0.1", directory=directory)
        print('* TCP Server listening for incoming connections in port {}'.format(server.PORT))
        thread = threading.Thread(target=server.run) #Creates a thread, with the server as the target
        thread.start() #Starts the server on a thread

if __name__ == "__main__":
    thread_manager = ThreadManager()
    thread_manager.run_server() #if you want to change directory, you can add it as a parameter here ex. macOS run_server("/Users/ibleminen/Downloads/test/rasp") 

