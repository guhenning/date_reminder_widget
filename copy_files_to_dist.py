import shutil
import os

# Path to the icons folder
icons_folder_path = "icons"

# Path to the build folder
build_folder_path = "dist"

# Create the build folder if it doesn't exist
if not os.path.exists(build_folder_path):
    os.makedirs(build_folder_path)

# Copy the icons folder to the build folder
shutil.copytree(icons_folder_path, os.path.join(build_folder_path, "icons"))
print("Icon Files Added to 'dist' folder successfully")
