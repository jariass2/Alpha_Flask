# Documentation for Profit and Loss (P&L) Data Generation Script

## 1. Brief Explanation of the Code

This script takes processed accounting data (the output from the *previous* script) and a "Masterfile" containing P&L categories, and combines them to create Profit and Loss (P&L) reports. Think of it like taking summarized accounting data for each store and a template for a P&L statement, and then filling in the template with the store's data.  The script generates P&L reports in both CSV and Excel formats, placing them in a designated folder. It solves the problem of manually creating P&L reports by automating the process.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting Up the Workspace and Configuration

This section sets up the necessary file paths. It specifies:

*   Where to find the "Masterfile" (a template for the P&L).
*   Where the input data files (from the previous script) are located.
*   Where to save the final P&L reports.

It's like organizing your workspace before a project – knowing where your tools and materials are, and where the finished product will go. It also prepares the computer to use the spanish style for numbers (using commas for thousands and points for decimals)

### Section 2: Loading the Masterfile

This section defines a task to load the P&L "Masterfile".  This Masterfile acts like a template, defining the structure and categories of the P&L report. It adds a new empty column, ready to receive the financial numbers.

### Section 3: Getting the List of Input Files

This section defines a task to get a list of all the CSV files (the output from the previous script) in the input directory. These files contain the summarized accounting data for each store.

### Section 4: Processing Each Input File

This section defines the core task of combining the Masterfile with the data from each input CSV file.  For each store's data file:

1.  **Loads Data:** It reads the store's summarized accounting data.
2.  **Checks Data:** It verifies that the store's data file has the necessary columns. If not, it skips the file and prints a warning.
3.  **Matches and Sums:** It goes through each line of the P&L Masterfile. For each line, it finds the matching accounting codes in the store's data and sums up the corresponding values.  It's like finding all the "Revenue" entries in the store's data and adding them up.
4.  **Updates Masterfile:** It puts the calculated sum into the 'imeapu' column of the Masterfile. So, the Masterfile now has the P&L categories *and* the calculated values for that store.

### Section 5: Formatting Numbers

This section defines a task to format the numbers in European style (e.g., 1.234,56 instead of 1,234.56).

### Section 6: Saving the P&L Reports

This section defines a task to save the updated Masterfile (which now contains the P&L data) as both a CSV file and an Excel file. It names the output files based on the input file name and adds "_PyG" to indicate it's a P&L report.  The excel file sheet name is determined by the month found in the name of the input file.

### Section 7: Extracting the Month

This defines a task to get the month from the input file name. This month is used for naming the output files and creating a descriptive sheet name within the Excel file.

### Section 8: Running Everything

This section is the main part of the script. It does the following:

1.  **Creates Output Folder:** It makes sure the output folder exists.
2.  **Sets Up Locale:** Sets up the spanish format for numbers.
3.  **Loads Masterfile:** It loads the P&L Masterfile template.
4.  **Processes Each File:** It loops through each CSV file in the input directory (the output from the previous script):
    *   Prints the name of the file being processed.
    *   Resets values in masterfile
    *   Processes the file (combining the Masterfile with the store's data, as described in Section 4).
    *   Saves the updated Masterfile as a P&L report (both CSV and Excel).
5.  **Prints Completion Message:** It prints a message indicating the process is complete.

## 3. Inputs Used

| Input Name       | Type | Description                                                                                  | Constraints                                                                           | Source                                                         |
| ---------------- | ---- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Masterfile\_PyG  | File | A CSV file containing the P&L categories and structure.                                      | Must be a CSV file named `Masterfile_PyG.csv` in the `POC/MASTERFILES/` folder. | `POC/MASTERFILES/` folder                                  |
| Store Data Files | File | CSV files containing the summarized accounting data for each store (output from previous script). | Must be CSV files located in the `POC/SUMAS_Y_SALDOS/FINAL_RESULT/` folder.            | `POC/SUMAS_Y_SALDOS/FINAL_RESULT/` folder (from previous script) |

## 4. Outputs Generated

| Output Name           | Type  | Description                                                                            | Conditions                                                                                          | Destination              |
| --------------------- | ----- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------ |
| P&L Reports (CSV)     | File  | P&L reports in CSV format, one for each input store data file.                           | One file is created for each processed input file.                                                  | `POC/PyG_mes/` folder    |
| P&L Reports (Excel) | File  | P&L reports in Excel format, one for each input store data file, with sheet name by month. | One file is created for each processed input file, with sheet name derived from the input file name. | `POC/PyG_mes/` folder    |

## 5. Final Summary

This script automates the creation of Profit and Loss (P&L) reports from summarized accounting data.  It takes the output of a previous data processing script and a P&L template (the Masterfile) and generates individual P&L reports for each store, saving them as both CSV and Excel files. This eliminates the need to manually create P&L reports, saving time and reducing the risk of errors. It provides a streamlined and consistent way to generate essential financial reports.
