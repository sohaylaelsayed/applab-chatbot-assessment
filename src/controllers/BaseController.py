from helpers.config import get_settings, Settings
from helpers.constants import AppConstants
import os



class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()

        self.base_dir = os.path.dirname( os.path.dirname(__file__) )
        self.files_dir = os.path.join(
            self.base_dir,
            AppConstants.FILE_PATH
        )
        
    def get_database_path(self):
        return os.path.join(self.base_dir, AppConstants.QDRANT_DIR_PATH)
