from pymongo import MongoClient
import csv

# Connect to MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['healthcare_db']
patients_collection = mongo_db['Patients']
appointments_collection = mongo_db['Appointments']

# Insert Patients Data from CSV to MongoDB
patients_data = []
with open('patients_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert empty strings to None
        row['contact_number'] = row['contact_number'] if row['contact_number'] else None
        row['email'] = row['email'] if row['email'] else None
        row['age'] = int(row['age'])  # Ensure age is an integer

        # Append to patients data for MongoDB
        patients_data.append({
            "_id": int(row['patient_id']),  # Use "_id" as MongoDB identifier
            "name": row['name'],
            "age": row['age'],
            "contact_number": row['contact_number'],
            "email": row['email']
        })

# Insert Patients Data into MongoDB
if patients_data:  # Check to ensure there's data to insert
    patients_collection.insert_many(patients_data)

# Insert Appointments Data from CSV to MongoDB
appointments_data = []
with open('appointments_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Convert is_follow_up from '0'/'1' to boolean
        is_follow_up = True if row['is_follow_up'] == '1' else False

        # Convert empty strings to None for symptoms
        row['symptom1'] = row['symptom1'] if row['symptom1'] else None
        row['symptom2'] = row['symptom2'] if row['symptom2'] else None

        # Convert dose day values to integers
        dose_schedule = [int(row[f'dose_day_{i}']) for i in range(1, 8)]

        # Handle symptoms: If no symptoms at all, set to an empty list
        symptoms = []
        if row['symptom1']:
            symptoms.append(row['symptom1'])
        if row['symptom2']:
            symptoms.append(row['symptom2'])

        # Append to appointments data for MongoDB
        appointments_data.append({
            "_id": int(row['appointment_id']),
            "patient_id": int(row['patient_id']),
            "date": row['date'],
            "is_follow_up": is_follow_up,
            "symptoms": symptoms if symptoms else None,  # Set as None if no symptoms provided
            "treatment_details": {
                "medication_name": row['medication_name'],
                "dosage": row['dosage'],
                "frequency": row['frequency'],
                "dose_schedule": dose_schedule
            }
        })

# Insert Appointments Data into MongoDB
if appointments_data:  # Check to ensure there's data to insert
    appointments_collection.insert_many(appointments_data)

# Close the MongoDB connection
mongo_client.close()
