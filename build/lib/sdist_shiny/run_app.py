import subprocess

def main():
    subprocess.run(["shiny", "run", "--reload", "-b", "sdist_shiny/app.py"], check=True)

if __name__ == "__main__":
    main()