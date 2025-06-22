import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker for synthetic data
fake = Faker()

def generate_appointments(start_date, rate, max_days=365):
    appointments = []
    current_date = start_date
    while True:
        delta = np.random.exponential(1 / rate)
        current_date += timedelta(days=delta)
        if (current_date - start_date).days > max_days:
            break
        appointments.append(current_date)
    return sorted(appointments)

def generate_patients(n_patients=1000):
    patients = []
    start_date = datetime(2024, 1, 1)
    reference_names = []
    states = ["CA", "NY", "TX"]
    visit_rates = [0.1, 0.01, 0.05]

    for i in range(n_patients):
        gender = random.choice(["M", "F"])
        state = random.choice(states)
        visit_rate = random.choice(visit_rates)
        
        first_name = fake.first_name()
        middle_name = fake.first_name() if random.random() < 0.5 else ""
        last_name = fake.last_name()
        original_name = f"{first_name} {middle_name} {last_name}".strip()
        
        #name = introduce_misspelling(original_name)
        name_formatted = f"{last_name}, {first_name} {middle_name}".strip()
        
        address1 = fake.street_address()
        address2 = f"Apt {random.randint(1, 100)}" if random.random() < 0.3 else ""
        address3 = ""
        
        city = fake.city()
        
        zip_code = fake.zipcode()
        
        address_formatted = f"{address1}{f' {address2}' if address2 else ''}, {city}, {state}, {zip_code}"
        
        age_min, age_max = random.choice([(20, 30), (40, 50), (60, 70)])
        dob = fake.date_of_birth(minimum_age=age_min, maximum_age=age_max)
        
        patient = {
            "id": i,
            "name": name_formatted,
            "original_name": original_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "address": address_formatted,
            "address1": address1,
            "address2": address2,
            "address3": address3,
            "city": city,
            "state": state,
            "zip": zip_code,
            "dob": dob,
            "gender": gender,
            "age": (datetime.now().date() - dob).days / 365.25,
            "appointments": generate_appointments(start_date, visit_rate)
        }

        patients.append(patient)
        reference_names.append(original_name)
    return patients, reference_names

def save_patients_to_excel(patients, filename="patients.xlsx"):
    df_data = []
    for p in patients:
        appt_str = ",".join([appt.strftime('%Y-%m-%d') for appt in p["appointments"]]) if p["appointments"] else "None"
        df_data.append({
            "name": p["name"],
            "address": p["address"],
            "appointments": appt_str
        })
    df = pd.DataFrame(df_data)
    df.to_excel(filename, index=False)
    print(f"Saved patient data to {filename}")

def load_patients_from_excel(filename="patients.xlsx"):
    from utils import parse_name, parse_address  # Import here to avoid circular dependency

    df = pd.read_excel(filename)

    patients = []
    reference_names = []
    states = ["CA", "NY", "TX"]
    
    for i, row in df.iterrows():
        name = row["name"]

       # print(f"Loading patient {i}: name = {name}")  # Debug

        first_name, middle_name, last_name = parse_name(name)
        original_name = f"{first_name} {middle_name} {last_name}".strip()

        address = row["address"]
        address1, address2, address3, city, state, zip_code = parse_address(address)
       
        appt_str = row["appointments"] if isinstance(row["appointments"], str) else ""
        appts = [datetime.strptime(date, '%Y-%m-%d') for date in appt_str.split(",") if date and date != "None"]
       
        gender = random.choice(["M", "F"])
        
        age_min, age_max = random.choice([(20, 30), (40, 50), (60, 70)])
        dob = fake.date_of_birth(minimum_age=age_min, maximum_age=age_max)
       
        patient = {
            "id": i,
            "name": name,
            "original_name": original_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "address": address,
            "address1": address1,
            "address2": address2,
            "address3": address3,
            "city": city,
            "state": state if state in states else random.choice(states),
            "zip": zip_code,
            "dob": dob,
            "gender": gender,
            "age": (datetime.now().date() - dob).days / 365.25,
            "appointments": appts
        }

        patients.append(patient)
        reference_names.append(original_name)

    return patients, reference_names