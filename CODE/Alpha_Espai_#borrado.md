## Documentation for File Cleanup App Code

## 1. Brief Explanation of the Code
This script is a simple tool designed to clear out old files. Imagine you have several folders on your computer that contain files you want to remove periodically. This script goes into each of those folders and deletes all the files it finds, leaving the folders empty and ready for new data. This helps in keeping your data organized and prevents the folders from getting full of unnecessary files.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting up the Workspace
This part prepares the script to run by setting the locations of the important folders. It defines the base folder and other folders within it for the data the script will interact with. This helps the script keep track of where all the important folders are located.

### Section 2: Creating a Directory (if needed)
This is a tool that checks to see if a folder exists. If it doesn't exist, the tool creates it, and displays a message saying so. This ensures that the script doesn't encounter any problems if the required folders do not exist before running.

### Section 3: Erasing files
This is the main tool of the script. It takes a folder as input, and:
    1. First, it makes sure the folder exists, creating it if necessary.
    2. Then, it looks into that folder and deletes every single file it finds.
    3. If there are no files, or if it encounters any errors, the tool will print a message to let you know.

### Section 4: Main Process
This is the part that executes the script.
    1.  It prints a message to the screen to indicate it has started working and the base folder where it will be working.
    2.  It makes sure that the main folders that the script works with all exist, creating them if necessary.
    3.  Then, it prints another message indicating that it's starting to erase files, and proceeds to erase the files in the specified folders one by one using the erasing tool from the previous section.
    4.  Finally, it prints a message to the screen to indicate that the script has finished all the steps.

## 3. Inputs Used

| Input Name | Type | Description | Constraints | Source |
|------------|------|-------------|-------------|------------------|
| None  | None |  This script does not take any direct input from the user. It automatically cleans up files from pre-defined folders. | None. The folders to be cleared are pre-defined in the script itself. | The code itself |

## 4. Outputs Generated

| Output Name | Type | Description | Conditions | Destination |
|-------------|------|-------------|------------|-----------------------|
| Cleared Directories |  Empty folder |  The folders defined in the script are cleared of all their files. | The script cleans up the folders every time that it's executed. | The pre-defined folders: `FINAL_RESULT`, `PyG_mes`, and `INTERMEDIATE` under the `SUMAS_Y_SALDOS` folder.  |
| Messages on Screen | Text |  The script displays messages to show its progress or any errors that it finds.  | These messages are displayed during the script’s execution. | The computer screen (terminal) |

## 5. Final Summary

This script is a file cleaning tool. It automatically removes all the files from several specific folders. It's useful for clearing old financial data before starting a new process, ensuring that the folders remain organized and without unnecessary files. By automating this process, this script saves time and reduces the possibility of errors.
