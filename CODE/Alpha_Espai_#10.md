# Documentation for Cash Margin Section Data Capture and PyG Update Script

## 1. Brief Explanation of the Code
This script is like a data organizer and updater for financial information. It focuses on 'Cash Margin', which is a key financial metric for businesses.  Imagine you have monthly reports in Excel files that detail 'Controlled' and 'Uncontrolled' shrinkage (like losses from damage or theft) for different product sections in your stores. This script automatically reads these Excel reports, gathers the shrinkage data for each store and product section, and then updates individual store performance reports (called 'PyG files') with this specific shrinkage information.  This process ensures that the store performance reports are always accurate and up-to-date with the latest shrinkage figures, giving a clearer picture of each store's financial health.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Script Setup and Configuration
This section is all about getting the script ready to work by setting up the necessary tools, locations, and instructions.

*   **Importing Tools:** The script starts by importing special tools (libraries) that help it perform tasks like working with spreadsheets (Excel files), managing data in tables, handling dates and times, and finding text patterns.
*   **Defining Settings:** It then sets up various configuration parameters. These are like pre-set instructions that tell the script how to behave and where to find things. This includes:
    *   Names for specific sheets in Excel files (like 'Mes').
    *   Column names in the store directory file (Masterfile) for 'ATICA Code', 'Store Name' ('TIENDA'), and 'Establishment Code' ('EST').
    *   Starting column numbers for sales and purchase data (although these are not directly used in this script, they are defined in the configuration).
    *   Column names in the store performance reports ('PyG files') for 'concept', 'value' ('imeapu'), and a secondary code ('codigo_2').
    *   Column numbers in the 'Cash Margin' Excel files for 'ATICA Code', 'Section', 'Controlled Shrinkage', and 'Uncontrolled Shrinkage'.
*   **Setting File Locations:** The script defines the exact folder paths on your computer where it will find the input files and save the output files. It's like setting up addresses for different departments:
    *   `PYG_MES`:  Where the monthly store performance reports are stored.
    *   `MASTERFILES`: Where the store directory (Masterfile) is located.
    *   `MARGEN_CAJA`: Where the Excel files containing 'Cash Margin' data are located.
*   **Data Display Options:** It sets up how data will be displayed when the script runs, making it easier to read on the screen.
*   **Helper Functions:** It defines two small helper functions:
    *   `convert_euro_format(value)`: This function is like a currency converter. It takes numbers in European format (like '1.234,56€') and transforms them into a standard numerical format that the script can understand (like 1234.56).
    *   `get_target_month_names(current_month_number)`: This function generates a list of month names (in Spanish) from January up to the month before the current month. For example, if the current month is October, it will create a list of months from January to September. This list helps the script know which monthly Excel sheets to process.

### Section 2: Processing Cash Margin Excel Data
This section explains how the script reads and organizes the 'Cash Margin' data from the Excel files.

