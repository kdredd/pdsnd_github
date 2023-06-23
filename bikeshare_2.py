import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

YES_NO = ['yes', 'no']

def check_input(prompt, valid_inputs):
    """
    Asks user for input using the supplied prompt, checking against valid inputs.  Repeats prompt until valid input is supplied.

    Args:
        (str) prompt - prompt string for user input
        (list) valid_inputs - list of strings that constitute valid input
    Returns:
        (str) user_input - valid user input
    """
    while True:
        user_input = input(prompt).lower()
        if not user_input in valid_inputs:
            print('\n\tInvalid input!  Please try again.\n')
            continue
        break

    return user_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    city = check_input('Enter name of city to analyze (Chicago, New York City, or Washington): ', CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
    month = check_input('Enter name of month to filter by (January, February, March, April, May, or June), or "all" to apply no month filter: ', MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input('Enter name of day of week to filter by, or "all" to apply no day filter: ', DAYS)

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_num = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']==month_num]
        
    # filter by day of week if applicable
    if day != 'all':
        day_num = DAYS.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day_num]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: %s' % MONTHS[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print('Most common day of week: %s' % DAYS[df['day_of_week'].mode()[0]].title())

    # display the most common start hour
    print('Most common start hour: %02d' % df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: %s' % df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station: %s' % df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most common trip: %s' % df['trip'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time (seconds): %f' % df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time (seconds): %f' % df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of users of each type:')
    user_types = df['User Type'].value_counts(dropna=False)
    for i in range(len(user_types)):
        print('\t%s: %d' % (user_types.index[i], user_types[i]))

    # Display counts of gender
    print('\nNumber of users of each gender:')
    try:
        genders = df['Gender'].value_counts(dropna=False)
        for i in range(len(genders)):
            print('\t%s: %d' % (genders.index[i], genders[i]))
    except KeyError:
        print('\tGender data does not exist.')

    # Display earliest, most recent, and most common year of birth
    print('\nBirth year statistics:')
    try:
        print('\tEarliest birth year: %d' % df['Birth Year'].min())
        print('\tMost recent birth year: %d' % df['Birth Year'].max())
        print('\tMost common birth year: %d' % df['Birth Year'].mode()[0])
    except KeyError:
        print('\tBirth year data does not exist.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data from DataFrame, 5 rows at a time.  Continues until user responds no or there is no more raw data."""
    ind = 0
    while True:
        #Get user input on whether or not display of raw data is desired
        if ind==0:
            display_data = check_input('\nWould you like to display the first 5 rows of raw data?  Enter yes or no.\n', YES_NO)
        else:
            display_data = check_input('\nWould you like to display the next 5 rows of raw data?  Enter yes or no.\n', YES_NO)
            
        if display_data != 'yes':
            break

        #Print 5 rows of data from the DataFrame; if fewer than 5 rows are returned, the end of the data has been reached
        rows_data = df.iloc[ind:ind+5]
        if len(rows_data) < 5:
            print(rows_data)
            print('\nEnd of data reached.\n')
            break
        else:
            print(rows_data)
            
        ind = ind + 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        pd.set_option("display.max_columns", 200) #Set option to ensure all columns of raw data are displayed
        raw_data(df)

        restart = check_input('\nWould you like to restart?  Enter yes or no.\n', YES_NO)
        
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
