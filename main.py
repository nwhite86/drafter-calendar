from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from custom_calendar import *

PROGRAM_NAME = "[Temporary Program Name]"

set_website_title(PROGRAM_NAME)
set_site_information(
    author="Nathaniel White",
    description="Manage custom calendars with Drafter.",
    sources="Drafter docs, some LLM interaction, Forgotten Realms campaign setting.",
    planning=[],
    links=["https://github.com/nwhite86/drafter-calendar"]
)
hide_debug_information()
set_website_framed(False)

# Global Constants
# todo: create dataclass to store time information.
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60

# Helper Functions

def display_month_drafter(year: Year, month: int) -> list:
    """
    Generates the Drafter content used to display a calendar month.

    Creates a calendar table containing weekday headers and individual
    buttons for each day. Each day button navigates to the day_info
    route with the corresponding date as an argument. Leading empty
    spaces are added to align the dates with their correct weekdays.

    Args:
        year (Year): The Year object containing calendar information.
        month (int): The index of the month to display.

    Returns:
        list: A list of Drafter content elements representing the
        calendar month.
    """
    # Useful debug in the console to know what it's supposed to look like
    year.print_month(month)

    # Create empty content list
    content = []
    # This will become the actual table content
    table_content = []
    # This will become the Table's rows argument
    table_rows = []

    # Add title
    content.append(Header(year.get_month_name(month), 3))

    # Add weekday titles
    for weekday in year.weekday_names:
        table_rows.append(weekday[:3])

    dates = [i + 1 for i in range(year.days_per_month[month])]
    whitespace = ["-"] * year.get_weekday(month=month, day=0)

    dates = whitespace + dates

    row = []
    for i, date in enumerate(dates):
        if isinstance(date, int):
            row.append(Button(str(date), "day_info", [Argument("date", date)]))
        else:
            row.append("")

        # If the week ended, wrap around
        if (i + 1) % year.days_per_week == 0:
            table_content.append(row)
            row = []

    content.append(Table(table_content, table_rows))

    return content

def display_month_timeline(year: Year, displayed_month: int):
    """
    Generates navigation controls for moving between calendar months.

    Creates a label displaying the current month and its position
    within the year, along with buttons for navigating to the
    previous or next month when those months exist.

    Args:
        year (Year): The Year object containing calendar information.
        displayed_month (int): The index of the currently displayed month.

    Returns:
        list: A list of Drafter content elements containing the
        month label and navigation controls.
    """
    content = []

    # If there is room to go left, add a button to go left
    if displayed_month != 0:
        content.append(
            Button("<", "increment_month", [Argument("amount", -1)]))
    else:
        content.append("[ < ]")
    # Add a label
    # TODO: Update the fstring for dynamic length
    # Currently it's hardcoded for a length of 2 digits. What if there are 100+ months?
    content.append(f"Change Month ({displayed_month + 1:02d}/{year.months_per_year})")
    # If there is room to go right, add a button to go right
    if displayed_month != year.months_per_year - 1:
        content.append(
            Button(">", "increment_month", [Argument("amount", 1)]))
    else:
        content.append("[ > ]")

    return content

# Drafter routes

@dataclass
class State:
    year: Year
    #current_time: Time
    displayed_month: int


@route
def index(state: State) -> Page:
    """
    Displays the program's landing page.

    Provides navigation options for defining a new calendar or
    loading an existing calendar.

    Args:
        state (State): The current application state.

    Returns:
        Page: The landing page containing the program title and
        calendar navigation buttons.
    """
    return Page(state, [
        "Welcome to ", PROGRAM_NAME, "\n",
        Button("Define Calender", "define_calender"),
        Button("Load Calender", "load_calender")

    ])



@route
def define_calender(state: State) -> Page:
    """
    Displays the calendar creation page.

    This is where users will define a custom calendar system.

    Currently serves as a placeholder for the future calendar
    creation functionality and provides navigation to the main
    calendar page.

    Args:
        state (State): The current application state.

    Returns:
        Page: The calendar creation page.
    """
    return Page(state, [
        "Define New Calender",
        "This is a placeholder until the backend logic is finished",
        Button("Continue to main calender page", "main_page")
    ])


