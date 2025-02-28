# Documentation for Sales and Purchases Calculation and PyG Update Script

## 1. Brief Explanation of the Code
This script is designed to automatically calculate monthly Gross Sales and Merchandise Purchases for different stores and update their monthly performance reports. Imagine you need to keep track of how much each store is selling and buying every month. This script takes sales and purchase data from Excel files, summarizes it for each store up to the previous month, and then automatically updates monthly performance reports (called 'PyG files') with these calculated figures. This saves time and ensures that the store performance reports are always current with the latest sales and purchase information.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Script Setup and Configuration
This part is like setting up the script with all the necessary instructions and locations it needs to work correctly.

*   **Importing Tools:**  The script starts by bringing in special tools (libraries) that help it work with spreadsheets (like Excel files), manage data in tables, handle dates and times, and find text patterns.
*   **Defining Names and Locations:** It then sets up names for important things like sheet names in Excel files (e.g., 'VTATOTAL' for sales sheet, 'COMPRAS' for purchases sheet), column names in different files (like 'CECO Code', 'ATICA Code', 'Store Code'), and the starting points of data columns in Excel files. Think of it as labeling all the tools and parts you'll use.
*   **File Paths:** It also specifies the exact locations of the folders on your computer where the script will find the input files (like Excel files with sales and purchase data, and store information) and where the output files (updated store reports) are located. Think of it as setting the addresses for all the documents the script needs to access. These folders are:
    *   `VENTAS_BRUTAS` (Gross Sales): Folder for Excel files containing gross sales data.
    *   `COMPRAS_MERCANCIAS` (Merchandise Purchases): Folder for Excel files containing merchandise purchases data.
    *   `PYG_MES` (Monthly P&L - Profit and Loss): Folder for monthly store performance reports (PyG files).
    *   `MASTERFILES`: Folder containing the store directory (Masterfile).
*   **Setting Display Options:**  It configures how data will be shown when the script runs, making it easier for someone using the script to read and understand the information.
*   **Determining Previous Month:** The script figures out what the previous month and year are. For example, if the script is run in October 2024, it determines that the previous month is September 2024. This is important because the script calculates sales and purchases up to the *previous* month. There's also a section to manually set the previous month and year for testing purposes.

### Section 2: Processing Sales Data (process_ventas_brutas Function)
This part focuses on reading and calculating Gross Sales from Excel files.

