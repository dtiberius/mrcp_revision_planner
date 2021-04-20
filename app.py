import numpy as np
import streamlit as st
from datetime import date

st.set_page_config(page_title="Sales Entry", layout="wide")
st.title("The Key Medicine MRCP Part 1 Revision Planner")

expander = st.beta_expander('About')
# get blurb
@st.cache(suppress_st_warning=True)
def get_blurb():
    f = open("blurb.txt", "r")
    blurb = f.read()
    f.close()
    return blurb

blurb = get_blurb()

expander.markdown(blurb)

st.markdown('')

# enter exam date
exam_date = st.selectbox('Which exam are you planning to sit?', ['24 Aug 2021', '23 Nov 2021'])

@st.cache(suppress_st_warning=True)
def date_calc():
    if exam_date == '24 Aug 2021':
        exam_date_formatted = date(2021,8,24)
    else:
        exam_date_formatted = date(2021,11,23)
    days_until_exam = (exam_date_formatted - date.today()).days
    weeks_until_exam = round(days_until_exam/7)
    st.markdown(f'There are {days_until_exam} days until your exam (roughly {weeks_until_exam} weeks). How much revision do you have time for between now and then? Be ambitious but realistic.')

date_calc()

# create sidebar
col1 = st.sidebar

knowledge_categories = ['significant gaps', 'okay', 'good', 'comprehensive']

# weight the knowledge categories
over_30_knowledge_weights = {
    knowledge_categories[0]:2.5,
    knowledge_categories[1]:1.75,
    knowledge_categories[2]:1,
    knowledge_categories[3]:0
    }
over_20_knowledge_weights = {
    knowledge_categories[0]:1.75,
    knowledge_categories[1]:1,
    knowledge_categories[2]:0.01,
    knowledge_categories[3]:0
    }
over_10_knowledge_weights = {
    knowledge_categories[0]:1,
    knowledge_categories[1]:0.5,
    knowledge_categories[2]:0.001,
    knowledge_categories[3]:0
    }

specialties = ['Cardiology','Clinical Pharmacology and Therapeutics','Dermatology','Endocrinology, diabetes and metabolic medicine',
    'Gastroenterology and Hepatology','Geriatrics','Haematology','Infectious diseases','Neurology','Oncology',
    'Medical ophthalmology','Palliative medicine and end of life care','Psychiatry','Renal medicine','Respiratory medicine',
    'Rheumatology', 'Cell, molecular and membrane biology','Clinical anatomy','Clinical biochemistry and metabolism',
    'Clinical physiology','Genetics','Immunology','Statistics, epidemiology and evidence-based medicine']

initial_weights = [14,15,8,14,14,8,10,14,14,5,4,4,9,14,14,14,2,3,4,4,3,4,5]

# add hours input (currently on main section)
hours_input = st.number_input("Hours available for revision:", min_value=10, value=40, max_value=400,step=1)

# add syllabus revision for high hours
if hours_input > 25:
    syllabus = 1.5
else:
    syllabus = 0

if syllabus == 1.5:
    non_specialty = (hours_input - 1.5)*0.1
else:
    non_specialty = 0

hours = hours_input - non_specialty - syllabus

# add content to sidebar
col1.markdown("Please rate your current expertise in each specialty listed:")
s1 = col1.select_slider(specialties[0], knowledge_categories, 'okay')
s2 = col1.select_slider(specialties[1], knowledge_categories, 'okay')
s3 = col1.select_slider(specialties[2], knowledge_categories, 'okay')
s4 = col1.select_slider(specialties[3], knowledge_categories, 'okay')
s5 = col1.select_slider(specialties[4], knowledge_categories, 'okay')
s6 = col1.select_slider(specialties[5], knowledge_categories, 'okay')
s7 = col1.select_slider(specialties[6], knowledge_categories, 'okay')
s8 = col1.select_slider(specialties[7], knowledge_categories, 'okay')
s9 = col1.select_slider(specialties[8], knowledge_categories, 'okay')
s10 = col1.select_slider(specialties[9], knowledge_categories, 'okay')
s11 = col1.select_slider(specialties[10], knowledge_categories, 'okay')
s12 = col1.select_slider(specialties[11], knowledge_categories, 'okay')
s13 = col1.select_slider(specialties[12], knowledge_categories, 'okay')
s14 = col1.select_slider(specialties[13], knowledge_categories, 'okay')
s15 = col1.select_slider(specialties[14], knowledge_categories, 'okay')
s16 = col1.select_slider(specialties[15], knowledge_categories, 'okay')
s17 = col1.select_slider(specialties[16], knowledge_categories, 'okay')
s18 = col1.select_slider(specialties[17], knowledge_categories, 'okay')
s19 = col1.select_slider(specialties[18], knowledge_categories, 'okay')
s20 = col1.select_slider(specialties[19], knowledge_categories, 'okay')
s21 = col1.select_slider(specialties[20], knowledge_categories, 'okay')
s22 = col1.select_slider(specialties[21], knowledge_categories, 'okay')
s23 = col1.select_slider(specialties[22], knowledge_categories, 'okay')

knowledge_inputs = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23]

# create knowledge coefficients from knowledge inputs
if hours_input > 30:
    knowledge_coefficients = [over_30_knowledge_weights[knowledge_input] for knowledge_input in knowledge_inputs]
elif hours_input > 20:
    knowledge_coefficients = [over_20_knowledge_weights[knowledge_input] for knowledge_input in knowledge_inputs]
else:
    knowledge_coefficients = [over_10_knowledge_weights[knowledge_input] for knowledge_input in knowledge_inputs]

# calculate double-weighted time split
double_weighted = np.array(initial_weights) * np.array(knowledge_coefficients)
normed = [i/sum(double_weighted) for i in double_weighted]
hours_per_specialty = [hours*proportion for proportion in normed]
hours_per_specialty = [round(specialty*2)/2 for specialty in hours_per_specialty]

# calculate hours not yet distributed
remaining_hours = round((hours_input - syllabus - non_specialty - np.sum(hours_per_specialty))*2)/2
removals = int(remaining_hours/0.5)
indices = [i for i in range(23)]

# add spare time or remove over-allocated time
if remaining_hours > 0:

    # order specialties by hours
    dummy = sorted(zip(hours_per_specialty, indices), reverse=False)
    # remove specialties with zero hours (as these don't need revising at all)
    dummy = list(filter(lambda x: x[0] != 0, dummy))
    # get the bottom three
    dummy = dummy[:removals]
    # remove zero entries as these don't need extra time
    adders = [i[1] for i in dummy]

    # add 30 minutes to bottom !three!
    for i in adders:
        hours_per_specialty[i] = hours_per_specialty[i] + 0.5
elif remaining_hours < 0:

    # locate top n time buckets
    dummy = sorted(zip(hours_per_specialty, indices), reverse=True)[:(-removals)]
    subtractors = [i[1] for i in dummy]

    # subtract 30 minutes to bottom !three!
    for i in subtractors:
        hours_per_specialty[i] = hours_per_specialty[i] - 0.5

# calculate true non-specialism value
non_specialty_print = hours_input - np.sum(hours_per_specialty) - syllabus

# write non-specialty time if present
if syllabus == 1.5:
    st.write(f'{syllabus} hours familiarising yourself with the official syllabus')

# write specialty time
for i in range(23):
    if hours_per_specialty[i] > 0:
        st.write(f'{hours_per_specialty[i]} hours revising {specialties[i]}')

# write non-specialty time if present
if syllabus == 1.5:
    st.write(f'{non_specialty_print} hours non-specialism revision (random MCQs and presentation-focused content)')