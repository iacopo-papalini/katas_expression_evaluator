import os
import subprocess
import webbrowser


def main():
    subprocess.call(["coverage", "erase"])
    subprocess.call(["coverage", "run", "--module", "pytest"])
    subprocess.call(["coverage", "html"])
    webbrowser.open("file://" + os.getcwd() + "/htmlcov/index.html", new=2)


if __name__ == "__main__":
    main()
