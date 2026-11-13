from dataclasses import dataclass, field
from bakery import assert_equal

@dataclass
class Time:
    """A time of day, with hours and minutes
    fields::
        hour: int - between 0 and [length of day] in hours. 
        minute: int - between 0 and [length of hour] in minutes
    """
    hour: int = 0
    minute: int = 0
    
    def print_time(self):
        """
        Prints the time in hours and minutes.

        Displays the hour followed by the minute, with the minute
        padded to two digits when necessary.

        Returns:
            None
        """
        print(f"{self.hour}:{self.minute:02d}")

@dataclass
class Event:
    """
    Represents an event occurring on a particular calendar date.

    Attributes:
        day (int): The day of the month on which the event occurs.
        month (int): The index of the month in which the event occurs.
        start_time (Time): The time at which the event begins.
        end_time (Time): The time at which the event ends.
    """
    day: int
    month: int
    start_time: Time
    end_time: Time

@dataclass
class Year:
    """
    Represents a customizable calendar year.

    Stores information about the structure, naming conventions,
    and calendar rules of a year. Supports customizable month
    lengths, weekday lengths, leap-year rules, floating days,
    and calendar events.

    Attributes:
        year_number (int): The numerical identifier of the year. (Current year)
        days_per_year (int): The number of regular days in the year,
            excluding floating days.
            1-indexed
        months_per_year (int): The number of months in the year.
            0-indexed

        has_leap_day (bool): Whether the calendar supports leap days.
        has_floating_leap_day (bool): Whether leap days are treated
            as floating days.
        years_per_leap (int): The number of years between leap years.
        leap_day (int): The position of the leap day in the year.
        has_centry_rule (bool): Whether the century leap-year rule
            is applied.
        years_per_century (int): The number of years in a century.

        days_per_week (int): The number of days in a week.
        days_per_month (list[int]): The number of days in each month.

        floating_days (dict): A dictionary containing floating days,
            indexed by their position relative to a month and day.
        events (list[Event]): A collection of events belonging to
            the calendar year.

        year_name (str): The custom name of the year.
        month_names (list[str]): The names of the months.
        weekday_names (list[str]): The names of the weekdays.

    Notes:
        The calendar assumes that the first day of year 1 is the
        first day of the week. Weekday calculations are based on
        this assumption.
    """

    #TODO:
    # Floating days implementation
    # events implementation


    year_number: int = 2026

    # days_per_year can not include floating days
    days_per_year: int = 365
    months_per_year: int = 12

    # Leap Day Rules
    has_leap_day: bool = True
    has_floating_leap_day: bool = False
    #
    years_per_leap: int = 4
    leap_day: int = 60
    #
    # The century rule is a funny little rule that says that leap years don't apply on
    # years that are multiples of 100, unless they're also multiples of 400
    has_centry_rule: bool = False
    years_per_century: int = 100
    #

    #Important day of week note: This calander program assumes that the first day of year 1 is the first day of the week.
    #This is used to calculate the day of the week.

    #For the defualt settings, 1 is a Monday.

    days_per_week: int = 7
    days_per_month: list[int] = field(default_factory=lambda: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    floating_days: dict = field(default_factory=dict)
    """
    floating_days format:
    {
        tuple: str
            (the month that the floating day is before / within, the day that the floating day before): "Name" 
    }
    """

    events: list[Event] = field(default_factory=lambda: [])

    # Custom Names
    year_name: str = "[DEFAULT YEAR NAME]"
    month_names: list[str]= field(default_factory=lambda: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    weekday_names: list[str] = field(default_factory=lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])




    # Custom Name Functions
    def get_weekday_name(self, weekday: int) -> str:
        """
        Retrieves the name of a weekday using its numerical index.

        Args:
            weekday (int): The zero-indexed position of the weekday.

        Returns:
            str: The name of the specified weekday.
        """
        return self.weekday_names[weekday]

    def get_month_name(self, month: int) -> str:
        """
        Retrieves the name of a month using its numerical index.

        Args:
            month (int): The zero-indexed position of the month.

        Returns:
            str: The name of the specified month.
        """
        return self.month_names[month]


    # Calander Logic Functions

    def get_weekday(self, month: int, day: int) -> int:
        """
        Calculates the weekday corresponding to a given date.

        Determines the weekday by accounting for the number of days
        in previous months, the starting weekday of the year, and
        any applicable leap-year adjustments.

        Args:
            month (int): The zero-indexed month of the date.
            day (int): The zero-indexed day within the month.

        Returns:
            int: The zero-indexed weekday corresponding to the date.

        Notes:
            The first day of year 1 is assumed to be the first day
            of the week. Leap-year and century rules are applied
            according to the calendar's configuration.
        """
        first_weekday_of_year = ((self.year_number - 1) * self.days_per_year) % self.days_per_week
        day_of_year = sum(self.days_per_month[:month]) + day
        # Step 1: Account for leap day in current year

        if self.has_leap_day and not self.has_floating_leap_day:
            # If it's a leap year
            is_leap_year = self.year_number % self.years_per_leap == 0
            # If the century rule applies and it's not a century leap year, update is_leap_year
            if self.has_centry_rule and is_leap_year:
                # If it is NOT a century leap year (the year is divisible by 400)
                if self.year_number % (self.years_per_leap * self.years_per_century) != 0:
                    is_leap_year = False
            if is_leap_year and day_of_year > self.leap_day:
                day_of_year += 1

            # Step 2: Find the offset in they day of the week from previous leap years
            leap_year_offset = (self.year_number - 1) // self.years_per_leap
            # If there's a centry rule, remove leap days for every year affected
            if self.has_centry_rule:
                leap_year_offset -= (self.year_number - 1) // self.years_per_century - (self.year_number - 1) // (self.years_per_leap  * self.years_per_century)

            day_of_year += leap_year_offset
        # Step 3: Use day_of_year + leap_year_offset % days_per_week to get the current day of the week
        # I need this -1 because days_per_week is 1 indexed, but everything else has been 0 indexed
        #                                                                           \/
        day_of_week = (day_of_year + first_weekday_of_year) % (self.days_per_week)

        return day_of_week



    # Displaying Calander
    def print_month(self, month: int):
        """
        Prints a formatted calendar representation of a month.

        Displays the month name, year number, weekday headers,
        and numbered dates. Dates are aligned with their
        corresponding weekdays using leading whitespace.

        Args:
            month (int): The zero-indexed month to display.

        Returns:
            None

        Notes:
            Floating days are not currently included in the output.
        """
        # todo:
        #  Figure out how to display floating months

        # Step 1: Printing the month
        # Print Title
        print(f"\t\t{self.get_month_name(month)}, {self.year_number}")

        # Print weekdays
        for weekday in self.weekday_names:
            print(weekday[:3], "\t", sep="", end="")
        print()

        dates = [ i + 1 for i in range(self.days_per_month[month]) ]
        whitespace = ["-"] * self.get_weekday(month=month, day=0)

        dates = whitespace + dates

        for i, date in enumerate(dates):
            print(date, "\t", sep="", end="")
            if (i + 1) % self.days_per_week == 0:
                print()
        print()

        # Step 2: Printing any floating days

    def get_day_string(self, month: int, day: int) -> str:
        """
        Generates a formatted string describing a calendar date.

        Example: 'Sunday, May 3'

        Combines the weekday name, month name, and day number
        into a human-readable date representation.

        Args:
            month (int): The zero-indexed month of the date.
            day (int): The one-indexed day of the month.

        Returns:
            str: A formatted date string containing the weekday,
            month, and day.
        """
        return f"{self.get_weekday_name(self.get_weekday(month, day) - 1)}, {self.get_month_name(month)} {day} \n"

            

fd  = {
    (10, 11): "Nathaniel's Favorite Day"
}
#test_year = Year(has_centry_rule=True, floating_days=fd)

#print(test_year)

#test_year.print_month(10)

forgotten_realms_months = [
    "Hammer",
    "Alturiak",
    "Ches",
    "Tarsakh",
    "Mirtul",
    "Kythorn",
    "Flamerule",
    "Eleasis",
    "Eleint",
    "Marpenoth",
    "Uktar",
    "Nightal",
]

forgotten_reams_year = Year(
    year_number=1492,
    days_per_year=360,
    months_per_year=12,

    has_leap_day=False,

    days_per_week=10,
    days_per_month=([30] * 12),

    year_name="Year of the Seven Ships Sailing",
    month_names=forgotten_realms_months,
    weekday_names=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
)

#############################################################
# Unit tests:

# ==========================================
# Testing Time
# ==========================================

assert_equal(Time(0, 0), Time(0, 0))
assert_equal(Time(12, 30), Time(12, 30))
assert_equal(Time(23, 59), Time(23, 59))


# ==========================================
# Testing Event
# ==========================================

assert_equal(Event(1, 0, Time(9, 0), Time(10, 0)),
             Event(1, 0, Time(9, 0), Time(10, 0)))

assert_equal(Event(5, 2, Time(12, 0), Time(13, 0)).day, 5)
assert_equal(Event(5, 2, Time(12, 0), Time(13, 0)).month, 2)


# ==========================================
# Testing Year Initialization
# ==========================================

assert_equal(forgotten_reams_year.year_number, 1492)
assert_equal(forgotten_reams_year.days_per_year, 360)
assert_equal(forgotten_reams_year.months_per_year, 12)


# ==========================================
# Testing get_weekday_name()
# ==========================================

assert_equal(forgotten_reams_year.get_weekday_name(0), "1st")
assert_equal(forgotten_reams_year.get_weekday_name(4), "5th")
assert_equal(forgotten_reams_year.get_weekday_name(9), "10th")


# ==========================================
# Testing get_month_name()
# ==========================================

assert_equal(forgotten_reams_year.get_month_name(0), "Hammer")
assert_equal(forgotten_reams_year.get_month_name(5), "Kythorn")
assert_equal(forgotten_reams_year.get_month_name(11), "Nightal")


# ==========================================
# Testing get_weekday()
# ==========================================

assert_equal(forgotten_reams_year.get_weekday(0, 0), 0)
assert_equal(forgotten_reams_year.get_weekday(0, 1), 1)
assert_equal(forgotten_reams_year.get_weekday(1, 0), 0)
assert_equal(forgotten_reams_year.get_weekday(11, 29), 9)


# ==========================================
# Testing get_day_string()
# ==========================================

assert_equal(forgotten_reams_year.get_day_string(0, 1),"1st, Hammer 1 \n")

assert_equal(forgotten_reams_year.get_day_string(0, 2),"2nd, Hammer 2 \n")

assert_equal(forgotten_reams_year.get_day_string(1, 1),"1st, Alturiak 1 \n")


# ==========================================
# Testing print_month()
# ==========================================

# These tests check that the method executes without errors.
# Visual output can be inspected in the console.

forgotten_reams_year.print_month(0)
forgotten_reams_year.print_month(5)
forgotten_reams_year.print_month(11)


print("Testing complete!")
