import pandas as pd
import matplotlib.pyplot as plt

# Constants
DEFAULT_COLS = ["Timestamp", "Gender"]
MAIN_COLS = ["GPA", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
MAJOR_WEIGHTS = [7, 4, 2, 1.5, 1, 0.5, 0.25]
MAJORS_AR_TO_EN = {
    "علوم الحاسب": "CS",
    "الأمن السيبراني": "SEC",
    "الذكاء الاصطناعي": "AI",
    "هندسة البرمجيات": "SE",
    "تفاعل الانسان مع الحاسب": "HCI",
    "هندسة الحاسب": "CE",
    "علم البيانات": "DS"
}

# Read CSV data
data = pd.read_csv("data.csv")

# Rename columns
new_cols = DEFAULT_COLS + MAIN_COLS + [f"Female {col}" for col in MAIN_COLS[:-1]]
data.columns = new_cols

# Rename values of the columns
data["Gender"].replace({"طالب": "Male", "طالبة": "Female"}, inplace=True)

# Merge female columns with original columns
for i in range(len(data)):
    if data.at[i, "Gender"] == "Female":
        for j in MAIN_COLS[:-1]:
            if pd.isnull(data.at[i, j]):
                data.at[i, j] = data.at[i, f"Female {j}"]

# Drop timestamp and female columns
data.drop(columns=["Timestamp"] + [f"Female {col}" for col in MAIN_COLS[:-1]], inplace=True)

# Rename values of the columns
data.iloc[:, 2:] = data.iloc[:, 2:].replace(MAJORS_AR_TO_EN)

# Set GPA value to be the midpoint
for i in range(len(data)):
    gpa_interval = data.at[i, "GPA"]
    upper_gpt = float(gpa_interval.split("-")[0])
    midpoint = upper_gpt - 0.05
    data.at[i, "GPA"] = midpoint

# Separate male and female data
male_data = data[data["Gender"] == "Male"]
female_data = data[data["Gender"] == "Female"]

# get masseurs of central tendency
male_average_gpa = male_data["GPA"].mean()
female_average_gpa = female_data["GPA"].mean()

male_mode_gpa = male_data["GPA"].mode()[0]
female_mode_gpa = female_data["GPA"].mode()[0]

male_median_gpa = male_data["GPA"].median()
female_median_gpa = female_data["GPA"].median()

print(f"{'Male GPA:':<15} Average = {male_average_gpa:.2f}, Mode = {male_mode_gpa:.2f}, Median = {male_median_gpa:.2f}")
print(f"{'Female GPA:':<15} Average = {female_average_gpa:.2f}, Mode = {female_mode_gpa:.2f}, Median = {female_median_gpa:.2f}")

def display_highest_majors(data, title):
    # Make a dict to store the total weighted GPA and count of students in each major
    majors_weighted_gpa_sum = {major: 0 for major in MAJORS_AR_TO_EN.values()}
    majors_student_count = {major: 0 for major in MAJORS_AR_TO_EN.values()}

    for i in range(len(data.index)):
        student_majors = data.iloc[i, 2:].values
        student_gpa = data.iloc[i]["GPA"]
        for j, major in enumerate(student_majors):
            try:
                # Calculate the weighted GPA for the major depending on the choice rank
                major_weight = MAJOR_WEIGHTS[j]
                weighted_gpa = student_gpa * major_weight

                # Add the weighted GPA to the total for the major
                majors_weighted_gpa_sum[major] += weighted_gpa / 4

                # Increment the count of students for the major
                majors_student_count[major] += 1
            except:
                pass

    # Calculate the average weighted GPA for each major
    majors_avg_weighted_gpa = {
        major: majors_weighted_gpa_sum[major] / majors_student_count[major]
        if majors_student_count[major] > 0
        else 0
        for major in MAJORS_AR_TO_EN.values()
    }

    # Sort the majors by their average weighted GPA
    sorted_majors = dict(sorted(majors_avg_weighted_gpa.items(), key=lambda item: item[1]))

    # Plot the data using matplotlib
    plt.barh(list(sorted_majors.keys()), list(sorted_majors.values()), color="blue", edgecolor="black")
    plt.title(f"{title} ({len(data)} students)")
    plt.show()

# Display highest majors for male students
display_highest_majors(male_data, "Majors ordered by GPA and choice rank (male students)\n(weighted GPA) " + str(MAJOR_WEIGHTS))