# Documentation for Margen de Gestión Calculation Script

## 1. Brief Explanation of the Code
This script is like a financial assistant that helps to calculate and update important business figures. Imagine you have sales and purchase data scattered across different monthly Excel sheets, and you need to summarize these numbers to understand the 'Management Margin' (which is like the profit from your core business activities). This script automatically goes through these Excel files, extracts the necessary information for each month, and combines it.  It then uses a 'Masterfile' which is like a store directory to link this financial data to specific stores. Finally, it updates other files (called 'PyG files', which are like monthly performance reports for each store) with these calculated 'Management Margin' figures.  Essentially, it automates the process of collecting, calculating, and distributing key financial data to keep track of business performance.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting Things Up (Configuration and Preparation)
This part of the script is like setting up the tools and workspace before starting a job.

*   **Importing Tools:** It first imports necessary tools, which are like special software libraries. These tools help the script work with spreadsheets (like Excel files), manage data in tables, handle dates and times, and find patterns in text.
*   **Configuring Data Display:** It sets up how data will be shown, making it easier to read, especially when dealing with large tables of numbers.
*   **Defining File Locations:** It then specifies the exact locations of different folders on the computer where the script will find input files and save output files. Think of this as setting up addresses for different departments in an office (like 'Sales Data Department', 'Purchase Data Department', etc.). These folders include:
    *   `VENTAS_BRUTAS` (Gross Sales): Probably intended for sales data, although not directly used in the provided script.
    *   `COMPRAS_MERCANCIAS` (Merchandise Purchases): Likely for purchase data, also not directly used here.
    *   `PYG_MES` (Monthly P&L - Profit and Loss): Where monthly performance reports are stored.
    *   `MARGEN_CAJA` (Cash Margin): Where the main Excel file with margin data is located, and where the final results will be saved.
    *   `MASTERFILES`: Where the 'store directory' (Masterfile) is located.
*   **Setting Column Indexes:** It defines numbers that point to where specific information (like sales or purchase figures for each month) starts in the Excel files.
*   **Checking if Folders Exist:** The script verifies if all the necessary folders actually exist. If any folder is missing, it stops and informs the user, like checking if all departments are in the office before starting work.
*   **Finding the Right Excel File:** It looks for a specific Excel file in the 'MARGEN_CAJA' folder. It searches for a file that starts with 'Margen_Demarca' and ends with '.xlsx'. If it cannot find this file, it stops and informs the user, like making sure the correct source document is on the desk.
*   **Determining Months to Process:** The script figures out which months it needs to process. It looks at the current month and decides to process data up to the month before the current one. For example, if it's October, it will process data from January to September.  There's also a line specifically to "force" the current month to October for testing purposes, so it processes up to September even if it's actually a later month.
*   **List of Months:** It creates a list of all months in a year (January to December) as a reference.
*   **Months to be Processed:** Based on the current month (or forced month for testing), it creates a list of months that need to be processed. For instance, if the current month is set to October, this list will be January, February, ..., September.

### Section 2: Data Collection and Combination (Data Aggregation)
This section is the core of the script where it gathers and combines data from different Excel sheets.

*   **Function `aggregate_data`:** This is a reusable block of instructions (a function) designed to collect and combine the 'Management Margin', 'Sales', and 'Purchases' data. It takes the Excel file path and the list of months to process as input.
*   **Iterating through Months:** It goes through each month in the list of months to be processed (e.g., January, February, ..., September).
*   **Finding the Correct Sheet for Each Month:** For each month, it looks for a sheet in the Excel file whose name starts with the month's name (e.g., for January, it looks for a sheet named 'January', 'JANUARY', 'Jan-Data', etc.).
*   **Processing Each Month's Sheet:** If it finds a sheet for a month:
    *   **Reading Sheet Data:** It reads the data from the Excel sheet into a table-like structure.
    *   **Filtering for 'Total' Rows:** It looks for rows in the sheet that have the word "Total" in a specific column (column 8, technically the 9th column as counting starts from 0). These "Total" rows likely contain summarized data for each store.
    *   **Going through Each 'Total' Row:** For each 'Total' row, it extracts:
        *   **'ATICA code'**: This is like a store ID, found in the first column (column 0). It cleans up this code by removing extra spaces.
        *   **Financial Figures:** It tries to extract 'Management Margin', 'Sales', and 'Purchases' from specific columns (28, 24, and 26 respectively). It handles cases where these values might be missing or not in the correct format (numbers). If there's an issue reading a value, it assumes it's zero and notes the problem.
        *   **Accumulating Data:** For each 'ATICA code', it adds up the 'Management Margin', 'Sales', and 'Purchases' from all processed months. This is like adding up monthly sales figures to get a year-to-date total.
