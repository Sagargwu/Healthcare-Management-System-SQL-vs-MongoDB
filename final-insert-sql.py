import mysql.connector
import csv

# Connect to the MySQL database
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="healthcare_db"
)
mysql_cursor = mysql_connection.cursor()

# Insert Patients Data from CSV to SQL
with open('patients_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert empty strings to None
        row['contact_number'] = row['contact_number'] if row['contact_number'] else None
        row['email'] = row['email'] if row['email'] else None
        row['age'] = int(row['age'])  # Ensure age is an integer

        # Insert into SQL
        mysql_cursor.execute("""
            INSERT INTO Patients (patient_id, name, age, contact_number, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (int(row['patient_id']), row['name'], row['age'], row['contact_number'], row['email']))

# Commit the SQL changes for Patients
mysql_connection.commit()

# Insert Appointments Data from CSV to SQL
with open('appointments_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert is_follow_up directly to an integer
        is_follow_up = int(row['is_follow_up'])  # Read the value directly as 0 or 1

        # Convert empty strings to None for symptoms
        row['symptom1'] = row['symptom1'] if row['symptom1'] else None
        row['symptom2'] = row['symptom2'] if row['symptom2'] else None

        # Convert dose day values to integers
        dose_schedule = [int(row[f'dose_day_{i}']) for i in range(1, 8)]

        # Insert into SQL
        mysql_cursor.execute("""
            INSERT INTO Appointments (
                patient_id, date, is_follow_up, symptom1, symptom2, medication_name, dosage, frequency,
                dose_day_1, dose_day_2, dose_day_3, dose_day_4, dose_day_5, dose_day_6, dose_day_7
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row['patient_id']),
            row['date'],
            is_follow_up,  # This will be 0 or 1 as read directly from the CSV
            row['symptom1'],  # Set as None if no symptom is provided
            row['symptom2'],  # Set as None if no symptom is provided
            row['medication_name'],
            row['dosage'],
            row['frequency'],
            dose_schedule[0],
            dose_schedule[1],
            dose_schedule[2],
            dose_schedule[3],
            dose_schedule[4],
            dose_schedule[5],
            dose_schedule[6]
        ))

# Commit the SQL changes for Appointments
mysql_connection.commit()

# Close the connections
mysql_cursor.close()
mysql_connection.close()
