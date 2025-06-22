import os
from data_utils import load_patients_from_excel, generate_patients, save_patients_to_excel


def main():
    excel_file = "patients.xlsx"
    i = 1
    # Load or generate patient data
    if os.path.exists(excel_file):
        print(f"Loading patient data from {excel_file}")
        patients, reference_names = load_patients_from_excel(excel_file)
        
        #Debug
        for patient in patients:
            print(f"Loading patient {i}: name = {patient['name']}")
            i+=1
    else:
        print("Generating new patient data")
        patients, reference_names = generate_patients()
        save_patients_to_excel(patients, excel_file)
        load_patients_from_excel(excel_file)
        
        i = 1
        for patient in patients:
            print(f"Loading patient {i}: name = {patient['name']}")  # Debug
            i+=1

if __name__ == "__main__":
    main()