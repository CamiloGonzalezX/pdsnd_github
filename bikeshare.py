import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    This will be helpful to obtain important information for an specific given date.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!. We\'ll ask you to provide some information, this will be interactive and guided.')
    #Creation of the list of applicable cities for the user to filter on.
    possible_cities = ["chicago", 'new york city', 'washington']
    city = str(input('What city would you like to explore?: ')).lower().rstrip().lstrip()
    while city not in possible_cities:
        print('You typed a non-valid city. Please try again')
        city = str(input('Please, type the name of the city: ')).lower().rstrip().lstrip()
    month = str(input('Please, type the full name of the month you\'d like to explore (I.e. \'January\', If you want to review all months, please type "all": ')).lower().rstrip().lstrip()
    possible_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    #Loop to make sure user gives a rigth input
    while month not in possible_months:
        print('It seems the month you specified is not written correctly. Check for typos and try again.')
        month = str(input('Please, specify the month (or type \'all\' if you want to see all months: ')).lower().rstrip().lstrip()
    day = str(input('Please, type the full name of the day of the week you\'d like to explore (i.e: \'Wednesday\', If you want to review all days of the week, please type \'all\': ')).lower().rstrip().lstrip()
    #Creation of the list of applicable days of the week for the user to filter on.
    possible_days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    #Loop to make sure user gives a right input
    while day not in possible_days:
        print('It seems the day you specified is not written correctly. Check for typos and try again.')
        day = str(input('Please, specify the day, type "all" if you want to check on all week days: ')).lower().rstrip().lstrip()
          
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load of file
    df = pd.read_csv(CITY_DATA[city])
    #adjust of the data types
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    #Create dictionaries to adjust months in filter
    dict_months = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    #Dictionary to adjust days in filter
    dict_days = {'sunday':6, 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5}
    #filter by month
    if month == 'all':
        df = df
    else:
        df = df[df['Start Time'].dt.month == dict_months[month]]
    #filter by day
    if day == 'all':
        df = df
    else:
        df = df[df['Start Time'].dt.dayofweek == dict_days[day]]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Definition of months in a dict and formula to find the most common one
    dict_months_number = {1: 'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july', 8:'august', 9:'september', 10:'october', 11:'november', 12:'december'}
    try:
        most_common_month = dict_months_number[df['Start Time'].dt.month.mode()[0]]
        print('The most common month for travel is {}! \nNote that if you filtered by month, this is the month you selected at the beggining.'.format(most_common_month))
    except:
        print('It seems there\'s no data to calculate the most frecuent month for the filters you selected. Please try again with other dates.')


    # Definition of days in a dict and formulas to display the most common day of week
    dict_days_number = {6:'sunday', 0:'monday', 1: 'tuesday', 2: 'wednesday', 3:'thursday', 4:'friday', 5:'saturday'}
    try:
        most_common_day = dict_days_number[df['Start Time'].dt.dayofweek.mode()[0]]
        print('\nOn the other hand, the most common day for travel is {}! \nNote that if you filtered by day, this is the day you selected at the beggining.'.format(most_common_day))
    except:
        print('\nIt seems there\'s no data to calculate the most frecuent day for the filters you selected. Please try again with other dates.')


    # Next, lines of code to exctract hours for each record and display statistics
    # As hour is given en 24h format, next lines of code will convert it in 12 hours mode, to make it easier to analyze.
    try:
        most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
        if most_common_start_hour < 12:
            most_common_start_hour = str(most_common_start_hour) + ' a.m.'
        else:
            most_common_start_hour = str(most_common_start_hour - 12) + ' p.m.'
        print('\nFor the selected period of time, travels start the most at {}!'.format(most_common_start_hour))
    except:
        print('\nIt seems there\'s no data to calculate the most frecuent time for the filters you selected. Please try again with other dates.')
        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Here, we extract the start station to find the most common one
    try:
        most_common_start_station = df['Start Station'].mode()[0]
        print('The most popular start station is {}!'.format(most_common_start_station))
    except:
        print('There\'s no data for the filters you selected to calculate the most popular start station. Please, try again selecting diferent filters')


    # This block is useful to display the most commonly used end station
    try:
        most_common_end_station = df['End Station'].mode()[0]
        print('\nThe station where most travels ended for the selected period of time is {}!'.format(most_common_end_station))
    except:
        print('\nWith the filters you selected, there\'s no data to calculate the most popular end station. Please, try again selecting diferent filters')


    # This line of code will mix the stations where travles start and end to find the most common combination
    try:
        df['combination'] = 'start at ' + df['Start Station'] + ' and end at ' + df['End Station']
        most_common_pair = df['combination'].mode()[0]
        print('\nWhen it comes to combinations, the most travels {}!'.format(most_common_pair))
    except:
        print('\nWith the filters you selected, there\'s no data to calculate the most popular combination of stations. Please, try again selecting diferent filters')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # This lines of code allows us to watch the duration of trips. As this information is given in seconds, it is divided by 3600 to show duration in hours
    try:
        total_time = df['Trip Duration'].sum()
        total_time_hours = total_time / 3600
        print('The total duration of trips for the selected period of time is {} seconds! Which is equivalent to {} hours!'.format(total_time, total_time_hours))
    except:
        print('\nWith the filters you selected, there\'s no data to calculate the total travel time. Please, try again selecting diferent filters')


    # Lines of code to describe mean travel tima
    try:
        mean_time = df['Trip Duration'].mean()
        mean_time_hours = mean_time / 3600
        print('\nThe mean duration of trips for the selected period of time is {} seconds! Which is equivalent to {} hours!'.format(mean_time, mean_time_hours))
    except:
        print('\nWith the filters you selected, there\'s no data to calculate the mean travel time. Please, try again selecting diferent filters')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counting users by their type
    try:
        user_values = df['User Type'].value_counts()
        print('For the selected period of time, this is the total of users based on their type:\nSubscribers: {}\nCustomers: {}'.format(user_values[0], user_values[1]))
    except:
        print('It seems we don\'t have information on the user types for the selected filters you used. Try again with different filters')
    


    # Counting users by their gender. I add the if statement for the code to run only uf the database contains this columns, as Washington doesn't have this information.
    columns = list(df.columns)
    if 'Gender' in columns:
        try:
            user_gender = df['Gender'].value_counts()
            print('\nFor the selected period of time, this is the distribution of users gender:\nMale: {}\nFemale: {}'.format(user_gender[0], user_gender[1]))
        except:
            print('\nIt seems we don\'t have information on the user gender for the selected filters you used. Try again with different filters')
    

    # Showing the earliest, most recent and most common year of birth of the users. I add the if statement for the code to run only uf the database contains this columns, as Washington doesn't have this information.
    if 'Birth Year' in columns:
        try:
            earliest_year = df['Birth Year'].min()
            print('\nThe earliest year of birth for users in our database for the selected filters is {}'.format(int(earliest_year)))
        except:
            print('\nIt seems we don\'t have information on the earliest year of birth for the selected filters you used. Try again with different filters')
    
        try:
            recent_year = df['Birth Year'].max()
            print('\nThe most recent year of birth for users in our database for the selected filters is {}'.format(int(recent_year)))
        except:
            print('\nIt seems we don\'t have information on the most recent year of birth for the selected filters you used. Try again with different filters')
    
        try:
            common_year = df['Birth Year'].mode()
            print('\nThe most common year of birth for users in our database for the selected filters is {}'.format(int(common_year)))
        except:
            print('\nIt seems we don\'t have information on the most common year of birth for the selected filters you used. Try again with different filters')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays groups of 5 lines of raw data if user wants to see it."""
    possible_answers = ["yes", "no"]
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    while view_data not in possible_answers:
        print('The command you entered is not valid. Check for typos.')
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower().rstrip().lstrip()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        view_data = input("Do you wish to continue?: (yes or no)").lower().lstrip().rstrip()
        while view_data not in possible_answers:
            print('The command you entered is not valid. Check for typos.')
            view_data = input("Do you wish to continue?: (yes or no)").lower().rstrip().lstrip()
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
