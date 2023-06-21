import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


data = pd.read_csv("data.csv")

num_of_students = len(data.index)

# renaming the columns

new_cols = []

default_cols = [
    "Timestamp",
    "Gender",
]

male_cols = [
    "GPA",
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
]

female_cols = []

for col in male_cols[:-1]:
    female_cols.append("Female " + col)

new_cols.extend(default_cols)
new_cols.extend(male_cols)
new_cols.extend(female_cols)

for i in range(len(data.columns)):
    data = data.rename(columns={data.columns[i]: new_cols[i]})

# renaming the values of the columns
data = data.replace(
    {
        "Gender": {"طالب": "Male", "طالبة": "Female"},
    }
)

# merging female columns with the original columns
for i in range(num_of_students):
    if data.iloc[i]["Gender"] == "Female":
        for j in male_cols[:-1]:
            if pd.isnull(data.iloc[i][j]):
                data.iloc[i][j] = data.iloc[i]["Female " + j]


# dropping the female columns
data.drop(
    female_cols,
    axis=1,
    inplace=True,
)

# dropping the timestamp column
data.drop(
    data.columns[0],
    axis=1,
    inplace=True,
)

# renaming the values of the columns
majors_ar_to_en = {
    "علوم الحاسب": "CS",
    "الأمن السيبراني": "SEC",
    "الذكاء الاصطناعي": "AI",
    "هندسة البرمجيات": "SE",
    "تفاعل الانسان مع الحاسب": "HCI",
    "هندسة الحاسب": "CE",
    "علم البيانات": "DS",
}

for i in data.columns[2:]:
    data[i] = data[i].replace(majors_ar_to_en)

# set gpa value to be the midpoint
for i in range(num_of_students):
    gpa_interval = data.iloc[i][1]
    upper_gpt = float(gpa_interval.split("-")[0])
    midpoint = upper_gpt - 0.05
    data.loc[i, data.columns[1]] = midpoint

male_data = data[data["Gender"] == "Male"]
female_data = data[data["Gender"] == "Female"]


# assign weights to the major ranks
major_weights = [7, 4, 2, 1.5, 1, 0.5, 0.25]

def display_heighest_majors(data, title):
    count = len(data.index)
    majors = majors_ar_to_en.values()

    # make a dict to store the total weighted GPA and count of students in each major
    majors_weighted_gpa_sum = {}
    majors_student_count = {}

    for major in majors:
        majors_weighted_gpa_sum[major] = 0
        majors_student_count[major] = 0

    for i in range(count):
        s_majors = data.iloc[i][2:].values
        student_gpa = data.iloc[i]["GPA"]
        for j in range(len(s_majors)):
            try:
                # calculate the weighted GPA for the major
                major = s_majors[j]
                major_weight = major_weights[j]
                weighted_gpa = student_gpa * major_weight

                # add the weighted GPA to the total for the major
                majors_weighted_gpa_sum[major] += weighted_gpa / 4

                # increment the count of students for the major
                majors_student_count[major] += 1
            except:
                pass
    print(majors_student_count)

    # calculate the average weighted GPA for each major
    majors_avg_weighted_gpa = {}

    for major in majors:
        if majors_student_count[major] > 0:
            majors_avg_weighted_gpa[major] = majors_weighted_gpa_sum[major] / majors_student_count[major]
        else:
            majors_avg_weighted_gpa[major] = 0

    # sort the majors by their average weighted GPA
    sorted_majors = dict(sorted(majors_avg_weighted_gpa.items(), key=lambda item: item[1]))

    # use matplotlib to plot the data
    plt.barh(
        list(sorted_majors.keys()),
        list(sorted_majors.values()),
        color="blue",
        edgecolor="black",
    )

    plt.title(title + f" ({count} students)")

    plt.show()

display_heighest_majors(male_data, "Majors ordered by GPA and choice rank (male students)\n(weighted GPA) " + major_weights.__str__())