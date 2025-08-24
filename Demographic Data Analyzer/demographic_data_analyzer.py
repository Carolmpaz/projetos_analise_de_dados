import pandas as pd

def calculate_demographic_data(print_data=True):
    # Lê os dados
    df = pd.read_csv("adult.data.csv")

    # 1. Quantas pessoas de cada raça
    race_count = df['race'].value_counts()

    # 2. Idade média dos homens
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Porcentagem com diploma de Bacharel
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. Pessoas com educação avançada
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    # Porcentagem com educação avançada que ganham >50K
    higher_education_rich = round((df[higher_education]['salary'] == '>50K').mean() * 100, 1)

    # Porcentagem sem educação avançada que ganham >50K
    lower_education_rich = round((df[lower_education]['salary'] == '>50K').mean() * 100, 1)

    # 5. Mínimo de horas por semana
    min_work_hours = df['hours-per-week'].min()

    # 6. Porcentagem dos que trabalham min horas e ganham >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((num_min_workers['salary'] == '>50K').mean() * 100, 1)

    # 7. País com maior porcentagem de >50K
    country_50k = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_total = df['native-country'].value_counts()
    country_percentage = (country_50k / country_total * 100).round(1)

    highest_earning_country = country_percentage.idxmax()
    highest_earning_country_percentage = country_percentage.max()

    # 8. Ocupação mais popular na Índia entre os ricos
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_rich['occupation'].value_counts().idxmax()

    # Retorno em dicionário
    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich people in country:", highest_earning_country_percentage)
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
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
