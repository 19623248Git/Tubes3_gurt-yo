import os
from collections import defaultdict
from pprint import pprint

class DirectoryScanner:
    
        """
        Scans subdirectories for files
        provides methods to display and access data
        """

        def __init__(self, base_dir: str):
                
                """
                Initializes the DirectoryScanner and collects all file paths.
                @param base_dir (str) The path to the root directory to scan (e.g., '../data' from src).
                """

                self.base_dir = base_dir
                self.file_path_map = self._collect_file_paths()
                # Get absolute path for display
                self.abs_base_dir = os.path.abspath(self.base_dir)

        def getMap(self) -> dict:
                
                """
                Returns the raw dictionary map of the scanned file structure.

                The dictionary structure will be:
                {
                'SUBDIRECTORY_NAME_1': ['path/to/file1.pdf', 'path/to/file2.pdf'],
                'SUBDIRECTORY_NAME_2': ['path/to/file3.pdf'],
                ...
                }
                """
                return self.file_path_map

        def _collect_file_paths(self) -> dict:
                """
                Scans subdirectories and collects all file paths. Internal method.
                """
                file_map = defaultdict(list)
                if not os.path.isdir(self.base_dir):
                        return {}
                try:
                        for item in sorted(os.listdir(self.base_dir)):
                                full_path = os.path.join(self.base_dir, item)
                                if os.path.isdir(full_path):
                                        try:
                                                files = sorted([f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))])
                                                for file_name in files:
                                                        relative_path = os.path.join(self.base_dir, item, file_name)
                                                        normalized_path = relative_path.replace('\\', '/')
                                                        file_map[item].append(normalized_path)
                                        except OSError:
                                                pass # Silently ignore directories we can't access
                        return dict(file_map)
                except OSError:
                        return {}

        def _get_emoji_for_file(self, file_path: str) -> str:
                """Returns a suitable emoji based on the file extension."""
                extension_map = {
                '.pdf': '📕', '.csv': '📊', '.xlsx': '📊', '.docx': '📝',
                '.txt': '📄', '.md': '📄', '.json': '⚙️', '.xml': '⚙️',
                '.zip': '📦', '.rar': '📦',
                }
                ext = os.path.splitext(file_path)[1].lower()
                return extension_map.get(ext, '📄')

        def displayAsTree(self):
                """
                Displays the entire directory structure as a visual tree.
                """
                if not self.file_path_map:
                        print(f"Directory '{self.base_dir}' is empty or could not be read.")
                        return

                print(f"📁 {os.path.basename(self.abs_base_dir)}")
                subdirs = list(self.file_path_map.keys())
                for i, subdir_name in enumerate(subdirs):
                        is_last_subdir = (i == len(subdirs) - 1)
                        subdir_prefix = "└──" if is_last_subdir else "├──"
                        print(f"{subdir_prefix} 📁 {subdir_name}")

                        connection_prefix = "    " if is_last_subdir else "│   "
                        files_in_subdir = self.file_path_map[subdir_name]
                        for j, file_path in enumerate(files_in_subdir):
                                is_last_file = (j == len(files_in_subdir) - 1)
                                file_prefix = "└──" if is_last_file else "├──"
                                file_name = os.path.basename(file_path)
                                emoji = self._get_emoji_for_file(file_name)
                                print(f"{connection_prefix}{file_prefix} {emoji} {file_name}")

        def driverTest(self):
                # The path to the directory is passed here, when creating the class instance.
                data_directory_path = os.path.join('..', 'data')

                # Create a dummy directory structure for demonstration if it doesn't exist
                if not os.path.exists(data_directory_path):
                        print("Creating dummy 'data' directory for demonstration...")
                        os.makedirs(os.path.join(data_directory_path, 'invoices'))
                        os.makedirs(os.path.join(data_directory_path, 'reports'))
                        os.makedirs(os.path.join(data_directory_path, 'Archive'))
                        with open(os.path.join(data_directory_path, 'invoices', 'inv_001.pdf'), 'w') as f: f.write('')
                        with open(os.path.join(data_directory_path, 'invoices', 'inv_002.csv'), 'w') as f: f.write('')
                        with open(os.path.join(data_directory_path, 'reports', 'report_q1.docx'), 'w') as f: f.write('')
                        with open(os.path.join(data_directory_path, 'reports', 'summary.xlsx'), 'w') as f: f.write('')
                        with open(os.path.join(data_directory_path, 'Archive', 'old_data.zip'), 'w') as f: f.write('')
                        print("Dummy structure created.\n")

                print("Scanning directory and generating tree...\n")
                # The 'data_directory_path' is passed to the constructor here.
                scanner = DirectoryScanner(data_directory_path)

                # 1. Display the final output in the requested tree format
                scanner.displayAsTree()

                print("\n" + "---" + "\n")

                # 2. Demonstrate the new getMap() method
                print("Demonstrating the getMap() method...")
                print("This method returns the raw Python dictionary of the file structure.\n")
                
                # Get the map from the scanner instance
                file_map_data = scanner.getMap()

                # Use pprint for a clean, readable print of the dictionary
                print("Contents of the map:")
                pprint(file_map_data)