@route
def load_calender(state: State) -> Page:
    """
    Load a preexising calendar.

    Currently serves as a placeholder for the future functionality
    to load an existing calendar and provides navigation to the
    main calendar page.

    Args:
        state (State): The current application state.

    Returns:
        Page: The calendar loading page.
    """
    return Page(state, [
        "This is a placeholder until the backend logic is finished",
        Button("Continue to main calender page", "main_page")
    ])

@route
def day_info(state: State, date: int) -> Page:
    """
    Displays information about a selected calendar day.

    Retrieves the selected day's date string from the current Year
    object and provides an option to add an event to that day.

    Args:
        state (State): The current application state.
        date (int): The day of the month to display.

    Returns:
        Page: A page displaying the selected day's information
        and available actions.
    """
    return Page(state, [
        "DAY INFO\n",
        state.year.get_day_string(state.displayed_month, date),
        "This is a placeholder until the backend logic is finished",
        Button("Add event", "add_event", arguments=[Argument("date", date)]),
        Button("Return to main calender page", "main_page")
    ])

@route
def add_event(state: State, date: int) -> Page:
    """
    Displays the event creation form for a selected calendar day.

    Provides textboxes for entering an event name, start time,
    and end time. The entered information is submitted to the
    save_event route for validation and processing.

    Args:
        state (State): The current application state.
        date (int): The day of the month to which the event
        will be assigned.

    Returns:
        Page: A page containing the event creation form.
    """
    return Page(state, [
        "Event for",
        state.year.get_day_string(state.displayed_month, date), "\n",
        "Event Name: ",
        TextBox("event_name", ""),
        "\n",
        "Event Start Time:",
        TextBox("start_hour", "0", "number"),
        ":",
        TextBox("start_minute", "0", "number"),
        "\n",
        "Event End Time:",
        TextBox("end_hour", "0", "number"),
        ":",
        TextBox("end_minute", "0", "number"),

        "\n",
        Button("Save Event", "save_event", arguments=[Argument("date", date)]),
    ])

@route
def save_event(state: State, date: int, event_name: str,
               start_hour: float, start_minute: float,
               end_hour: float, end_minute: float) -> Page:
    """
    Validates and saves a new calendar event.

    Checks that the provided start and end times contain integer
    values and fall within the valid hours and minutes of a day.
    If validation succeeds, creates a new Event object, adds it
    to the current year's event list, and returns to the selected
    day's information page.

    If validation fails, displays an error message and provides
    an option to return to the event creation form.

    Args:
        state (State): The current application state.
        date (int): The day of the month to which the event
        will be assigned.
        event_name (str): The name of the event.
        start_hour (float): The event's starting hour.
        start_minute (float): The event's starting minute.
        end_hour (float): The event's ending hour.
        end_minute (float): The event's ending minute.

    Returns:
        Page: Either the selected day's information page if the
        event is successfully saved, or an error page if validation
        fails.
    """    # Step 1: Validate the user's input
    # Are the hours and minutes integers?
    try:
        start_hour = int(start_hour)
        start_minute = int(start_minute)

        end_hour = int(end_hour)
        end_minute = int(end_minute)
    except:
        return Page(state, content=[
            "Your times must be integers.", "\n",
            Button("Ok", "add_event", arguments=[Argument("date", date)])
        ])
    # Are the hours and minutes within the day?
    if not ( (HOURS_PER_DAY > start_hour >= 0) and (MINUTES_PER_HOUR > start_minute >= 0)
         and (HOURS_PER_DAY > end_hour >= 0) and (MINUTES_PER_HOUR > end_minute >= 0)):
        return Page(state, content=[
            "Your times must be within the hours and minutes per day.", "\n",
            Button("Ok", "add_event", arguments=[Argument("date", date)])
        ])

    # Step 2: Create new event
    start_time = Time(
        hour = start_hour,
        minute = start_minute,
    )

    end_time = Time(
        hour = end_hour,
        minute = end_minute
    )

    new_event = Event(
        day = date,
        month = state.displayed_month,
        start_time = start_time,
        end_time = end_time
    )

    # Step 3: Update State and return
    state.year.events.append(new_event)

    return day_info(state, date)


