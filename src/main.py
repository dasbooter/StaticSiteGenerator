import os
import shutil

def copy_static_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            # Recursively copy directory
            print(f"Copying directory {src_path} to {dest_path}")
            copy_static_files(src_path, dest_path)
        else:
            # Copy file
            print(f"Copying file {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)

def main():
    src_dir = 'static'
    dest_dir = 'public'

    copy_static_files(src_dir, dest_dir)
    print("Static files copied successfully!")

if __name__ == "__main__":
    main()