*   **Finding Sales Excel Files:** It looks inside the `VENTAS_BRUTAS` folder and finds any Excel files (files ending in `.xlsx` or `.xls`). It checks if there are any Excel files at all and stops if it can't find any.
*   **Opening and Reading Sales Data:** It opens the first Excel file it finds and reads the sheet named 'VTATOTAL' (or as configured).
*   **Cleaning Up the Data:** It removes any completely empty rows from the data. It then uses the first row of the sheet as the column names and removes the first row itself (as it's now used as headers).
*   **Calculating Total Sales per Store (CECO):** The script goes through each row of the sales data. For each row, it tries to identify the store code (called 'CECO Code'). It then adds up the sales figures from January up to the *previous* month for that store.  It knows which columns represent each month's sales based on the configuration. If a sales figure is missing or not in the correct number format, it ignores it and continues.
*   **Storing Sales Totals:** The script keeps a record of the total sales calculated for each store code.
*   **Creating Sales Summary Table:** Finally, it creates a table that lists each store code and its total calculated Gross Sales up to the previous month. It also ensures that if a store has zero sales, it's marked as 'not available' (NA) in the table.

### Section 3: Processing Purchases Data (process_compras Function)
This part is similar to the sales processing, but it focuses on reading and calculating Merchandise Purchases.

*   **Finding Purchase Excel Files:** It looks inside the `COMPRAS_MERCANCIAS` folder and finds Excel files.
*   **Opening and Reading Purchase Data:** It opens the first Excel file and reads the sheet named 'COMPRAS' (or as configured).
*   **Cleaning Up the Data:** Similar to sales data, it removes empty rows and sets the column names from the first row.
*   **Calculating Total Purchases per Store (CECO):**  It goes through each row, identifies the store code ('CECO Code'), and adds up the purchase figures from January up to the *previous* month. It handles missing or incorrectly formatted purchase figures similarly to sales data.
*   **Storing Purchase Totals:** It records the total purchases for each store code.
*   **Creating Purchase Summary Table:** It creates a table listing each store code and its total calculated Merchandise Purchases up to the previous month. Zero purchase values are also marked as 'not available' (NA).

### Section 4: Loading Store Information (process_masterfile Function)
This section explains how the script loads store details from the 'Masterfile'.

*   **Finding and Reading Masterfile:** It looks for the 'Masterfile_CODIGOS.csv' file in the `MASTERFILES` folder and reads it. This file is like a directory of all stores.
*   **Extracting Store Information:** From the Masterfile, it extracts three important pieces of information for each store: 'ATICA Code', 'Store Name' ('TIENDA'), and 'Establishment Code' ('EST').
*   **Providing Store Information:** The script makes this store information available for later use, to link sales and purchase data to specific stores.

### Section 5: Merging Data and Saving to CSV (save_merged_dataframe_to_csv Function)
This section describes how the script combines sales, purchases, and store information and saves it to a file.

*   **Merging Sales and Store Information:** It combines the sales summary table with the store information from the Masterfile, using the store code ('CECO Code' in sales data and 'ATICA Code' in Masterfile) as a link. This step connects the sales figures to the correct store details.
*   **Merging Purchases and Store Information:** It does a similar merging process for the purchase summary table and the store information.
*   **Combining Sales and Purchases Data:** It then combines the merged sales data and merged purchase data, using the 'Establishment Code' ('EST') as a link. This puts sales and purchase figures for each store together in one table.
*   **Adding Store Name:**  It adds the 'Store Name' ('TIENDA') to the combined table for better readability.
*   **Cleaning and Ordering the Final Table:** It organizes the columns in the final table to be 'Establishment Code', 'Gross Sales', 'Merchandise Purchases', and 'Store Name'. It also rounds the sales and purchase figures to two decimal places.
*   **Saving to CSV File:** Finally, it saves this combined table to a CSV file named 'Ventas_y_Compras_[previous month number]_[previous year].csv' in the `PYG_MES` folder. This file acts as a summary report of calculated sales and purchases for all stores.

### Section 6: Updating PyG Files (process_pyg_files Function)
This section explains how the script updates the individual store performance reports ('PyG files').

*   **Going through Store List:** The script goes through each row in the combined sales and purchases table (created in the previous step).
*   **Identifying PyG File for Each Store:** For each store, it tries to find the corresponding 'PyG file' in the `PYG_MES` folder. It looks for a filename that matches a specific pattern containing the store's 'Establishment Code' ('EST'), previous month, and previous year.
*   **Reading PyG File Data:** If it finds a matching PyG file, it reads the data from that file into a table.
*   **Updating Sales Value in PyG File:** It searches for a line in the PyG file where the 'concept' is 'VENTA BRUTA (SIN CONCESIONES)' (Gross Sales (Without Concessions)). If found, it updates the 'value' column ('imeapu') in that line with the calculated Gross Sales figure from the combined table. If the concept is not found, it notes that it's missing.
*   **Updating Purchases Value in PyG File:** It does a similar process for Merchandise Purchases. It searches for a line where the 'concept' is 'COMPRAS' (Purchases) and updates the 'value' column with the calculated Merchandise Purchases figure. If the concept is not found, it notes that.
*   **Saving Updated PyG File:** After updating the sales and purchase values, it saves the updated PyG file, overwriting the original file.
*   **Reporting Progress:**  Throughout the process, it prints messages to the screen indicating which files are being processed and updated, and if any concepts are not found in the PyG files.

### Section 7: Main Script Execution
This is the part that runs when you execute the script and puts all the pieces together.

*   **Setting Previous Month and Year:** It determines the previous month and year (or uses the manual setting for testing).
*   **Processing Sales, Purchases, and Masterfile:** It calls the `process_ventas_brutas`, `process_compras`, and `process_masterfile` functions to read and process the data.
*   **Merging and Saving Data:** It then merges the processed data, saves it to a CSV file using `save_merged_dataframe_to_csv`, and prints the combined data table to the screen.
*   **Updating PyG Files:** Finally, it calls the `process_pyg_files` function to update the store performance reports with the calculated sales and purchases figures.
*   **Error Handling:** If any error occurs during the script's execution, it catches the error and prints an error message to the screen.

## 3. Inputs Used

| Input Name | Type | Description | Constraints | Source |
|------------|------|-------------|-------------|------------------|
| **Sales Excel File** | `.xlsx` or `.xls` file | Excel file containing monthly Gross Sales data for each store (identified by CECO code).  Data for each month is in separate columns. | File should be in `.xlsx` or `.xls` format. Must contain a sheet named 'VTATOTAL' (or as configured). Sales data for each month should be in columns starting from a specified index (configured in the script). | Located in the `DIR_VENTAS_BRUTAS` directory. |
| **Purchases Excel File** | `.xlsx` or `.xls` file | Excel file containing monthly Merchandise Purchases data for each store (identified by CECO code). Data for each month is in separate columns. | File should be in `.xlsx` or `.xls` format. Must contain a sheet named 'COMPRAS' (or as configured). Purchase data for each month should be in columns starting from a specified index (configured in the script). | Located in the `DIR_COMPRAS_MERCANCIAS` directory. |
| **Masterfile (Masterfile_CODIGOS.csv)** | `.csv` file | CSV file containing store information, including 'ATICA Code', 'Store Name' ('TIENDA'), and 'Establishment Code' ('EST'). | Must be a CSV file and contain columns named 'ATICA', 'TIENDA', and 'EST'. | Located in the `DIR_MASTERFILE` directory. |
| **PyG Files (Monthly Performance Reports)** | `.csv` files | CSV files representing monthly performance reports for each store. Filenames are expected to follow a pattern that includes the store's 'Establishment Code' ('EST'), month, and year. | Must be CSV files. Each file is expected to have columns named 'concepto' and 'imeapu'. Filenames should match a specific pattern to be correctly identified for each store and month. | Located in the `DIR_PYG_MES` directory. |

## 4. Outputs Generated

| Output Name | Type | Description | Conditions | Destination |
|-------------|------|-------------|------------|-----------------------|
| **Ventas_y_Compras_[MM]_[YYYY].csv** | `.csv` file | A CSV file summarizing the calculated Gross Sales and Merchandise Purchases for each store ('Establishment Code' - EST) for the period up to the previous month ([MM] and [YYYY] represent the previous month and year). Includes 'Store Name' ('TIENDA'). | Generated every time the script is run successfully and combines sales and purchase data. | Saved in the `DIR_PYG_MES` directory. |
| **Updated PyG Files** | `.csv` files | The original PyG files in the `DIR_PYG_MES` directory are modified. The 'imeapu' value for the 'VENTA BRUTA (SIN CONCESIONES)' and 'COMPRAS' concepts are updated with the calculated sales and purchases figures for each corresponding store. | Updated for each PyG file for which a matching store and the relevant concepts are found. | Overwrites the original files in the `DIR_PYG_MES` directory. |
| **Console Output (Information Messages)** | Text messages | Messages printed to the console during script execution, indicating progress, warnings, errors, and the final consolidated data table. | Generated during script execution to provide feedback on the process. | Displayed on the user's screen when running the script. |

## 5. Final Summary
This script automates the process of calculating and updating key financial figures – Gross Sales and Merchandise Purchases – for your stores.  Instead of manually collecting data from Excel files, calculating totals, and then updating individual store performance reports, this script does it all for you. It reads sales and purchase data, does the necessary calculations up to the previous month, combines this with store information, and then automatically updates the relevant figures in each store's monthly performance report. This not only saves a significant amount of manual work but also ensures that your store performance reports are accurate and consistently updated with the latest sales and purchase information, giving you a reliable and timely view of your stores' financial performance.