@route
def increment_month(state: State, amount: int) -> Page:
    """
    Changes the currently displayed calendar month.

    Updates the displayed_month attribute of the application state
    by the specified amount and returns to the main calendar page.

    Args:
        state (State): The current application state.
        amount (int): The number of months to move forward or
        backward. Positive values move forward, while negative
        values move backward.

    Returns:
        Page: The updated main calendar page.
    """
    #todo: Make sure that the displayed month is within bounds. Perhaps just wrap around.
    state.displayed_month += amount
    return main_page(state)

@route
def main_page(state: State) -> Page:
    """
    Displays the main calendar interface.

    Generates the calendar page header using the current year's
    information, displays the currently selected month, and adds
    navigation controls for changing months.

    Args:
        state (State): The current application state.

    Returns:
        Page: The main calendar page containing the year header,
        monthly calendar, and month navigation controls.
    """

    content = [
        "This is a placeholder until the backend logic is finished\n",
    ]

    header = str(state.year.year_number)
    if state.year.year_name:
        header += (", " + state.year.year_name)

    content.append(Header(header, 2)),

    # Add visual calendar
    content += display_month_drafter(state.year, state.displayed_month)

    content += display_month_timeline(state.year, state.displayed_month)

    return Page(state, content)

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


display_month_drafter(
    year=forgotten_reams_year, month=2)


###################################################################
# Unit Tests

def make_test_year(year_name="Test Year"):
    return Year(
        year_number=2024,
        days_per_year=360,
        months_per_year=12,
        has_leap_day=False,
        days_per_week=10,
        days_per_month=[30] * 12,
        year_name=year_name,
        month_names=[
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ],
        weekday_names=[
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday", "Eighth",
            "Ninth", "Tenth"
        ]
    )


def make_test_state(month=0, day=0):
    return State(
        year=make_test_year(),
        displayed_month=month
    )


# ==========================================
# display_month_drafter()
# ==========================================

year = make_test_year()
result = display_month_drafter(year, 0)

# Test 1: Correct month header
assert assert_equal(result[0], Header("January", 3))

# Test 2: Correct weekday headers
expected_headers = [
    "Mon", "Tue", "Wed", "Thu", "Fri",
    "Sat", "Sun", "Eig", "Nin", "Ten"
]
assert assert_equal(result[1].header, expected_headers)


# ==========================================
# display_month_timeline()
# ==========================================

year = make_test_year()

# Test 1: First month has no previous button
result = display_month_timeline(year, 0)

assert assert_equal(result[0], "[ < ]")
assert assert_equal(result[1], "Change Month (01/12)")

# Test 2: Middle month has both navigation buttons
result = display_month_timeline(year, 5)

assert assert_equal(
    result[0],
    Button("<", "increment_month", [Argument("amount", -1)])
)
assert assert_equal(
    result[2],
    Button(">", "increment_month", [Argument("amount", 1)])
)

# Test 3: Last month has no next button
result = display_month_timeline(year, 11)

assert assert_equal(result[1], "Change Month (12/12)")
assert assert_equal(result[2], "[ > ]")


# ==========================================
# index()
# ==========================================

state = make_test_state()
result = index(state)

# Test 1: Welcome message
assert assert_equal(result.content[0], "Welcome to ")

# Test 2: Define calendar button
assert assert_equal(
    result.content[3],
    Button("Define Calender", "define_calender")
)

# Test 3: Load calendar button
assert assert_equal(
    result.content[4],
    Button("Load Calender", "load_calender")
)


# ==========================================
# define_calender()
# ==========================================

