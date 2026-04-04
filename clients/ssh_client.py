import atexit
from abc import ABC, abstractmethod
import os
import subprocess

class SSHInterface(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def port_forward(self, local_port, remote_port):
        pass
    
class MUXSSHClient(SSHInterface):
    def __init__(self, user, target, jump, no_close=False):
        super().__init__()
        self.user = user
        self.target = target
        self.jump = jump
        self.mux_path = f"/tmp/ssh_mux_{user}_{target}"
        self.no_close = no_close
        
        self._closed = False
        atexit.register(self._cleanup)
    
    def port_forward(self, local_port, remote_port):
        """
        Creates a local port forward via existing multiplexed SSH session.
        Returns the subprocess.Popen object for the forwarding process.
        """
        cmd = [
            "ssh",
            "-S", self.mux_path,
            "-L", f"{local_port}:localhost:{remote_port}",
            "-N",  # no remote command
            f"{self.user}@{self.target}"
        ]
        
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
        except:
            return None

        return proc
        
    def start(self):
        """Start the persistent master connection"""
        if os.path.exists(self.mux_path):
            print("REUSING CONN")
            # Already exists, assume running
            return
        cmd = [
            "ssh",
            "-M",
            "-S", self.mux_path,
            "-f",
            "-N"
        ]
        
        if self.jump:
            cmd += ["-J", f"{self.user}@{self.jump}"]
        cmd += [f"{self.user}@{self.target}"]
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"Master connection started: {self.mux_path}")
        
    def close(self):
        """Stop the persistent master connection"""
        
        if self.no_close:
            return
        
        if os.path.exists(self.mux_path):
            subprocess.run(["ssh", "-S", self.mux_path, "-O", "exit", f"{self.user}@{self.target}"])
            print("Master connection closed")
            
    
    def _cleanup(self):
        if getattr(self, "_closed", False):
            return
        self._closed = True
        print("Closing SSH connections…")
        self.close()
        
            
