import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("What city are you interested in? Please enter: Chicago, New York City, Washington -> "))
        if not city.lower() in ['chicago', 'new york city', 'washington']:
            print("That input isn't recognized - please try again: Chicago, New York City or Washington -> ")
            # Return to start of the loop
            continue
        else:
            # Value accepted
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("What month? Please enter: January, February, March, April, May, June, or All -> "))
        if not month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("That input isn't recognized - please try again: January to June accepted, or All -> ")
            # Return to start of the loop
            continue
        else:
            # Value accepted
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("What day of the week? Please enter: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All -> "))
        if not day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print("That input isn't recognized - please try again: Monday through Sunday, or All -> ")
            # Return to start of the loop
            continue
        else:
            # Value accepted
            break

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
    
    # load the city file preferred
    df = pd.read_csv(CITY_DATA[city.lower()])
    # datetime modifications
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month.lower() != 'all':
        month_map = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        month_value = month_map[month.lower()]
        df = df[df['month'] == month_value]

    # filter by day of week if applicable
    if day.lower() != 'all':
        day = day.lower()
        df = df[df['day_of_week'] == day.title()]
        
    # return the new dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month = months[common_month-1]    
    print('Most common month: ', month)

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week: ', common_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_sstation = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', common_sstation)

    # Display most commonly used end station
    common_estation = df['End Station'].mode()[0]
    print('Most commonly used end station: ', common_estation)

    # Display most frequent combination of start station and end station trip
    df['Both Stations'] = 'Start station: ' + df['Start Station'] + '\n End station: ' + df['End Station']
    frequent_comb = df['Both Stations'].value_counts().idxmax()
    print('Most frequent combination of start station and end station trip:\n', frequent_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Display total travel time
    tot_time = df['Trip Duration'].sum()
    tot_time = str(datetime.timedelta(seconds=int(tot_time)))
    print('Total travel time: ', tot_time)
    
    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time = str(datetime.timedelta(seconds=int(mean_time)))
    print('Mean travel time: ', mean_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types: \n',user_types)
    
    print('\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        # Only access Gender column in this case
        gender_count = df['Gender'].value_counts()
        print('Count of genders: \n',gender_count)
    else:
        print('Gender stats cannot be calculated - \'Gender\' does not appear in the dataframe. Moving on..')

    if 'Birth Year' in df.columns:
        print('\nYear of birth statistics')
        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].value_counts().idxmax()
        print('\n Earliest year of birth: ', int(earliest),
              '\n Most recent year of birth: ', int(most_recent),
              '\n Most common year of birth: ', int(most_common))
    else:
        print('Birth year stats cannot be calculated - \'Birth Year\' does not appear in the dataframe. Moving on..')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no -> ").lower()
    start_loc = 0
    if view_data == 'yes':
        keep_asking = True
    else:
        keep_asking = False
    while (keep_asking):
        print(df.iloc[start_loc:start_loc+6])
        start_loc += 5
        view_display = input("Do you wish to continue? Enter yes or no -> ").lower()
        if view_display == 'yes':
            keep_asking = True
        else:
            keep_asking = False

        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
