
# Documentation for Data Extraction and Transformation Script

## 1. Brief Explanation of the Code

This script takes accounting data from several database files, processes it, and creates separate, organized data files.  It's like taking information from many messy notebooks, cleaning it up, summarizing it, and putting the key facts into neatly labeled folders.  The script specifically works with accounting data related to franchises, extracting details for each store and saving them in a standard format. It solves the problem of having scattered and inconsistent accounting data by consolidating and standardizing it.

## 2. Detailed Breakdown of Each Part of the Code

### Section 1: Setting Up the Workspace

This part tells the script where to find the input data files, where to store temporary files, and where to put the final, cleaned-up data files. It's like setting up your desk before you start working: making sure you know where everything is and where you'll put things when you're done. It also defines names of important folders and files.

### Section 2: Cleaning Store Names

This section defines a small task to clean up the store names.  Sometimes, store names have extra numbers or commas at the end, which can be messy. This part removes those extra characters, ensuring the store names are consistent.

### Section 3: Getting Franchisee Code and Year

This section defines another small task to get two important pieces of information from the input file names: the franchisee code (a short code identifying the franchise owner) and the year the data is from. It is similar to look at the cover of a notebook that holds the year and the author.

### Section 4: Extracting Data from the Database

This section defines a task to pull a specific table of data out of each input database file. Think of it like copying a specific page from each notebook. It checks if the page exists before copying it, to avoid errors.

### Section 5: Checking and Correcting Department Codes

This section defines a task to check and potentially fix a specific code called "DEPAPU".  If there's only one main DEPAPU value (other than zero), it makes sure all the zero values are replaced with that main value. It's like ensuring all entries in a column use the same consistent code.

### Section 6: Processing Each Database File

This is the main part where the script does most of its work. It combines all the previous smaller tasks. For each input database file:

1.  **Gets Information:** It figures out the franchisee code and year from the file name.
2.  **Pulls Data:** It extracts the main accounting table from the database.
3.  **Cleans Up:** It checks and corrects the "DEPAPU" codes.
4.  **Filters Data:** It focuses only on the data for the most recent year and a specific account code (4770000), then figures out the most recent month. It removes the not needed information.
5.  **Prepares Data for Output:** It selects only the necessary columns, adds columns for the month, year, and franchisee code.
6.  **Filters and Organizes:** It removes any remaining entries where "DEPAPU" is zero and organizes the data.
7.  **Summarizes:** It groups the data by several categories (like account code, department, year, month, and franchisee) and calculates the total value for each group.
8. **Corrects values:** Changes some values in the summary based on starting number and a code.
9.  **Adds More Information:** It uses a separate "Masterfile" (like a reference guide) to add extra details about each department, such as the store name, city, and other codes.
10. **Creates Output Files:** It saves the final, cleaned-up data into several CSV files. It creates a separate file for each store, named using the store name, department code, year, and month.

### Section 7: Running Everything

This section is the "main switch" of the script. It tells the script to go through each database file in the input folder and run the processing steps (defined in Section 6) on each one. It also measures how long the entire process takes.

## 3. Inputs Used

| Input Name            | Type     | Description                                                                       | Constraints                                                                                    | Source                                            |
| --------------------- | -------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Accounting Databases | File     | Database files containing the raw accounting data.                               | Must be in `.accdb` format and located in the `POC/SUMAS_Y_SALDOS/` folder. Each represents a different accounting period. | Input folder (`POC/SUMAS_Y_SALDOS/`)            |
| Masterfile_CODIGOS    | File     | A CSV file containing extra information about departments (stores, etc.).     | Must be a CSV file named `Masterfile_CODIGOS.csv` located in `POC/MASTERFILES/`. Contains reference data.       | `POC/MASTERFILES/` folder                       |

## 4. Outputs Generated

| Output Name                   | Type | Description                                                                  | Conditions                                                                                                   | Destination                                     |
| ----------------------------- | ---- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| Intermediate CSV Files         | File | Temporary CSV files containing data extracted and partially processed.      | One file is created for each input database, named based on the input file and the most recent month.    | `POC/SUMAS_Y_SALDOS/INTERMEDIATE/` folder      |
| Final CSV Files               | File | CSV files containing the final, cleaned, and summarized accounting data. | One file is created for each store and department, named using the store name, department code, year, and month. | `POC/SUMAS_Y_SALDOS/FINAL_RESULT/` folder   |

## 5. Final Summary

This script is a tool for automatically cleaning, organizing, and summarizing accounting data from multiple database files. It takes raw, messy data and transforms it into a set of clear, well-organized files, one for each store, making it much easier to analyze and understand the financial information. The script helps users by automating a tedious manual process, saving time and reducing the risk of errors. It provides a consistent and reliable way to extract key accounting insights.

