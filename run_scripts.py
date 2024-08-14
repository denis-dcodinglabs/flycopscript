import subprocess
from concurrent.futures import ThreadPoolExecutor

# List of scripts to run
scripts = ['rfly.py', 'prishtinaticket.py', 'kosfly.py', 'flyska.py', 'ark.py' , 'airprishtina.py']

def run_script(script):
    """Run a script using subprocess."""
    result = subprocess.run(['python', script], capture_output=True, text=True)
    return result.stdout, result.stderr

def main():
    with ThreadPoolExecutor(max_workers=len(scripts)) as executor:
        futures = [executor.submit(run_script, script) for script in scripts]
        for future in futures:
            stdout, stderr = future.result()
            if stdout:
                print(f"Output from script:\n{stdout}")
            if stderr:
                print(f"Error from script:\n{stderr}")

if __name__ == '__main__':
    main()