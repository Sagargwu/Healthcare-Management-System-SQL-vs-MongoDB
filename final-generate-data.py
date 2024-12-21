import csv
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# List of common symptoms
symptoms_list = [
    "fever", "cough", "headache", "fatigue", "sore throat",
    "shortness of breath", "nausea", "vomiting", "diarrhea",
    "dizziness", "chills", "muscle pain", "joint pain", "rash",
    "congestion", "runny nose", "loss of smell", "loss of taste"
]

# List of real medicine names
medicines_list = [
    "Ibuprofen", "Paracetamol", "Amoxicillin", "Aspirin", "Metformin",
    "Lisinopril", "Atorvastatin", "Simvastatin", "Omeprazole", "Albuterol",
    "Prednisone", "Ciprofloxacin", "Metoprolol", "Furosemide", "Hydrochlorothiazide"
]

# List of common email domains
email_domains = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com"
]

# Generate and Store Patients Data to CSV
patients_data = []
for patient_id in range(1, 100001):
    # Randomly decide if a patient will have an email or contact number (or both)
    has_contact_number = random.choice([True, False])
    has_email = random.choice([True, False])

    contact_number = fake.numerify('##########') if has_contact_number else None

    # Generate email based on patient's name if needed
    name = fake.name()
    email = None
    if has_email:
        # Format the name to create a valid email address
        name_parts = name.split()
        first_name = name_parts[0].lower()
        last_name = name_parts[-1].lower() if len(name_parts) > 1 else ""
        email = f"{first_name}.{last_name}@{random.choice(email_domains)}"

    patient = {
        "patient_id": patient_id,
        "name": name,
        "age": random.randint(1, 100),
        "contact_number": contact_number,
        "email": email
    }
    patients_data.append(patient)

# Save Patients Data to CSV with specified column names
with open('patients_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Header row as per your requirement
    writer.writerow(['patient_id', 'name', 'age', 'contact_number', 'email'])
    for patient in patients_data:
        writer.writerow([patient['patient_id'], patient['name'], patient['age'], patient['contact_number'], patient['email']])

# Generate and Store Appointments Data to CSV
appointments_data = []
for appointment_id in range(1, 100001):
    patient_id = random.randint(1, 100000)  # Assuming 100,000 patients exist
    num_symptoms = random.choice([0, 1, 2])  # Randomly choose if the patient has no symptoms, one, or two symptoms

    symptoms = []
    symptom1 = None
    symptom2 = None

    # Generate symptoms based on the number of symptoms decided
    if num_symptoms >= 1:
        symptom1 = random.choice(symptoms_list)
        symptoms.append(symptom1)
    if num_symptoms == 2:
        symptom2 = random.choice(symptoms_list)
        while symptom1 == symptom2:
            symptom2 = random.choice(symptoms_list)
        symptoms.append(symptom2)

    # Generate dose schedule with values from 0 to 3
    dose_schedule = [random.randint(0, 3) for _ in range(7)]  # Random doses for 7 days, between 0 and 3

    # Randomly decide if the appointment is a follow-up or not
    is_follow_up = random.choice([True, False])

    appointment = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "date": fake.date_this_decade().isoformat(),
        "is_follow_up": is_follow_up,
        "symptoms": symptoms,
        "medication_name": random.choice(medicines_list),
        "dosage": random.choice(["10mg", "20mg", "30mg", "500mg", "1g"]),
        "frequency": random.choice(["Once a day", "Twice a day", "Three times a day"]),
        "dose_schedule": dose_schedule
    }
    appointments_data.append(appointment)

# Save Appointments Data to CSV with specified column names
with open('appointments_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Header row as per your requirement
    writer.writerow([
        'appointment_id', 'patient_id', 'date', 'is_follow_up', 'symptom1', 'symptom2',
        'medication_name', 'dosage', 'frequency', 'dose_day_1', 'dose_day_2', 'dose_day_3',
        'dose_day_4', 'dose_day_5', 'dose_day_6', 'dose_day_7'
    ])
    for appointment in appointments_data:
        writer.writerow([
            appointment['appointment_id'],
            appointment['patient_id'],
            appointment['date'],
            1 if appointment['is_follow_up'] else 0,  # Convert boolean to 1/0
            appointment['symptoms'][0] if len(appointment['symptoms']) > 0 else None,  # If no symptom, set to None
            appointment['symptoms'][1] if len(appointment['symptoms']) > 1 else None,  # If no second symptom, set to None
            appointment['medication_name'],
            appointment['dosage'],
            appointment['frequency'],
            appointment['dose_schedule'][0],
            appointment['dose_schedule'][1],
            appointment['dose_schedule'][2],
            appointment['dose_schedule'][3],
            appointment['dose_schedule'][4],
            appointment['dose_schedule'][5],
            appointment['dose_schedule'][6]
        ])
