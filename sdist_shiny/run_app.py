import subprocess
from pathlib import Path

def main():
    dir = Path(__file__).resolve().parent
    subprocess.run(["shiny", "run", "--reload", "-b", f"{str(dir)}/app.py"], check=True)

if __name__ == "__main__":
    main()