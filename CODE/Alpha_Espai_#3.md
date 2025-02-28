# Documentation for Spreadsheet Worksheet Copying Script

## 1. Brief Explanation of the Code

This script takes monthly Profit and Loss (P&L) reports (the Excel files created by the *second* script) and adds them as new sheets to a yearly P&L file. It's like having a separate notebook for each month's P&L, and then at the end of the month, copying the latest notebook into a master binder that holds all the monthly reports for the year. If the yearly file doesn't exist, the user is expected to create it. The script solves the problem of manually compiling monthly reports into a yearly overview.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting Up the Workspace and Configuration

This section defines the file paths. It specifies:

*   Where the input monthly P&L files (from the second script) are located.
*   Where the output yearly P&L files are located (or should be created).

It is, again, setting up workspace.

### Section 2: Create Directory

This section makes sure that the input and output folders exits. If not, it creates them.

### Section 3: Extracting the Base File Name

This section defines a task to get the main part of the file name from the input files.  For example, if the input file is named "StoreA\_01\_PyG.xlsx", this section would extract "StoreA".  This base name is used to find or create the matching yearly file.

### Section 4: Getting Existing Yearly File Names

This section defines a task to get a list of all the existing yearly P&L files in the output directory. This is used to check if a yearly file already exists for a given store before adding new monthly data.

### Section 5: Extracting the Sheet Name

This section defines a task to get the sheet name from the input file name. For example, if the input file is called 'Store_01_pyg.xlsx, it extracts "01_PyG" to be the sheet name.

### Section 6: Running Everything

This is the main part of the script.  It does the following:

1.  **Starts:** Displays a starting message.
2.  **Checks/Creates Directories:** Makes sure the input and output folders exist.
3.  **Gets Existing Output Files:** It gets a list of all the existing yearly P&L files.
4.  **Processes Input Files:** It loops through each Excel file in the input directory (the monthly P&L files):
    *   Gets the base file name (e.g., "StoreA").
    *   Checks if a yearly file with the same base name exists in the output directory.
    *   **If the yearly file exists:**
        *   Reads all the sheets from the monthly file.
        *   Reads all sheets from the existing yearly file.
        *   Adds the monthly sheets to the yearly file (overwriting if a sheet with the same name already exists).
        *   Writes all data, with correct number format, to the yearly file (using a special method to ensure proper Excel formatting, with commas for decimals)
        *   Prints a success message.
    *   **If the yearly file doesn't exist:**
        *   Prints a warning message, indicating that the monthly file was skipped.
5.  **Prints Completion Message:** Prints a message indicating how many files were processed.
6. **Handles Errors:** If any error occurs, prints an error message and stops the script.

## 3. Inputs Used

| Input Name           | Type | Description                                                                        | Constraints                                                                          | Source                                   |
| -------------------- | ---- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------- |
| Monthly P&L Files | File | Excel files containing monthly P&L data (output from the second script).         | Must be Excel files (`.xlsx`) in the `POC/PyG_mes/` folder.                       | `POC/PyG_mes/` folder (from second script) |

## 4. Outputs Generated

| Output Name    | Type | Description                                                                                               | Conditions                                                                                                                              | Destination          |
| -------------- | ---- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| Yearly P&L Files | File | Excel files containing yearly P&L data, with each month's data added as a separate sheet.          | Updated (or created if not exits) in the `POC/PyG_anual/` folder. Each sheet is added/replaced with the corresponding monthly P&L data. | `POC/PyG_anual/` folder |

## 5. Final Summary

This script automates the process of compiling monthly Profit and Loss (P&L) reports into a yearly P&L file. It takes monthly Excel files, extracts the data, and adds it as new sheets to an existing yearly Excel file. This simplifies the task of creating a consolidated yearly view of P&L data, saving time and reducing the risk of manual errors. The user needs to create a yearly empty file before starting this process. The script handles the formatting and merging of data, providing a convenient way to track P&L performance over time.
