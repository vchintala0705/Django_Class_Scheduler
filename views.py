from django.shortcuts import render
import pandas as pd
import numpy as np
from harsha_project_1 import settings

df = pd.read_html(f"{settings.TEMPLATE_DIR}\Murray State Classes - Classes.html") # reads html file and stores the tables present in html in the variable df
df = df[0]       # stores the only available table in df df

df.columns = [i[1] for i in df.columns] # rename columns [('ACC Accounting, "Status"), ***]

uniq_counts = df.nunique(axis=1)   # remove recoreds with single value in all columns
df = df[uniq_counts > 1]

df = df[df['CRN'].astype(str).str.match(r'^\d{5}$')] # filter recoreds with valid crn i.e it should have 5 digits

df['Start Time'] = pd.to_datetime(df['Time'].str.split('-').str[0], format='%I:%M %p', errors='coerce') # calculate start and end times for schedule generation 
df['End Time'] = pd.to_datetime(df['Time'].str.split('-').str[1], format='%I:%M %p', errors='coerce')

offline_classes = df[df["Start Time"].notna()]            ## filter out invalid courses
online_classes = df[df["Time"] == 'WEB']            # store online courses in another var to check WEB courses

# concatenate offline and online courses for total valid courses
valid_classes = pd.concat([offline_classes, online_classes], axis=0)

# reset the index of data frame to CRN.
valid_classes.reset_index(drop=True, inplace=True)

# drop unnecessary columns
columns_to_drop = ["Status", "Date (MM/DD)"]
valid_classes = valid_classes.drop(columns=columns_to_drop)


# helper function for student schedule
def student_schedule(crns):

    # check if given crn's are valid
    crn_list = crns.split(',')
    if len(crn_list) < 3:
        return False, "Atleast three CRN's are needed"
    
    # filter recoreds with given crn
    offline_crns = list(offline_classes["CRN"])
    online_crns = list(online_classes["CRN"])
    df_crns = list(df["CRN"])


    selected_crns = []  # proper offline courses count
    online_crn_count = 0 # web class count
    bad_crns = []  # values of web courses 
    # check for valid CRN's and decide 
    for crn in crn_list:
        if crn.strip() in offline_crns:
            selected_crns.append(crn.strip())
        elif crn.strip() in online_crns:
            online_crn_count += 1
            bad_crns.append(crn.strip())
        elif crn.strip() in df_crns:
            return False, f"CRN '{crn.strip()}' doesn't have valid 'Time'"
        else:
            return False, f"CRN '{crn.strip()} doesn't exist in given database"

    # web classes can't be more than 1
    if online_crn_count > 1:
        s = f"Following CRN's belong to WEB class. {','.join(bad_crns)}. The count of WEB classes can't be more than 1"
        return False, s

    # coureses for given CRN's 
    selected_courses = offline_classes[offline_classes['CRN'].astype(str).isin(selected_crns)]

    # schedule dictionary for each day of the week
    schedule = {'M': [], 'T': [], 'W': [], 'R': [], 'F': [], 'S': [], 'U': []}

    # dictionary to track course conflicts
    conflicts = {}

    # Iterate through selected courses
    for _, course in selected_courses.iterrows():
        crn = str(course['CRN'])
        days = course['Days']
        start_time = course['Start Time']
        end_time = course['End Time']
        subj = course['Subj']
        
        # Check for conflicts and update schedule
        for day in days:
            if any(c['End Time'] > start_time and c['Start Time'] < end_time for c in schedule[day]):
                if crn not in conflicts:
                    conflicts[crn] = []
                conflicts[crn].extend([c['CRN'] for c in schedule[day] if c['End Time'] > start_time and c['Start Time'] < end_time])

            schedule[day].append({'CRN': crn, 'Start Time': start_time, 'End Time': end_time, 'Subj':subj})

    cols = ["M","T", 'W', 'R','F','S','U']
    schedule_df = pd.DataFrame(columns=cols)

    # make index of dataframe as the CRN's of given courses
    for crn in selected_crns:
        new_row = pd.Series(index=schedule_df.columns, dtype=np.int64, name=crn)
        new_row[:] = np.nan
        schedule_df = pd.concat([schedule_df, new_row.to_frame().T])

    # store the dataframes 
    for day, courses in schedule.items():
        if len(courses)>0:
            for item in courses:
                s = f"{item['Subj']} - ({str(item['Start Time']).split()[1]}, {str(item['End Time']).split()[1]})"
                if pd.isna(schedule_df.at[item["CRN"],day]):
                    schedule_df.loc[item["CRN"],day] = s
                else:
                    schedule_df.loc[item["CRN"],day] = str(schedule_df.at[item["CRN"],day]) + '\n' + s
    # Display conflicts
    col_maps = {"M":"Monday","T":"Tuesday", 'W':"Wednesday", 'R':"Thursday",'F':"Friday",'S':"Saturday",'U':"Sunday"}
    schedule_df.rename(columns=col_maps, inplace=True)
    schedule_df.fillna("-------", inplace=True)

    # show conflicts if any
    if conflicts:
        conf = "Conflicts: " + '\n'
        for crn, conflicting_crns in conflicts.items():
            conf += f"CRN {crn} conflicts with CRN(s) {', '.join(conflicting_crns)}\n"
        return False, conf
    return True, schedule_df


