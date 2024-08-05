import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df[["race"]]
    race_count["race_count"] = 1
    race_count = race_count.groupby(["race"]).sum()
    race_count = race_count.sort_values(by=["race_count"],ascending=False).values.reshape(-1)

    # What is the average age of men?
    average_age_men = df[["sex", "age"]]
    average_age_men = average_age_men.groupby(["sex"]).mean()
    average_age_men = average_age_men.rename(columns={"age": "average_age_men"})
    average_age_men = average_age_men.loc["Male",["average_age_men"]]
    average_age_men = round(average_age_men["average_age_men"], 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = df[["education"]]
    percentage_bachelors["percentage_bachelors"] = 1.
    percentage_bachelors = percentage_bachelors.groupby(["education"]).sum()
    percentage_bachelors = percentage_bachelors/(percentage_bachelors["percentage_bachelors"]).sum()*100.
    percentage_bachelors = percentage_bachelors.loc["Bachelors",["percentage_bachelors"]]
    percentage_bachelors = round(percentage_bachelors["percentage_bachelors"], 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[["education", "salary"]]
    higher_education[["is_advanced"]] = ((higher_education[["education"]]).apply(lambda x: (x[0]).count('Bachelors'), axis=1, result_type='broadcast').astype(int)+(higher_education[["education"]]).apply(lambda x: (x[0]).count('Masters'), axis=1, result_type='broadcast').astype(int)+(higher_education[["education"]]).apply(lambda x: (x[0]).count('Doctorate'), axis=1, result_type='broadcast').astype(int))
    higher_education = higher_education[higher_education["is_advanced"]>0]
    
    lower_education = df[["education", "salary"]]
    lower_education[["is_advanced"]] = ((lower_education[["education"]]).apply(lambda x: (x[0]).count('Bachelors'), axis=1, result_type='broadcast').astype(int)+(lower_education[["education"]]).apply(lambda x: (x[0]).count('Masters'), axis=1, result_type='broadcast').astype(int)+(lower_education[["education"]]).apply(lambda x: (x[0]).count('Doctorate'), axis=1, result_type='broadcast').astype(int))
    lower_education = lower_education[lower_education["is_advanced"]==0]
    
    # percentage with salary >50K
    higher_education_rich = higher_education.copy(deep=True)
    higher_education_rich["count"] = 1.
    higher_education_rich = ((higher_education_rich[(higher_education_rich[["salary"]]).apply(lambda x: (x[0]).count('>50K'), axis=1, result_type='broadcast').astype(int)["salary"]>0])["count"]).sum()/(higher_education_rich["count"]).sum()*100.
    higher_education_rich = round(higher_education_rich, 1)

    lower_education_rich = lower_education.copy(deep=True)
    lower_education_rich["count"] = 1.
    lower_education_rich = ((lower_education_rich[(lower_education_rich[["salary"]]).apply(lambda x: (x[0]).count('>50K'), axis=1, result_type='broadcast').astype(int)["salary"]>0])["count"]).sum()/(lower_education_rich["count"]).sum()*100.
    lower_education_rich = round(lower_education_rich, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].values.min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = higher_education = df[["hours-per-week", "salary"]]
    num_min_workers = num_min_workers[num_min_workers["hours-per-week"]==min_work_hours]

    rich_percentage = num_min_workers.copy(deep=True)
    rich_percentage["count"] = 1.
    rich_percentage = ((rich_percentage[(rich_percentage[["salary"]]).apply(lambda x: (x[0]).count('>50K'), axis=1, result_type='broadcast').astype(int)["salary"]>0])["count"]).sum()/(rich_percentage["count"]).sum()*100.
    rich_percentage = round(rich_percentage,1)

    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = df[["native-country","salary"]]
    highest_earning_country = highest_earning_country[highest_earning_country["native-country"]!="?"]
    highest_earning_country["high_salary"] = (highest_earning_country[["salary"]]).apply(lambda x: (x[0]).count('>50K'), axis=1, result_type='broadcast').astype(int)
    highest_earning_country = (highest_earning_country[["native-country","high_salary"]]).groupby(["native-country"]).mean()
    highest_earning_country = highest_earning_country.rename(columns={"high_salary": "percentage_high_salary"})
    highest_earning_country["percentage_high_salary"] = highest_earning_country["percentage_high_salary"]*100.
    highest_earning_country = highest_earning_country.sort_values(by=["percentage_high_salary"],ascending=False)
    highest_earning_country = highest_earning_country.reset_index().rename(columns={"native-country":"highest_earning_country", "percentage_high_salary":"highest_earning_country_percentage"})
    highest_earning_country_percentage = highest_earning_country[["highest_earning_country_percentage"]]
    highest_earning_country_percentage = highest_earning_country_percentage.iloc[0]
    highest_earning_country_percentage = round(highest_earning_country_percentage["highest_earning_country_percentage"],1)
    highest_earning_country = highest_earning_country[["highest_earning_country"]]
    highest_earning_country = highest_earning_country.iloc[0]
    highest_earning_country = highest_earning_country["highest_earning_country"]

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = (df[df["native-country"]=="India"])[["occupation","salary"]]
    top_IN_occupation["high_salary"] = (top_IN_occupation[["salary"]]).apply(lambda x: (x[0]).count('>50K'), axis=1, result_type='broadcast').astype(int)
    top_IN_occupation = top_IN_occupation[top_IN_occupation["high_salary"]>0]
    top_IN_occupation["count"] = 1
    top_IN_occupation = (top_IN_occupation[["occupation", "count"]]).groupby(["occupation"]).sum()
    top_IN_occupation = top_IN_occupation.sort_values(by=['count'],ascending=False)
    top_IN_occupation = top_IN_occupation.reset_index().rename(columns={"occupation":"top_IN_occupation"})
    top_IN_occupation = top_IN_occupation[["top_IN_occupation"]]
    top_IN_occupation = top_IN_occupation.iloc[0]
    top_IN_occupation = top_IN_occupation["top_IN_occupation"]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
