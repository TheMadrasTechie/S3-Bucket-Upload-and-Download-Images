import os
import shutil

# Define the root directory
root_dir = r"E:\spoof photos\extracted photos\CelebA_Spoof\Data"

# Iterate over the train and test folders
for main_folder in ["train", "test"]:
    main_folder_path = os.path.join(root_dir, main_folder)

    # Ensure live and spoof folders exist in train and test
    for category in ["live", "spoof"]:
        target_folder = os.path.join(main_folder_path, category)
        os.makedirs(target_folder, exist_ok=True)

    # Traverse all subfolders (e.g., 10161, 10234, etc.)
    for subfolder in os.listdir(main_folder_path):
        subfolder_path = os.path.join(main_folder_path, subfolder)

        # Ensure it's a directory
        if os.path.isdir(subfolder_path):
            # Move files from 'live' and 'spoof' into the respective main category folders
            for category in ["live", "spoof"]:
                category_folder_path = os.path.join(subfolder_path, category)
                target_folder = os.path.join(main_folder_path, category)

                if os.path.isdir(category_folder_path):
                    for file_name in os.listdir(category_folder_path):
                        file_path = os.path.join(category_folder_path, file_name)
                        new_location = os.path.join(target_folder, file_name)

                        if os.path.isfile(file_path):
                            try:
                                shutil.move(file_path, new_location)
                                print(f"Moved: {file_path} -> {new_location}")
                            except Exception as e:
                                print(f"Error moving {file_path}: {e}")

print("File reorganization completed.")
