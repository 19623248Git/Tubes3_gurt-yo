import sys
print(sys.prefix)
print(sys.base_prefix)

# Check if the script is running in a virtual environment
if sys.prefix != sys.base_prefix:
        print("Running in a virtual environment.")
else:
        print("Not running in a virtual environment.")
        print("Please activate the virtual environment before running this script.")
        sys.exit(1)