import os
import zipfile
from datetime import datetime

def create_epub(source_dir, output_epub):
    def get_files_recursively(directory):
        file_paths = []
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, directory)
                file_paths.append((filepath, relative_path))
        return file_paths

    with zipfile.ZipFile(output_epub, 'w', zipfile.ZIP_DEFLATED) as epub:
        
        mimetype_path = os.path.join(source_dir, 'mimetype')
        if os.path.exists(mimetype_path):
            zinfo = zipfile.ZipInfo('mimetype', datetime.now().timetuple()[:6])
            zinfo.compress_type = zipfile.ZIP_STORED
            
            with open(mimetype_path, 'rb') as f:
                epub.writestr(zinfo, f.read())
        
        files = get_files_recursively(source_dir)
        for filepath, relative_path in files:
            if relative_path != 'mimetype':  
                zinfo = zipfile.ZipInfo(relative_path, datetime.now().timetuple()[:6])
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                
                with open(filepath, 'rb') as f:
                    epub.writestr(zinfo, f.read())
        
        print(f"Created EPUB at: {os.path.abspath(output_epub)}")

if __name__ == '__main__':
    source_directory = '/path/to/your/readmoo/folder'  # Use your absolute path here
    output_file = 'output.epub'
    create_epub(source_directory, output_file)
