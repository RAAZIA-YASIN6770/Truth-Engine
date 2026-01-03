import os
import shutil
import stat

def on_rm_error(func, path, exc_info):
    """
    Error handler for shutil.rmtree to delete read-only files (like .git files).
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_project():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Cleaning project at: {root_dir}")
    
    # 1. Remove incorrect files from root (duplicates or unused)
    files_to_delete = [
        "manage.py",       # Django file (incorrect)
        "routes.py",       # Duplicate (should be in app/)
        "settings.json"    # Duplicate (should be in .vscode/)
    ]
    
    for file in files_to_delete:
        file_path = os.path.join(root_dir, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file}")
            except OSError as e:
                print(f"Error deleting {file}: {e}")

    # 2. Fix nested git repositories (The cause of 'fatal: adding files failed')
    # We look for folders like 'Truth-Engine' that contain a .git folder
    subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    
    for d in subdirs:
        if d in ['.git', '.vscode', 'app', '__pycache__', 'venv']:
            continue
            
        nested_git = os.path.join(root_dir, d, ".git")
        if os.path.exists(nested_git):
            print(f"Found nested git repository in: {d}/")
            # Remove the .git folder so it becomes just a normal folder
            shutil.rmtree(nested_git, onerror=on_rm_error)
            print(f"Fixed: Removed nested .git config from {d}/")

    # 3. Move files to correct structure
    moves = {
        "scenario_1.json": "data/scenario_1.json",
        "scenario_loader.py": "app/services/scenario_loader.py",
        "__init__.py": "app/services/__init__.py",
        "app/scenario.html": "app/templates/scenario.html"
    }
    
    for src, dest in moves.items():
        src_path = os.path.join(root_dir, src)
        dest_path = os.path.join(root_dir, dest)
        
        if os.path.exists(src_path):
            # Ensure dest dir exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            try:
                shutil.move(src_path, dest_path)
                print(f"Moved: {src} -> {dest}")
            except Exception as e:
                print(f"Error moving {src}: {e}")

if __name__ == "__main__":
    clean_project()
    print("\nCleanup complete. You can now run git commands.")