# helper function for teacher schedule
def teacher_schedule(instructor_name):

    # filter courses with given instrucor
    selected_courses = offline_classes[offline_classes['Instructor'] == instructor_name]

    # Initialize a schedule dictionary for each day of the week
    schedule = {'M': [], 'T': [], 'W': [], 'R': [], 'F': [], 'S': [], 'U': []}

    # Initialize a dictionary to track course conflicts
    conflicts = {}

    # Iterate through selected courses
    for _, course in selected_courses.iterrows():
        crn = str(course['CRN'])
        days = course['Days']
        start_time = course['Start Time']
        end_time = course['End Time']
        subj = course['Subj']
        
        # Check for conflicts and update schedule
        for day in days:
            if any(c['End Time'] > start_time and c['Start Time'] < end_time for c in schedule[day]):
                if crn not in conflicts:
                    conflicts[crn] = []
                conflicts[crn].extend([c['CRN'] for c in schedule[day] if c['End Time'] > start_time and c['Start Time'] < end_time])

            schedule[day].append({'CRN': crn, 'Start Time': start_time, 'End Time': end_time, 'Subj':subj})

    cols = ["M","T", 'W', 'R','F','S','U']
    schedule_df = pd.DataFrame(columns=cols)

    # create empty df for selected CRN's
    for crn in list(selected_courses["CRN"]):
        new_row = pd.Series(index=schedule_df.columns, dtype=np.int64, name=crn)
        new_row[:] = np.nan
        schedule_df = pd.concat([schedule_df, new_row.to_frame().T])

    # fill df with proper values
    for day, courses in schedule.items():
        if len(courses)>0:
            for item in courses:
                s = f"{item['Subj']} - ({str(item['Start Time']).split()[1]}, {str(item['End Time']).split()[1]})"
                if pd.isna(schedule_df.at[item["CRN"],day]):
                    schedule_df.loc[item["CRN"],day] = s
                else:
                    schedule_df.loc[item["CRN"],day] = str(schedule_df.at[item["CRN"],day]) + '\n' + s
    
    # Display conflicts
    col_maps = {"M":"Monday","T":"Tuesday", 'W':"Wednesday", 'R':"Thursday",'F':"Friday",'S':"Saturday",'U':"Sunday"}
    schedule_df.rename(columns=col_maps, inplace=True)
    schedule_df.fillna("-------", inplace=True)
    if conflicts:
        conf = "Conflicts: " + '\n'
        for crn, conflicting_crns in conflicts.items():
            conf += f"CRN {crn} conflicts with CRN(s) {', '.join(conflicting_crns)}\n"
        return False, conf
    return True, schedule_df

# Create your views here.
# view for home page
def home_view(request):
    return render(request, 'index.html')

# view for view_content page
def content_view(request):
    # create a local so that original info won't be lost
    vc_copy= valid_classes.copy()
    # remove unncessary columns as they don't make while displaying in page
    columns_to_drop = ["Start Time", "End Time"]
    vc_copy.drop(columns_to_drop, axis=1)

    # my_dict is shared to html file
    my_dict = {"table": vc_copy.to_html(classes='table table-stripped table-bordered table-hover')}

    # if we get form submit request from page
    if request.method == "POST":
        # get the values of entered  input text fields 
        crn = request.POST.get("crn")
        subject = request.POST.get("subject")
        course = request.POST.get("course")
        instructor = request.POST.get("instructor")

        if not any([crn, subject, course, instructor]):
            my_dict['table'] = "Please provide atleast one filter"
            return render(request, 'view_content.html', context=my_dict)

        # filter the dataframe with given values 
        if crn:
            vc_copy = vc_copy[vc_copy["CRN"] == crn]
        if subject:
            vc_copy = vc_copy[vc_copy["Subj"] == subject]
        if course:
            vc_copy = vc_copy[vc_copy["Crse"].str.contains(course)]
        if instructor:
            vc_copy = vc_copy[vc_copy["Instructor"].str.contains(instructor)]
        
        # check if the dataframe is of 0 length or not before sending it to html file
        if len(vc_copy) == 0:
            my_dict["table"] = "No Courses found with given filters"
        else:
            my_dict["table"] = vc_copy.to_html(classes='table table-stripped table-bordered table-hover')
        
        return render(request, 'view_content.html', context=my_dict)
    return render(request, 'view_content.html', context=my_dict)

# view function for student schedure
def student_schedule_view(request):
    my_dict = {"table": None, 'greeting':None}

    # if we get form submit request from use
    if request.method == "POST":
        crn = request.POST.get("crn")
        if crn:
            status, content = student_schedule(crn)
        else:
            my_dict["table"] = "Please provide CRN's"
            return render(request, 'student_schedule.html', context=my_dict)
        if status:
            my_dict["table"] = content.to_html(classes='table table-stripped table-bordered table-hover')
            my_dict["greeting"] = "Weekly schedule of student with given CRN's"
        else:
            my_dict["table"] = content
        return render(request, 'student_schedule.html', context=my_dict)
    return render(request, 'student_schedule.html', context=my_dict)

# view function for teacher view
def schedule_teacher_view(request):
    vc_copy = valid_classes.copy()
    # instructors = list(vc_copy["Instructor"])
    instructors = list(vc_copy["Instructor"].unique())
    my_dict= {"table":None, "dropdown_list":instructors,'greeting':None}
    if request.method == "POST":
        instructor_name = request.POST.get("dropdown");
        status, content = teacher_schedule(instructor_name)
        if status:
            my_dict["greeting"] = f"Weekly schedule of instructor {instructor_name}"
            my_dict["table"] = content.to_html(classes='table table-stripped table-bordered table-hover')
        else:
            my_dict["table"] = content
        return render(request, "teacher_schedule.html", context=my_dict)
    return render(request, "teacher_schedule.html", context=my_dict)
