
import pandas as pd

df = pd.read_csv("healthcare_data_analysis/diabetic_data.csv")

print(df.head())
print(df.shape)
print(df.columns.to_list())

df.info()

print((df =="?").sum())
print(df.duplicated().sum())



missing = (df =="?").sum()
print(missing[missing > 0])
missing_percent = (missing/len(df)*100)
print(missing_percent[missing_percent>0])

print(df["readmitted"].value_counts())
print("unique patients: ",df["patient_nbr"].nunique())

unique_counts = df.nunique()
print(unique_counts.sort_values(ascending=False))

constant_columns = unique_counts[unique_counts==1]
print("constant_columns: ",constant_columns)

df = df.drop(columns=["weight"])
df["medical_specialty"] = df["medical_specialty"].replace("?", pd.NA)
df["medical_specialty"] = df["medical_specialty"].fillna("Unknown")

df = df.drop(columns=["payer_code"])

df["race"] = df["race"].fillna("Unknown")
df[["diag_1","diag_2","diag_3"]] = df[["diag_1","diag_2","diag_3"]].fillna("Unknown")
df=df.drop(columns=["examide","citoglipton"])

print(df.shape)
print(df.isna().sum()[df.isna().sum()>0])

df["max_glu_serum"] = df["max_glu_serum"].fillna("None")
df["A1Cresult"] = df["A1Cresult"].fillna("None")
print(df.isna().sum()[df.isna().sum()>0])

print(df["readmitted"].value_counts())
print(df['readmitted'].value_counts(normalize=True)*100)

print("Total encounters:", len(df))
print("Unique patients:", df["patient_nbr"].nunique())
print("Average encounters per patient:", df.groupby("patient_nbr").size().mean())
print("Max encounters for one patient:", df.groupby("patient_nbr").size().max())

encounters_per_patient = df.groupby("patient_nbr").size().reset_index(name="encounters")

print(encounters_per_patient.head())
print(encounters_per_patient["encounters"].describe()) 

repeat_patients = encounters_per_patient[encounters_per_patient["encounters"] > 1]
print("Repeat patients:", len(repeat_patients))
repeat_rate = len(repeat_patients) / df["patient_nbr"].nunique() * 100
print("Repeat rate:", round(repeat_rate, 2), "%")

patient_readmission = (
    df.groupby("patient_nbr")["readmitted"]
    .apply(lambda x: (x == "<30").sum())
    .reset_index(name="readmitted_30_days")
)

print(patient_readmission.head())
print(patient_readmission["readmitted_30_days"].value_counts().head())

patients_with_most_encounters = (
    df.groupby("patient_nbr")
    .size()
    .sort_values(ascending=False)
    .head(10)
)
print(patients_with_most_encounters)

encounters_distribution = df.groupby("patient_nbr").size().value_counts().sort_index()
print(encounters_distribution)

age_distribution = df["age"].value_counts().sort_index()
print(age_distribution)

gender_distribution = df["gender"].value_counts()
print(gender_distribution)

race_distribution = df["race"].value_counts()
print(race_distribution)
df["race"] = df["race"].replace("?", "Unknown")
race_distribution = df["race"].value_counts()
print(race_distribution)

age_gender_distribution = pd.crosstab(df["age"], df["gender"])
print(age_gender_distribution)

hospital_utilization = df["time_in_hospital"].describe()
print(hospital_utilization)

inpatient_distribution = df["number_inpatient"].value_counts().sort_index()
print(inpatient_distribution)

outpatient_distribution = df["number_outpatient"].value_counts().sort_index()
print(outpatient_distribution)

emergency_distribution = df["number_emergency"].value_counts().sort_index()
print(emergency_distribution)

utilization_averages = df[["number_inpatient", "number_outpatient", "number_emergency"]].mean()
print(utilization_averages)

top_diagnoses = df["diag_1"].value_counts().head(10)
print(top_diagnoses)

df["diag_1_numeric"] = pd.to_numeric(df["diag_1"], errors="coerce")

def diagnosis_category(code):
    if pd.isna(code):
        return "Unknown"
    elif 390 <= code <= 459 or code ==785:
        return "Circulatory"
    elif 460 <= code <= 519:
        return "Respiratory"
    elif 520 <= code <= 579:
        return "Digestive"
    elif 250 <= code <= 251:
        return "Diabetes"
    elif 800 <= code <= 999:
        return "Injury"
    elif 710 <= code <= 739:
        return "Musculoskeletal"
    elif 580 <= code <= 589:
        return "Kidney"
    else:
        return "Other"

df["diagnosis_category"] = df["diag_1_numeric"].apply(diagnosis_category)
diagnosis_distribution = df["diagnosis_category"].value_counts()
print(diagnosis_distribution)

insulin_distribution = df["insulin"].value_counts()
print(insulin_distribution)
medication_changes_distribution = df["change"].value_counts()
print(medication_changes_distribution)
medication_count_distribution = df["num_medications"]
print(medication_count_distribution.describe())

medication_change__readmission = pd.crosstab(df["change"], df["readmitted"])
print(medication_change__readmission)
medication_change__readmission_percent = pd.crosstab(df["change"], df["readmitted"], normalize='index') *100
print(medication_change__readmission_percent)

medication_readmission = df.groupby("readmitted")["num_medications"].mean()
print(medication_readmission)

diagnosis_readmission = pd.crosstab(df["diagnosis_category"], df["readmitted"], normalize="index") * 100
print(diagnosis_readmission)

age_readmission = pd.crosstab(df["age"], df["readmitted"], normalize="index") * 100
print(age_readmission)
length_of_stay_readmission = df.groupby("readmitted")["time_in_hospital"].mean()
print(length_of_stay_readmission)

prior_utilization_readmission = df.groupby("readmitted")[["number_inpatient", "number_outpatient", "number_emergency"]].mean()
print(prior_utilization_readmission)

df["readmit_30"] =(df["readmitted"] == "<30").astype(int)
print(df[["readmit_30", "readmitted"]].head())

df["total_prior_visits"] = df["number_inpatient"] + df["number_outpatient"] + df["number_emergency"]
print(df[["total_prior_visits", "number_inpatient", "number_outpatient", "number_emergency"]].head())

df["medication_changed"] = (df["change"] == "Ch").astype(int)
print(df[["medication_changed", "change"]].head())

df["high_prior_utilization"] = (df["total_prior_visits"] > 3).astype(int)
print(df[["high_prior_utilization", "total_prior_visits"]].head())

df.to_csv("healthcare_data_cleaned.csv", index=False)
print("Cleaned data saved to healthcare_data_cleaned")
