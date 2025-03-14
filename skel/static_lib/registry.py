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
    
    def get_locations(self):
        print(self._timestamps)

    
    def scan_times(self):
        for folder in ["html", "pages"]:
            for file in os.listdir(self._locations[folder]):
                path = os.path.join(self._locations[folder], file)
                self._timestamps[f"{folder}-{os.path.basename(file)}"] = os.path.getmtime(path)
    
    def compare_times(self):
        pass

test_obj = Timestamp("skel")
test_obj.scan_times()
test_obj.get_locations()