import os

# Define the root directory
root_dir = r"E:\spoof photos\extracted photos\CelebA_Spoof\Data"

# Walk through all directories and files
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".txt"):
            file_path = os.path.join(foldername, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

print("Deletion process completed.")
