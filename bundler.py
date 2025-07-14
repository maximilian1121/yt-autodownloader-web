import os
import shutil
import zipfile

repo_name = os.path.basename(os.getcwd()).replace('-', '_').replace(' ', '_')
bundle_path = f"{repo_name}.py"

with open(bundle_path, 'w') as outfile:
    outfile.write(f"# Auto-generated bundled script for {repo_name} WINDOWS/OTHER\n")
    outfile.write(f"import app\n")
    
with open(repo_name, 'w') as outfile:
    outfile.write("#!/usr/bin/env python\n")
    outfile.write(f"# Auto-generated bundled script for {repo_name} LINUX\n")
    outfile.write(f"import app\n")
    
with zipfile.ZipFile('bundled.zip', 'w', compression=zipfile.ZIP_DEFLATED) as my_zip:
    my_zip.write(bundle_path, arcname=bundle_path)
    my_zip.write(repo_name, arcname=repo_name)
    
    # Recursively add the entire folder with all files
    for foldername, subfolders, filenames in os.walk(f"app"):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # This keeps the folder structure inside the zip
            arcname = os.path.relpath(file_path, os.path.dirname(f"app"))
            my_zip.write(file_path, arcname=arcname)

os.remove(bundle_path)
os.remove(repo_name)

print(f"[✓] Created {bundle_path}")