state = make_test_state()
result = define_calender(state)

# Test 1: Correct page title
assert assert_equal(result.content[0], "Define New Calender")

# Test 2: Placeholder message
assert assert_equal(
    result.content[1],
    "This is a placeholder until the backend logic is finished"
)

# Test 3: Navigation button
assert assert_equal(
    result.content[2],
    Button("Continue to main calender page", "main_page")
)


# ==========================================
# load_calender()
# ==========================================

state = make_test_state()
result = load_calender(state)

# Test 1: Placeholder message
assert_equal(
    result.content[0],
    "This is a placeholder until the backend logic is finished"
)

# Test 2: Navigation button
assert_equal(
    result.content[1],
    Button("Continue to main calender page", "main_page")
)

# Test 3: State remains unchanged
assert_equal(result.state, state)


# ==========================================
# day_info()
# ==========================================

state = make_test_state()
result = day_info(state, 5)

# Test 1: Correct page title
assert_equal(result.content[0], "DAY INFO\n")

# Test 2: Correct date information
assert_equal(
    result.content[1],
    state.year.get_day_string(0, 5)
)

# Test 3: Add event button contains correct date
assert_equal(
    result.content[3],
    Button("Add event", "add_event",
           arguments=[Argument("date", 5)])
)


# ==========================================
# add_event()
# ==========================================

state = make_test_state()
result = add_event(state, 10)

# Test 1: Correct date displayed
assert_equal(
    result.content[1],
    state.year.get_day_string(0, 10)
)

# Test 2: Event name textbox
assert_equal(result.content[4], TextBox("event_name", ""))

# Test 3: Save button contains correct date
assert_equal(
    result.content[-1],
    Button("Save Event", "save_event",
           arguments=[Argument("date", 10)])
)


# ==========================================
# save_event()
# ==========================================

state = make_test_state()

# Test 1: Reject non-integer time input
result = save_event(
    state, 5, "Meeting",
    "abc", "30", "10", "30"
)

assert_equal(
    result.content[0],
    "Your times must be integers."
)
assert_equal(len(state.year.events), 0)


# Test 2: Reject invalid time ranges
state = make_test_state()

result = save_event(
    state, 5, "Meeting",
    "10", "60", "11", "30"
)

assert_equal(
    result.content[0],
    "Your times must be within the hours and minutes per day."
)
assert_equal(len(state.year.events), 0)


# Test 3: Successfully create an event
state = make_test_state()

result = save_event(
    state, 5, "Meeting",
    "9", "30", "10", "45"
)

expected_event = Event(
    day=5,
    month=0,
    start_time=Time(hour=9, minute=30),
    end_time=Time(hour=10, minute=45)
)

assert_equal(len(state.year.events), 1)
assert_equal(state.year.events[0], expected_event)
assert_equal(result.content[0], "DAY INFO\n")


# ==========================================
# increment_month()
# ==========================================

# Test 1: Increment month
state = make_test_state(month=0)
result = increment_month(state, 1)

assert_equal(state.displayed_month, 1)

# Test 2: Decrement month
state = make_test_state(month=5)
result = increment_month(state, -1)

assert_equal(state.displayed_month, 4)

# Test 3: Increment by zero
state = make_test_state(month=7)
result = increment_month(state, 0)

assert_equal(state.displayed_month, 7)


# ==========================================
# main_page()
# ==========================================

# Test 1: Year header with year name
state = make_test_state()
result = main_page(state)

assert_equal(
    result.content[1],
    Header("2024, Test Year", 2)
)

# Test 2: Year header without year name
state = make_test_state()
state.year.year_name = ""

result = main_page(state)

assert_equal(
    result.content[1],
    Header("2024", 2)
)

# Test 3: Correct month displayed
state = make_test_state(month=5)
result = main_page(state)

assert_equal(
    result.content[2],
    Header("June", 3)
)


print("All tests completed!")


#start_server(State(year=forgotten_reams_year, displayed_month=0))
