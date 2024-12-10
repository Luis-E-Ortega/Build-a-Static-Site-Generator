import shutil
import os

def main():
    copy_static("static", "public")


def copy_static(src_path, dest_path):
    # Check if destination exists before removing
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    
    # Create the new destination directory
    os.mkdir(dest_path)

    # List of contents of source directory
    dir_list = os.listdir(src_path)

    for entry in dir_list:
        # Create full paths
        src_entry = os.path.join(src_path, entry)
        dest_entry = os.path.join(dest_path, entry)

        if os.path.isfile(src_entry):
            print(f"Copying file: {src_entry}")
            shutil.copy(src_entry, dest_entry)
        elif os.path.isdir(src_entry):
            print(f"Copying file: {src_entry}")
            copy_static(src_entry, dest_entry)


if __name__ == "__main__":
    main()
