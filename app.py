import pandas as pd
import streamlit as st
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('xgb_model.pkl', 'rb'))

# Title
st.title("Academic Success Predictor")

# Define the mappings for each feature
application_mode_options = {
    '1st phase - general contingent': 1,
    'Ordinance No. 612/93': 2,
    '1st phase - special contingent (Azores Island)': 5,
    'Holders of other higher courses': 7,
    'Ordinance No. 854-B/99': 10,
    'International student (bachelor)': 15,
    '1st phase - special contingent (Madeira Island)': 16,
    '2nd phase - general contingent': 17,
    '3rd phase - general contingent': 18,
    'Ordinance No. 533-A/99, item b2) (Different Plan)': 26,
    'Ordinance No. 533-A/99, item b3 (Other Institution)': 27,
    'Over 23 years old': 39,
    'Transfer': 42,
    'Change of course': 43,
    'Technological specialization diploma holders': 44,
    'Change of institution/course': 51,
    'Short cycle diploma holders': 53,
    'Change of institution/course (International)': 57,
}

application_order_options = {
    'first choice': 0,
    'second choice': 1,
    'third choice': 2,
    'fourth choice': 3,
    'fifth choice': 4,
    'sixth choice': 5,
    'seventh choice': 6,
    'eighth choice': 7,
    'ninth choice': 8,
    'last choice': 9,
}
course_options = {
    'Biofuel Production Technologies': 33,
    'Animation and Multimedia Design': 171,
    'Social Service (evening attendance)': 8014,
    'Agronomy': 9003,
    'Communication Design': 9070,
    'Veterinary Nursing': 9085,
    'Informatics Engineering': 9119,
    'Equinculture': 9130,
    'Management': 9147,
    'Social Service': 9238,
    'Tourism': 9254,
    'Nursing': 9500,
    'Oral Hygiene': 9556,
    'Advertising and Marketing Management': 9670,
    'Journalism and Communication': 9773,
    'Basic Education': 9853,
    'Management (evening attendance)': 9991,
}

mother_qualification_options = {
    'Secondary Education - 12th Year of Schooling or Eq.': 1,
    'Higher Education - Bachelor\'s Degree': 2,
    'Higher Education - Degree': 3,
    'Higher Education - Master\'s': 4,
    'Higher Education - Doctorate': 5,
    'Frequency of Higher Education': 6,
    '12th Year of Schooling - Not Completed': 9,
    '11th Year of Schooling - Not Completed': 10,
    '7th Year (Old)': 11,
    'Other - 11th Year of Schooling': 12,
    '10th Year of Schooling': 14,
    'General commerce course': 18,
    'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.': 19,
    'Technical-professional course': 22,
    '7th year of schooling': 26,
    '2nd cycle of the general high school course': 27,
    '9th Year of Schooling - Not Completed': 29,
    '8th year of schooling': 30,
    'Unknown': 34,
    'Can\'t read or write': 35,
    'Can read without having a 4th year of schooling': 36,
    'Basic education 1st cycle (4th/5th year) or equiv.': 37,
    'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.': 38,
    'Technological specialization course': 39,
    'Higher education - degree (1st cycle)': 40,
    'Specialized higher studies course': 41,
    'Professional higher technical course': 42,
    'Higher Education - Master (2nd cycle)': 43,
    'Higher Education - Doctorate (3rd cycle)': 44,
}

father_qualification_options = mother_qualification_options  # Same as mother's qualification

mother_occupation_options = {
    'Student': 0,
    'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers': 1,
    'Specialists in Intellectual and Scientific Activities': 2,
    'Intermediate Level Technicians and Professions': 3,
    'Administrative staff': 4,
    'Personal Services, Security and Safety Workers and Sellers': 5,
    'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry': 6,
    'Skilled Workers in Industry, Construction and Craftsmen': 7,
    'Installation and Machine Operators and Assembly Workers': 8,
    'Unskilled Workers': 9,
    'Armed Forces Professions': 10,
    'Other Situation': 90,
    '(blank)': 99,
    'Health professionals': 122,
    'Teachers': 123,
    'Specialists in information and communication technologies (ICT)': 125,
    'Intermediate level science and engineering technicians and professions': 131,
    'Technicians and professionals, of intermediate level of health': 132,
    'Intermediate level technicians from legal, social, sports, cultural and similar services': 134,
    'Office workers, secretaries in general and data processing operators': 141,
    'Data, accounting, statistical, financial services and registry-related operators': 143,
    'Other administrative support staff': 144,
    'Personal service workers': 151,
    'Sellers': 152,
    'Personal care workers and the like': 153,
    'Skilled construction workers and the like, except electricians': 171,
    'Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like': 173,
    'Workers in food processing, woodworking, clothing and other industries and crafts': 175,
    'Cleaning workers': 191,
    'Unskilled workers in agriculture, animal production, fisheries and forestry': 192,
    'Unskilled workers in extractive industry, construction, manufacturing and transport': 193,
    'Meal preparation assistants': 194,
}