*   **Handling Missing Sheets or Errors:** If it can't find a sheet for a month or encounters any errors while processing a sheet (like a sheet not having enough columns or data being in the wrong format), it prints a warning message and continues with the next month.
*   **Storing Combined Data:** All the aggregated data (total 'Management Margin', 'Sales', and 'Purchases' for each 'ATICA code') is stored in a temporary storage (a dictionary).
*   **Returning Combined Data:** The function finally returns this combined data.

### Section 3: Preparing Data for Reports (Masterfile Integration and Data Structuring)
This part takes the combined data and prepares it for use in reports and updates.

*   **Creating a Table from Combined Data:** It takes the aggregated data (which was in a dictionary) and converts it into a table-like structure (DataFrame), making it easier to work with.
*   **Setting 'ATICA' as Store Identifier:** It sets the 'ATICA code' as the main identifier for each row in the table, like using store names as labels.
*   **Loading Store Directory (Masterfile):** It loads the 'Masterfile', which is a CSV file, into another table. This Masterfile contains information about each store, including its 'ATICA code', 'Store Number' ('TIENDA'), and 'Establishment Code' ('EST').
*   **Ensuring Masterfile has Necessary Information:** It checks if the Masterfile contains the columns 'ATICA', 'TIENDA', and 'EST'. If any of these are missing, it stops and informs the user, as this information is crucial for linking financial data to stores. It also ensures that the 'Establishment Code' is treated as a number and 'ATICA' as text to avoid issues when combining data.
*   **Combining Financial Data with Store Information:** It merges the aggregated financial data with the store information from the Masterfile using the 'ATICA code' as the link. This is like joining the financial performance data with the store directory to know which financial figures belong to which store. If a store in the Masterfile doesn't have financial data, it will still be included, but its financial figures will be marked as missing initially.
*   **Cleaning and Ordering the Final Table:**
    *   It ensures 'Establishment Code' is treated as a number again.
    *   It selects and reorders the columns in the final table to be 'ATICA', 'EST', 'TIENDA', 'Management Margin', 'Sales', and 'Purchases'.
    *   It sorts the table by 'ATICA code' for better organization.
    *   It fills in any missing 'Management Margin', 'Sales', or 'Purchases' values with zero and rounds all these financial figures to two decimal places, making the data cleaner and ready for reporting.

### Section 4: Updating Performance Reports (PyG Files Update)
This section takes the calculated 'Management Margin' and updates individual store performance reports.

*   **Function `update_pyg_files`:** This is another reusable block of instructions that updates the 'PyG files' (monthly performance reports) with the calculated 'Management Margin'. It takes the prepared data table and the folder where 'PyG files' are located as input.
*   **Ensuring 'Establishment Code' is a Number:** It makes sure the 'Establishment Code' in the data table is treated as a number.
*   **Processing Each PyG File:** It goes through each file in the 'PYG_MES' folder.
*   **Identifying Store from Filename:** For each file, it tries to find the 'Establishment Code' from the filename. It assumes the filename contains '_[Establishment Code]_' pattern (e.g., a filename might be 'PYG_Store_123_Month.csv', where '123' is the 'Establishment Code').
*   **Finding Matching Store Data:** Using the extracted 'Establishment Code', it looks for the corresponding store's data in the prepared data table.
*   **Extracting 'Management Margin':** If it finds a match, it extracts the calculated 'Management Margin' for that store. If the 'Management Margin' is missing or not a valid number, it assumes it's zero.
*   **Reading PyG File Data:** It reads the content of the 'PyG file' into a table.
*   **Updating 'Management Margin' in PyG File:** It looks for a row in the 'PyG file' where the 'concept' is 'MARGEN CAJA' (Cash Margin). If found, it updates the 'imeapu' (likely a value column) in that row with the calculated 'Management Margin' value.
*   **Saving Updated PyG File:** It saves the updated 'PyG file', overwriting the old version.
*   **Handling Errors and Missing Data:** If it encounters errors like not finding a store's data, issues reading 'PyG files', or if the 'PyG file' doesn't have the expected columns ('concepto' and 'imeapu'), it prints warning messages and continues processing other files.

