# Stores the timestamp of each file and scans build files for changes
import os

class Timestamp:
    def __init__(self, root_folder: str):
        self._locations = {
            "html": os.path.join(root_folder, "html"),
            "pages": os.path.join(root_folder, "pages")
        }

        # Store (folder-name, timestamp)
        self._timestamps = {}
    
    # Updates timestamp dictionary
    def update_times(self):
        for folder in ["html", "pages"]:
            for file in os.listdir(self._locations[folder]):
                if file != "__pycache__":
                    path = os.path.join(self._locations[folder], file)
                    self._timestamps[f"{folder}-{os.path.basename(file)}"] = os.path.getmtime(path)
    
    # Compares timestamp and returns True if the timestamp is different
    def compare_times(self) -> bool:
        for folder in ["html", "pages"]:
            for file in os.listdir(self._locations[folder]):
                if file != "__pycache__":
                    path = os.path.join(self._locations[folder], file)
                    different = self._timestamps[f"{folder}-{os.path.basename(file)}"] != os.path.getmtime(path)
                    return different