father_occupation_options = mother_occupation_options  # Same as mother's occupation

# Feature Inputs with actual values
application_mode = st.selectbox("Application Mode", list(application_mode_options.keys()))
application_order = st.selectbox("Application Order", list(application_order_options.keys()))
course = st.selectbox("Course", list(course_options.keys()))
prev_qualification_grade = st.slider("Previous Qualification Grade", 0, 200)
mother_qualification = st.selectbox("Mother's Qualification", list(mother_qualification_options.keys()))
father_qualification = st.selectbox("Father's Qualification", list(father_qualification_options.keys()))
mother_occupation = st.selectbox("Mother's Occupation", list(mother_occupation_options.keys()))
father_occupation = st.selectbox("Father's Occupation", list(father_occupation_options.keys()))
admission_grade = st.slider("Admission Grade", 0, 200)
displaced = st.selectbox("Displaced", ["No", "Yes"])
debtor = st.selectbox("Debtor", ["No", "Yes"])
tuition_fees_up_to_date = st.selectbox("Tuition Fees Up To Date", ["No", "Yes"])
gender = st.selectbox("Gender", ["Female", "Male"])
scholarship_holder = st.selectbox("Scholarship Holder", ["No", "Yes"])
age_at_enrollment = st.slider("Age at Enrollment", 15, 80)
curricular_units_1st_sem_enrolled = st.slider("Curricular Units 1st Sem Enrolled", 0, 8)
curricular_units_1st_sem_evaluations = st.slider("Curricular Units 1st Sem Evaluations", 0, 8)
curricular_units_1st_sem_approved = st.slider("Curricular Units 1st Sem Approved", 0, 8)
curricular_units_1st_sem_grade = st.slider("Curricular Units 1st Sem Grade", 0, 20)
curricular_units_2nd_sem_evaluations = st.slider("Curricular Units 2nd Sem Evaluations", 0, 8)
curricular_units_2nd_sem_grade = st.slider("Curricular Units 2nd Sem Grade", 0, 20)
unemployment_rate = st.slider("Unemployment Rate", 0.0, 20.0)
inflation_rate = st.slider("Inflation Rate", 0.0, 20.0)
gdp = st.slider("GDP", 0.0, 20.0)

# Converting
# the selected options to numeric values
application_mode = application_mode_options[application_mode]
application_order = application_order_options[application_order]
course = course_options[course]
mother_qualification = mother_qualification_options[mother_qualification]
father_qualification = father_qualification_options[father_qualification]
mother_occupation = mother_occupation_options[mother_occupation]
father_occupation = father_occupation_options[father_occupation]
displaced = 1 if displaced == "Yes" else 0
debtor = 1 if debtor == "Yes" else 0
tuition_fees_up_to_date = 1 if tuition_fees_up_to_date == "Yes" else 0
gender = 1 if gender == "Male" else 0
scholarship_holder = 1 if scholarship_holder == "Yes" else 0

# Prepare the input for the model
input_features = np.array([
    application_mode, application_order, course, prev_qualification_grade, mother_qualification,
    father_qualification, mother_occupation, father_occupation, admission_grade,
    displaced, debtor, tuition_fees_up_to_date, gender, scholarship_holder,
    age_at_enrollment, curricular_units_1st_sem_enrolled, curricular_units_1st_sem_evaluations,
    curricular_units_1st_sem_approved, curricular_units_1st_sem_grade,
    curricular_units_2nd_sem_evaluations, curricular_units_2nd_sem_grade,
    unemployment_rate, inflation_rate, gdp
]).reshape(1, -1)

# Predict and display the result
if st.button("Predict"):
    prediction = model.predict(input_features)  

    if prediction == 0:
        st.write("Prediction: Dropout")
    elif prediction == 1:
        st.write("Prediction: Enrolled")
    elif prediction == 2:
        st.write("Prediction: Graduate")