### Section 5: Final Actions (Output and Script Execution)
This is the final part that executes the main tasks and saves the results.

*   **Main Execution Block (`if __name__ == "__main__":`)**: This ensures that the following code only runs when the script is executed directly (not when imported as a tool into another script).
*   **Saving Combined Data to CSV:** It saves the final table containing 'ATICA', 'EST', 'TIENDA', 'Management Margin', 'Sales', and 'Purchases' to a CSV file named 'Margenes_Ventas_Compras.csv' in the 'MARGEN_CAJA' folder. This file serves as a summary report of the calculated margins, sales, and purchases. It also prints the content of this table to the screen.
*   **Updating PyG Files:** It calls the `update_pyg_files` function to update all the 'PyG files' in the 'PYG_MES' folder with the calculated 'Management Margin' values.

## 3. Inputs Used

| Input Name | Type | Description | Constraints | Source |
|------------|------|-------------|-------------|------------------|
| **Margen Excel File** | `.xlsx` file | Excel file containing monthly 'Management Margin', 'Sales', and 'Purchases' data, organized in sheets named after months (e.g., "ENERO", "FEBRERO"). | File name must start with 'Margen_Demarca' and end with '.xlsx'. Sheets should have a specific structure with 'Total' rows and columns for required data. | Located in the `MARGEN_CAJA` directory. |
| **Masterfile (Masterfile_CODIGOS.csv)** | `.csv` file | CSV file containing store information, including 'ATICA code', 'Store Number' ('TIENDA'), and 'Establishment Code' ('EST'). | Must contain columns named 'ATICA', 'TIENDA', and 'EST'. 'EST' should be numeric, 'ATICA' should be a string. | Located in the `MASTERFILES` directory. |
| **PyG Files (Monthly Performance Reports)** | `.csv` files | CSV files representing monthly performance reports for each store. Filenames are expected to contain '_[Establishment Code]_' to identify the store. | Must be CSV files. Expected to have columns named 'concepto' and 'imeapu'. | Located in the `PYG_MES` directory. |

## 4. Outputs Generated

| Output Name | Type | Description | Conditions | Destination |
|-------------|------|-------------|------------|-----------------------|
| **Margenes_Ventas_Compras.csv** | `.csv` file | A CSV file summarizing the aggregated 'Management Margin', 'Sales', and 'Purchases' for each store ('ATICA') along with store information ('EST', 'TIENDA'). | Generated every time the script is run successfully. | Saved in the `MARGEN_CAJA` directory. |
| **Updated PyG Files** | `.csv` files | The original PyG files in the `PYG_MES` directory are modified. The 'imeapu' value for the 'concepto' "MARGEN CAJA" is updated with the calculated 'Management Margin' for each corresponding store. | Updated for each PyG file for which a matching store and 'Management Margin' is found. | Overwrites the original files in the `PYG_MES` directory. |
| **Console Output (Print Statements)** | Text messages | Messages printed to the console during script execution, indicating progress, warnings, or errors. | Generated during script execution to provide feedback on the process. | Displayed on the user's screen when running the script. |

## 5. Final Summary
This script is a helpful tool that simplifies the process of understanding business performance. Imagine you need to know the 'Management Margin' for all your stores each month. Instead of manually going through many Excel sheets and adding up numbers, this script does it automatically. It reads sales and purchase data from monthly Excel reports, combines this data, and links it to your stores using a store directory.  The script then calculates the total 'Management Margin', 'Sales', and 'Purchases' for each store and creates a summary report in a new file.  Furthermore, it updates your individual store performance reports with these calculated 'Management Margin' figures, ensuring all your reports are up-to-date with this important information. This saves time and effort, and reduces the chance of errors when dealing with large amounts of financial data, giving you a clear and quick overview of your business's financial health.