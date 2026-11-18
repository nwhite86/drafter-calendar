from custom_calendar import *
from main import *

#region main.py unit tests
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

year_test = make_test_year()
result = display_month_drafter(year_test, 0)

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

year_test = make_test_year()

# Test 1: First month has no previous button
result = display_month_timeline(year_test, 0)

assert assert_equal(result[0], "[ < ]")
assert assert_equal(result[1], "Change Month (01/12)")

# Test 2: Middle month has both navigation buttons
result = display_month_timeline(year_test, 5)

assert assert_equal(
    result[0],
    Button("<", "increment_month", [Argument("amount", -1)])
)
assert assert_equal(
    result[2],
    Button(">", "increment_month", [Argument("amount", 1)])
)

# Test 3: Last month has no next button
result = display_month_timeline(year_test, 11)

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

##############################################
#endregion

#region custom_calendar.py unit tests
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
#endregion