from cx_Freeze import setup, Executable
import sys
import os
import subprocess

# Define the build options
build_options = {
    "packages": ["playwright", "bs4", "dotenv"],
    "include_files": [
        ("C:/Users/PC/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/site-packages/playwright", "lib/playwright"),
    ],
}

# Define the executables
executables = [Executable("kosfly.py", base=None)]

# Post-build script to install Playwright browsers
def install_playwright_browsers(build_dir):
    playwright_path = os.path.join(build_dir, "lib", "playwright")
    subprocess.run([sys.executable, "-m", "playwright", "install"], cwd=playwright_path)

# Setup configuration
setup(
    name="FlightScraper",
    version="1.0",
    description="A script to scrape flight information",
    options={"build_exe": build_options},
    executables=executables,
)

# Run the post-build script
build_dir = os.path.join(os.getcwd(), "build", "exe.win-amd64-3.12")
install_playwright_browsers(build_dir)