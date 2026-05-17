from pathlib import Path
import tempfile, os, subprocess

def get_items(path):
    items = []
    for item in path.iterdir():
        items.append(item.name)

    return items

def upload_play_file(file_name, downloaded):
    with tempfile.TemporaryDirectory() as tmpdir:

        file_path = os.path.join(tmpdir, file_name)
        with open(file_path, "wb") as f:
            f.write(downloaded)
            
        subprocess.run(
            file_path,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmpdir,
            shell=True
            )
            