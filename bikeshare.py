import time
import pandas as pd
import numpy as np


CITY_DATA = {
            'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'
            }


def display_raw_data(df):
    """Displays raw data in increments of 5 rows upon user request."""
    start = 0
    while True:
        show_data = input("Would you like to see 5 rows of raw data? Enter yes or no.\n").strip().lower()
        if show_data not in ['yes', 'y']:
            break
        print(df.iloc[start:start+5])  # Display 5 rows
        start += 5
        if start >= len(df):
            print("No more data to display.")
            break


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose a city: chicago, new york city, washington\n').strip().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        print('\nInvalid input. Please enter one of: chicago, new york city, washington.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Choose a month: all, january, february, ... , june\n').strip().lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        print('\nInvalid input. Please enter a valid month from January to June or "all".')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Choose a day of week: all, monday, tuesday, ... sunday\n').strip().lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        print('\nInvalid input. Please enter a valid day or "all".')

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
    if city == 'chicago':
        df = pd.read_csv(CITY_DATA['chicago'])

    elif city == 'new york city':
        df = pd.read_csv(CITY_DATA['new york city'])

    else:
        df = pd.read_csv(CITY_DATA['washington'])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        df = df[df['Start Time'].dt.month_name().str.lower() == month]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): The filtered bikeshare data.
    Prints:
        The most common month, day, and start hour along with their counts.
    """

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # Most common month
    most_common_month_name = df['Start Time'].dt.month_name().value_counts(ascending=False).index[0]
    most_common_month_count = df['Start Time'].dt.month_name().value_counts(ascending=False).iloc[0]

    print('\nThe most common month:', most_common_month_name)
    print('The Count:', most_common_month_count)

    # Most common day of week
    most_common_day_name = df['Start Time'].dt.day_name().value_counts(ascending=False).index[0]
    most_common_day_count = df['Start Time'].dt.day_name().value_counts(ascending=False).iloc[0]

    print('\nThe most common day of week:', most_common_day_name)
    print('The Count:', most_common_day_count)

    # Most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.value_counts(ascending=False).index[0]
    most_common_hour_count = df['Start Time'].dt.hour.value_counts(ascending=False).iloc[0]

    print('\nThe most common start hour:', most_common_start_hour)
    print('The Count:', most_common_hour_count)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): The filtered bikeshare data.
    Prints:
        The most common start station, end station, and stations combination along with their counts.
    """
    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # Most common start station
    most_common_start_station_name = df['Start Station'].value_counts(ascending=False).index[0]
    most_common_start_station_count = df['Start Station'].value_counts(ascending=False).iloc[0]

    print('\nThe most common Start Station:', most_common_start_station_name)
    print('The Count:', most_common_start_station_count)

    # Most common end station
    most_common_end_station_name = df['End Station'].value_counts(ascending=False).index[0]
    most_common_end_station_count = df['End Station'].value_counts(ascending=False).iloc[0]

    print('\nThe most common end station:', most_common_end_station_name)
    print('The Count:', most_common_end_station_count)

    # Most frequent combination of start station and end station trip
    trip_count = df.groupby(['Start Station', 'End Station'])['Start Station'].count().reset_index(name='Count')

    # Most frequent trip
    most_frequent_trip = trip_count.sort_values(by='Count', ascending=False).iloc[0]

    print(f"\nThe Start Station: {most_frequent_trip['Start Station']} \nThe End Station: {most_frequent_trip['End Station']} \nThe Count: {most_frequent_trip['Count']}")
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): The filtered bikeshare data.
    Prints:
        The total travel time, mean travel time.
    """
    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time:', pd.Timedelta(total_travel_time, "s"))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:',  pd.Timedelta(mean_travel_time, "s"))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (DataFrame): The filtered bikeshare data.
    Prints:
        The counts of user types, counts of gender, earliest, most recent, and most common year of birth.
    """
    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts(ascending=False).to_string(header=False)

    print('\nCounts of user types:\n'+user_types_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts(ascending=False).to_string(header=False)
        print('\nCounts of genders:\n'+gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = df.sort_values(by=['Birth Year'])['Birth Year'].min()
        most_recent_year_of_birth = df.sort_values(by=['Birth Year'])['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].value_counts(ascending=False).index[0]
        most_common_year_of_birth_count = df['Birth Year'].value_counts(ascending=False).iloc[0]

        print('\nEarliest year of birth:', int(earliest_year_of_birth))
        print('\nMost recent year of birth:', int(most_recent_year_of_birth))
        print('\nMost Common year of birth:', int(most_common_year_of_birth))
        print('The Count:', most_common_year_of_birth_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart not in ['yes', 'y']:
            break


if __name__ == "__main__":
    main()
