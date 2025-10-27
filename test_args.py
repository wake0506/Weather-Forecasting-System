#!/usr/bin/env python3
"""
Test command line arguments
"""

import sys
import subprocess

def run_command(cmd):
    """Run command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Errors:\n{result.stderr}")
    print("-" * 50)
    return result.returncode == 0

def main():
    print("Testing command line arguments...")
    
    tests = [
        "python src/main.py --help",
        "python src/main.py --city Beijing",
        "python src/main.py --city Shanghai --threshold 35",
        "python src/main.py --city Guangzhou --threshold 30 --verbose",
        "python src/main.py --city Shenzhen --threshold 40",
    ]
    
    all_passed = True
    
    for test in tests:
        if not run_command(test):
            all_passed = False
    
    if all_passed:
        print("All argument tests passed!")
    else:
        print("Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
