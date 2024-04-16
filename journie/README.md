# CS50 FINAL PROJECT

# JOURNIE: Your month at a glance
#### Video Demo:  https://youtu.be/Nl6OgiDm2VY
#### Description:
My project is a web-based application that allows users to have a "bullet-journal" style glance at the current month.
The main page (index.html) has 5 blocks:
- Calendar,
- Priorities,
- Events,
- Success Journal,
- Habits.

#### Calendar
Calendar on the main page is not interactive, it has weekend highlighted so that it is easier to navigate it.

#### Priorities
This block contains a list of things user would like to focus on during the month. Priorities can be added and
deleted from the list on the main page. Each user can choose not more than 3 priorities (which is reasanable, it
is difficult to keep focus on more than 3 big topics during a month). If they attempt to add the 4th priority,
they will see a flash message yelling at them.

#### Events
This block displays a list of previously added events. To edit the list (to add or delete events) user should
click on the button "Edit events", which will take them to another page (events.html) with a select button for
a day selection and an input line to add a text (event). Once event is added the page reloads and the user can
delete events from the list if needed. The added events are organized in ascending order and the list is displayed
on this page as well as on the main page.

#### Success Journal
This block is for the user to praise themselves for completing tasks, when they feel down looking at this section
can cheer them up and make them remember that they've actually achieved something this month. The block has a list
of previously added completed tasks and a field under the list where they can add an achievement by selecting the
day and tryping in the text.

#### Habits
This section displays a list of habits the user wants to track this month. There is a button under the list of habits
which leads the user to the habit tracker page (habit.html). Habit tracker shows a table with habits and tiles which
represent values (done/not done) for each habit for every day of month. The user can update the completion of their
habits for today. They can update the status of habits for the previous days if needed as well as add and delete habits
from the table.

All of the data is stored in DB.db database which contains 6 tables:
- users (stores user's ids, usernames and hashes for their passwords),
- priorities (stores lists of priorities for each user),
- events (stores lists of events for each user),
- success (stores lists of achievemtns for each user),
- habits_list (connects users with their habit trackers),
- habits (stores the status of each of their habit - done/not done - for every day of the month).

The application iss based on two files - app.py and helpers.py.
App.py contains app.routes for every function of Journie (17 app.routes altogether).
"/login" lets already exisiting user log into the application.
"/logout" lets the use log out from the application and close the session.
"/change" renders the page (change.html), allows the user to change their password and updates the hash in the
DB.db/users and shows a flash message when the password is successfully changed.
"/register" renders the registration page (register.html), asks the new user to provide their username and password
and adds the data to DB.db/users.
"/" displays the main page as described above.
"/deletepr" deletes the priority from the table (DB.db/priorities).
"/addpr" adds the priority to the table (DB.db/priorities).
"/editevents" renders the events page (events.html).
"/addevent" adds the event to the table (DB.db/events).
"/deleteevent" deletes the event from the table (DB.db/events).
"/addsuccess" adds the achievement to the table (DB.db/success).
"/deletesuccess" deletes the achievement from the table (DB.db/success).
"/addhabit" adds the habit to the list of habits (DB.db/habits_list) and updates the log of the newly added habit for the
habit tracker (DB.db/habits). It automatically consideres all the previous days' status "not done", which can later be
updated with app.route("/update").
"/deletehabit" deletes the habit from both tables mentioned above.
"/habit" renders the page with habit tracker (habit.html).
"/done" updates status for the habits for today.
"/update" updates status for the habits for the days before today.

Helpers.py contains the login_required decoration (which
was used for every app.route that required the user to be logged in to access the functionality of the application) and
the apology function (which would create a funny Micheal Scott meme with a face showing that something went wrong).
The appology.html is rendered when the user encounters a problem while trying to log in or register (at register.html)
- wrong password, username already exists, etc. After the user logs in, they can change their password by clicking at
the dedicated button on the right top corner of the main page which leads them to the page (change.html) where they can
type in their old password and their new password (twice).

Styles.css contains the style changes that I have decided to adjust after applying bootstrap classes for the grid of the
main page.

Layout.html used to provide a template for a layout for every page of the application, it contains the top header of the
page with the name of the application as well as the buttons "Change password" and "Log out".
