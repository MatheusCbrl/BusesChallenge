To install the App, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

## Usage
-----
To use the App, follow these steps:

1. Run the `app.py` file using the CLI. Execute the following command:
   ```
   run login.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Key Implementation Details:
Database Connection: Using SQLAlchemy for flexible and maintainable database connections.
Data Validation and Transformation: Ensuring correct data types for fields before insertion.
Avoiding Duplication: Catching IntegrityError for duplicate entries.
Bus Image Insertion: Associating image URLs with corresponding buses.
Next Steps and SQL Script for Testing
To preload or test sample data:

Create and initialize the database using your provided schema.
Use SQL scripts to insert initial dummy data for development and testing.
If you need assistance creating SQL scripts or further optimizations for data handling, just let me know!



## License
-------
released under the [MIT License](https://opensource.org/licenses/MIT).
