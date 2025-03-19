# Stores the timestamp of each file and scans build files for changes
import os

class Timestamp:
    def __init__(self, root_folder: str):
        self._locations = {
            "html": os.path.join(root_folder, "html"),
            "pages": os.path.join(root_folder, "pages")
        }

        # Store (folder-name, timestamp)
        self._timestamps = []
    
    # Creates a new list
    def build_new(self) -> list:
        files = []
        for folder in ["html", "pages"]:
            for file in os.listdir(self._locations[folder]):
                if file != "__pycache__":
                    path = os.path.join(self._locations[folder], file)
                    files.append(os.path.getmtime(path))
        return files
    
    # Updates timestamp dictionary
    def update_times(self):
        self._timestamps = self.build_new()
    
    # Compares timestamp and returns True if the timestamp is different
    def compare_times(self) -> bool:
        new = self.build_new()
        if len(new) != len(self._timestamps):
            return True
        else:
            for timestamp in new:
                if timestamp not in self._timestamps:
                    return True
            return False