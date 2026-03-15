import os
import subprocess
import tempfile
import time
import resource
from typing import Dict, Any, Tuple

class Sandbox:
    """
    Executes code in an isolated environment.
    Note: Real production environments use Docker/gVisor.
    This implementation uses local subprocesses with resource limits 
    for macOS / Linux compatibility.
    """
    def __init__(self, time_limit: float = 2.0, memory_limit_mb: int = 128):
        self.time_limit = time_limit
        self.memory_limit_mb = memory_limit_mb

    def execute_python(self, code: str, input_data: str) -> Dict[str, Any]:
        """
        Executes Python code.
        Returns a dictionary with stdout, stderr, execution_time, memory_usage, and status.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "solution.py")
            with open(file_path, "w") as f:
                f.write(code)

            return self._run_command(["python3", file_path], input_data)

    def _set_resource_limits(self):
        """
        Sets resource limits for the child process.
        """
        try:
            # Memory limit in bytes
            mem_bytes = self.memory_limit_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
            
            # CPU time limit in seconds (add 1s buffer for python startup)
            cpu_time = int(self.time_limit) + 1
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_time, cpu_time))
        except (ValueError, OSError):
            # Limit setting might fail on some OS combinations (e.g. macOS native vs Linux)
            pass

    def _run_command(self, cmd: list, input_data: str) -> Dict[str, Any]:
        start_time = time.time()
        start_mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=self._set_resource_limits,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=self.time_limit)
                execution_time = time.time() - start_time
                
                # Fetch memory usage
                end_mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                # On macOS, ru_maxrss is in bytes. On Linux, it's in kilobytes.
                # Assuming macOS for this project execution environment:
                memory_usage_mb = max(0, (end_mem - start_mem)) / (1024 * 1024)
                
                status = "ACCEPTED"
                if process.returncode != 0:
                    status = "RUNTIME_ERROR"
                    
                return {
                    "stdout": stdout,
                    "stderr": stderr,
                    "execution_time": execution_time,
                    "memory_usage": memory_usage_mb,
                    "status": status,
                    "returncode": process.returncode
                }
                
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                return {
                    "stdout": "",
                    "stderr": "Time Limit Exceeded",
                    "execution_time": self.time_limit,
                    "memory_usage": 0.0,
                    "status": "TIME_LIMIT_EXCEEDED",
                    "returncode": -1
                }
                
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "execution_time": 0.0,
                "memory_usage": 0.0,
                "status": "SYSTEM_ERROR",
                "returncode": -1
            }

def run_code(language: str, code: str, input_data: str, time_limit: float = 2.0, memory_limit_mb: int = 256) -> Dict[str, Any]:
    sandbox = Sandbox(time_limit=time_limit, memory_limit_mb=memory_limit_mb)
    
    if language.lower() == "python":
        return sandbox.execute_python(code, input_data)
    else:
        return {
            "stdout": "",
            "stderr": f"Language {language} not supported yet.",
            "execution_time": 0.0,
            "memory_usage": 0.0,
            "status": "COMPILATION_ERROR",
            "returncode": -1
        }
