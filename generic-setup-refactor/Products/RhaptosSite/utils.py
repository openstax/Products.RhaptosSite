import os
import sys
import signal
import threading

def kill_other_threads_and_exit():
    """
    This function terminates all running threads without cleanup (commits seppuku).
    
    There are tools (like CMFSquidTool) that spawn threads without a way to terminate them.
    Usually, they expect to be long-running daemon processes and so don't have provisions 
    for terminating spawned children.
    
    Exiting the main thread or calling exit() will wait until the child threads finish
    and will not terminate the program.
    """
    if 1 == len(threading.enumerate()):
        sys.exit(0)
    else:
        os.kill(os.getpid(), signal.SIGTERM)
