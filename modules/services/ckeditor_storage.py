from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime


class CKEditorStorage(FileSystemStorage):
    def get_folder_name(self):
        return datetime.now().strftime('%Y/%m/%d')

    def _save(self, name, content):
        file_path = Path(self.get_folder_name()).joinpath(name)
        return super()._save(file_path, content)
    
    location = settings.MEDIA_ROOT / 'ckeditor_uploads/'
    base_url = urljoin(settings.MEDIA_URL, 'ckeditor_uploads/')
        