*   **Locating Excel Files:** The script first looks in the `MARGEN_CAJA` folder to find any Excel files (files ending with `.xlsx` or `.xls`). It checks if there are any Excel files at all in the folder.
*   **Opening the Excel File and Identifying Months:** It opens the first Excel file it finds. It then uses the `get_target_month_names` function to get a list of months it needs to process (e.g., January to September).
*   **Reading Data from Monthly Sheets:** The script goes through each sheet in the Excel file. It skips any sheet named 'Mes' (as it's likely a summary sheet). For the other sheets, it checks if the sheet name starts with a month name from the target month list (like "ENERO ", "FEBRERO ", etc.).
*   **Extracting Key Information:** For each monthly sheet it finds, the script extracts the following data:
    *   'ATICA Code' (store identifier)
    *   'Section' (product category within the store, e.g., 'Electronics', 'Clothing')
    *   'Controlled Shrinkage' value
    *   'Uncontrolled Shrinkage' value
    It knows exactly which columns in the Excel sheet contain this information based on the configuration settings.
*   **Cleaning and Preparing Data:** The script then cleans up the extracted data to ensure it's usable:
    *   It removes rows with missing or invalid 'ATICA Codes' or 'Sections'.
    *   It converts the 'Controlled Shrinkage' and 'Uncontrolled Shrinkage' values from European currency format to standard numbers using the `convert_euro_format` function.
*   **Combining Data from All Months:**  The script collects the cleaned data from all the monthly sheets and combines it into a single table.
*   **Aggregating Data:** It then groups this combined data by 'ATICA Code' and 'Section'. For each unique combination of store and section, it adds up the 'Controlled Shrinkage' and 'Uncontrolled Shrinkage' values from all the processed months to get total values for the period.
*   **Adding Store Details:**  The script reads the 'Masterfile' (store directory) which contains extra information about each store, like its 'Store Name' ('TIENDA') and 'Establishment Code' ('EST'). It then merges this store information with the aggregated shrinkage data using the 'ATICA Code' to link them together.
*   **Finalizing Data Table:** Finally, the script prepares the data table for output by:
    *   Ensuring 'Establishment Codes' are in a numerical format.
    *   Setting any missing shrinkage values to zero.
    *   Renaming the columns to be more descriptive (e.g., 'Código ATICA', 'Tienda', 'Sección', 'Demarca Controlada', 'Demarca Incontrolada').
    *   Formatting the shrinkage values to display with two decimal places.
*   **Saving Detailed Report:** The script saves this finalized data table as a CSV file named 'Margenes_Detalle_por_seccion.csv' in the `MARGEN_CAJA` folder. This file is a detailed breakdown of shrinkage by store and product section.
*   **Passing Data for PyG Update:** The script makes this processed data table available to be used in the next step, which is updating the store performance reports ('PyG files').

### Section 3: Updating PyG Files with Shrinkage Data
This section describes how the script takes the processed shrinkage data and updates the individual store performance reports.

*   **Finding PyG Files:** The script looks into the `PYG_MES` folder for all files ending with `.csv`. These are assumed to be the store performance reports.
*   **Identifying Store Code from Filename:** For each PyG file, the script tries to identify the store's 'Establishment Code' ('EST') from the filename. It expects the filename to contain a pattern like `_XXXX_` where `XXXX` is the four-digit store code.
*   **Matching Store Data:** Using the identified 'Establishment Code', the script searches for the corresponding store's data in the processed shrinkage data table (created in the previous section).
*   **Updating Shrinkage Values in PyG Files:** For each store and product section, the script performs the following updates in the store's PyG file:
    *   **Controlled Shrinkage Update:** It searches for a line in the PyG file where the 'concept' column matches a specific text like 'VARIACION EXISTENCIAS DEMARCA CONTROLADA' followed by the product section name (e.g., 'VARIACION EXISTENCIAS DEMARCA CONTROLADAElectronics'). If it finds a match, it updates the 'value' column ('imeapu') in that line with the 'Controlled Shrinkage' value from the processed data.
    *   **Uncontrolled Shrinkage Update:** It does a similar update for 'Uncontrolled Shrinkage'. It searches for a line where the 'concept' column matches text like 'VARIACION EXISTENCIAS DEMARCA INCONTROLADA' followed by the product section name, with an additional condition to exclude lines where 'codigo_2' starts with '61004' (this might be a specific category to exclude). If a match is found, it updates the 'value' column with the 'Uncontrolled Shrinkage' value.
*   **Saving Updated PyG Files:** After updating all relevant shrinkage values in a PyG file, the script saves the updated file, replacing the original file.
*   **Reporting Progress:** Throughout the PyG file update process, the script prints messages to the screen to show which files are being processed and which updates are being made. It also reports if certain 'concepts' (like 'VARIACION EXISTENCIAS DEMARCA CONTROLADA...') are not found in a PyG file.

### Section 4: Script Execution
This is the final part of the script that puts everything into action when you run it.

*   **Setting Current Month for Processing (and Testing):** The script determines the current month from your computer's date. It also includes a line specifically for testing purposes where it sets the current month to October (`current_month = 10`). This is useful for testing the script on past months' data.
*   **Running the Margin Data Processing:** It calls the `process_margen_caja` function to process the 'Cash Margin' data from the Excel files and generate the detailed shrinkage report.
*   **Displaying Processed Data:** If the margin data processing is successful, the script prints the processed data table (the detailed shrinkage report) to the screen.
*   **Running PyG File Updates:** It then calls the `update_pyg_files` function to update all the store performance reports ('PyG files') with the processed shrinkage data.
*   **Error Handling:** If any error occurs during the script's execution, it catches the error and displays an error message on the screen, helping to troubleshoot any problems.

## 3. Inputs Used

| Input Name | Type | Description | Constraints | Source |
|------------|------|-------------|-------------|------------------|
| **Cash Margin Excel File** | `.xlsx` or `.xls` file | Excel file containing monthly 'Cash Margin' data. This includes 'ATICA Code' (store ID), 'Section' (product category), 'Controlled Shrinkage', and 'Uncontrolled Shrinkage' values. Data is organized in separate sheets for each month (e.g., "ENERO ", "FEBRERO "). | File must be in `.xlsx` or `.xls` format. Sheet names should start with month names in Spanish (uppercase) followed by a space and two characters. Specific columns for 'ATICA Code', 'Section', 'Controlled Shrinkage', and 'Uncontrolled Shrinkage' are expected in each sheet, based on the script's configuration. | Located in the `DIR_MARGEN_CAJA` directory. |
| **Masterfile (Masterfile_CODIGOS.csv)** | `.csv` file | CSV file acting as a store directory. It contains information about each store, including 'ATICA Code', 'Store Name' ('TIENDA'), and 'Establishment Code' ('EST'). | Must be a CSV file and contain columns named 'ATICA', 'TIENDA', and 'EST'. 'EST' column should contain numerical store codes, and 'ATICA' column should contain store identifiers as text. | Located in the `DIR_MASTERFILE` directory. |
| **PyG Files (Monthly Performance Reports)** | `.csv` files | CSV files representing monthly performance reports for each store. The filenames are expected to include '_[Establishment Code]_' (a 4-digit number) to identify which store the report belongs to. | Must be CSV files. Each file is expected to have columns named 'concepto', 'imeapu' (for values), and 'codigo_2'. | Located in the `DIR_PYG_MES` directory. |

## 4. Outputs Generated

| Output Name | Type | Description | Conditions | Destination |
|-------------|------|-------------|------------|-----------------------|
| **Margenes_Detalle_por_seccion.csv** | `.csv` file | A CSV file that provides a detailed summary of 'Controlled Shrinkage' and 'Uncontrolled Shrinkage' for each store ('ATICA Code') and product section. It also includes store names ('Tienda') and 'Establishment Codes' ('Código EST'). | This file is generated every time the `process_margen_caja` function runs successfully. | Saved in the `DIR_MARGEN_CAJA` directory. |
| **Updated PyG Files** | `.csv` files | The original PyG files in the `DIR_PYG_MES` directory are modified. Specifically, the 'value' column ('imeapu') for rows related to 'Controlled Shrinkage' and 'Uncontrolled Shrinkage' (for each product section) are updated with the calculated shrinkage values from the processed data. | PyG files are updated if the script successfully processes the 'Cash Margin' Excel data and finds matching store codes and sections. | Overwrites the original files in the `DIR_PYG_MES` directory. |
| **Console Output (Progress and Information Messages)** | Text messages | Messages printed to the user's screen during the script's execution. These messages indicate the script's progress, any warnings, error messages, and confirmation of updates. The final processed 'Cash Margin' data table is also printed to the console. | Generated throughout the script execution to provide feedback and information about the process. | Displayed in the command-line interface or terminal where the script is run. |

## 5. Final Summary
In essence, this script is an automated assistant for managing and updating store shrinkage data.  Instead of manually sifting through monthly Excel reports and updating numerous store performance files, this script handles it all automatically. It takes in monthly Excel reports detailing shrinkage, organizes this data by store and product type, and then intelligently updates each store's performance report with the correct shrinkage figures. This automation saves significant time and effort, reduces the risk of manual data entry errors, and ensures that all store performance reports are consistently accurate and reflect the most recent shrinkage information.  The script also conveniently creates a detailed summary report of shrinkage, providing a clear and consolidated view of shrinkage across all stores and product sections, which is invaluable for financial analysis and decision-making.