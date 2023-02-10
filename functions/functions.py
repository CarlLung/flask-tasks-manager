from datetime import datetime
from flask import session
import pytz
import re
import uuid

# Create a class for task objects, containing the necessary info required in a task
# The objects formed by this class would have defauly values for
# 1 - id (with value generated by uuid) module
# 2 - created date (set as today's day)
# 3 - completed set as 'No'
# The following info are to be filled by values entered by the new task adding form
# - title, responsible (user assigned), description, due (Due date)

class Task:
   def __init__(self, responsible, title, description, due, id = uuid.uuid4(), created_date = datetime.today().strftime('%-d %b %Y'), completed = 'No'):
       self.id = id
       self.responsible = responsible
       self.title = title
       self.description = description
       self.due = due
       self.created_date = created_date
       self.completed = completed
    
   def mark_as_completed(self):
       self.completer = 'Yes'
   
   def edit_task(self, name, due_date):
       self.responsible = name
       self.due = due_date

   def __repr__(self):
        return f"{self.completed}"
   

#----------Function for turning the data in user.txt ------------
#-----into a dictionary with key: username, value: password -----

# Using split by ', ', and then putting the items in the returned array into a dictionary

def view_mine():
 users_dict = {}
 with open ('static/user.txt', 'r') as f_user:
    for line in f_user:
      split = line.split(', ')
      users_dict.update({split[0] : split[1].replace('\n', '')})
 return users_dict

#----------Function for checking credentials in the login form ------------

# Form entries would be passed in as arguments
def check_credentials(name, pw, pw2):
# use view_mine function to get the dictionary of all users
     users_dict = view_mine()
# Declare variables for error/ success message
     msg_err = ''
     success = ''
# Declare boolean variable for indicating status of login
     isLoggedIn = False
# Declare variable to be stored in the session as logged in information
     current_user = ''
# If the confirm password does not match the first password, return error
     if pw != pw2:
       msg_err = 'Second password entry does not match first password entry.'
# Check the entered username, if it exists as a key in the users dictionary
# Also checking if the password matches the password value for the respective key in the dictionary
# If matches both, indicate login success by the boolean variable isLoggedIn
     else:
      if name in users_dict.keys():
        if pw == users_dict[name] and pw == pw2:
           current_user = name
           success = 'Login successful.'
           isLoggedIn = True
# If the credentials does not match the two conditions, return error
        else:    
          msg_err = 'Incorrect credentials. Please enter again.'
          isLoggedIn = False
      else:
        msg_err = 'Incorrect credentials. Please enter again.'
        isLoggedIn = False
# Return the variables that now stored the username and login status(if success), and the messages
# The variables would be returned to the login_form function in routes.py for rendering purpose
     return success, msg_err, isLoggedIn, current_user

#----------Function for setting session to be expired------------

def expired_session():
  expired = False
# If there are log in information in the session
# Check if 5 mins is already passed after log in
# If yes, clear the log in session and return a bollean variable - expired as an indicator
  if 'logged_in_at' in session:
    session['logged_in_at'] = pytz.utc.localize(session['logged_in_at'].replace(tzinfo=None))
    elapsed_time = datetime.now(pytz.utc) - session['logged_in_at']

    if elapsed_time.seconds > 5 * 60: 
      session.clear()
      expired = True
  return expired

#----------Function for checking if user is logged in or not by accessing the session------------

def not_logged_in():
  not_login = False
  if session.get('logged_in') == None:
    not_login = True
  return not_login

#----------Function for writing new task into the tasks.txt------------

# Form entries would be passed in as arguments
def add_task(responsible, title, description, due):
# Ensuring ', ' does not exists in the description, otherwise when reading the tasks.txt
# the info could not be extracted properly, as we are using split by ', ' to extract the information
  description = description.replace(', ', ',')
  print(description)
# Casting the correct type (string) and format to the form entry of due date
  due = due.strftime('%-d %b %Y')
# Pass the form entries into the class Task to give an object
  task = Task(responsible, title, description, due)
# Using the object's keys and turn them into a single string
# Write the string into a new line in the tasks.txt file
  with open ('static/tasks.txt', 'a') as f_task:
   f_task.write(f"{task.id}, {task.responsible}, {task.title}, {task.description}, {task.due}, {task.created_date}, {task.completed}\n")

#----------Function for turning the data in tasks.txt ------------
#-----------------into a list of task objects --------------------

def view_all():
# Declare variable to store the list
  tasks_list = []
# Read the lines in tasks.txt, turn the info into items inside a list using split by ', '
  with open ('static/tasks.txt', 'r') as f_task:
   for line in f_task:
    split = line.split(', ')
# Form a task objects by the class Task by passing the items inside the list in to the class
    task = Task(split[1], split[2], split[3], split[4], split[0], split[5], split[6].replace('\n', ''))
# For each task, append it to the list
# when the for loop is finished, the list will contain all information in the tasks.txt
# in the form of a list of task objects
    tasks_list.append(task)
  return tasks_list

#----------Function for password validation------------
#----------------by utilising RegEx--------------------

def pw_valid(pw):
  pw_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#%?&+-_^=])[A-Za-z\d@$!%+#-_%^=*?&]{8,}$")
  return re.match(pw_pattern, pw) is not None

#----------Function for username validation------------
#----------------by utilising RegEx--------------------

def name_valid(name):
  name_pattern = re.compile(r"^[\w\d\._]{8,20}$")
  return re.match(name_pattern, name) is not None

#----------Function for checking validity of form entries------------
#---------------for the new user registration form-------------------

# Form entries would be passed as arguments
def reg_user(name, pw, pw2):
# get the dictionary of all users from user.txt
  users_dict = view_mine()
# boolean variable indicating if the new username already existed or not
# by using python any method, checking if the username entry matches any keys inside the dictionary 
  duplicate_name = any(key == name for key in users_dict)
# Declare variables to be returned to routes.py for rendering
  valid_entries = False
  success = ''
  msg_err = ''
# Call on name_valid function above to validate on the username format
  valid_name = name_valid(name) 
# Return error if username format does not meet format requirements
  if not valid_name:
    msg_err  = 'Name must be 8-20 characters long, contain only alphanumeric characters, dot or underscore.'
# Return error if the name is already existing
  elif duplicate_name:
    msg_err  = 'Username is taken. Try another one.'
# Return error if the confirmation password does not match the first password entry
  elif pw != pw2:
    msg_err  = 'Second password entry does not match first password entry.'
# Call on pw_valid function above to validate on the password format
  else:
    valid_pw = pw_valid(pw)
# Set boolean variable as true to indicate passing of all validations
# also set the success message to be displayed
    if valid_pw:
     valid_entries = True
     success = 'New user succesfully registered.'
# Return error if password format does not meet format requirements
    else:
     msg_err  = 'Password must contain minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.'
# Return validity indicator (boolean variable) and message to be used in rendering registration page (routes.py)
  return valid_entries, msg_err, success

#----------Function for getting statistics numbers------------
def statistics():
# Get a dictionary of all data from user.txt
  users_dict = view_mine()
# Get the length of the dictionary as the total number of all users
  number_users = len(users_dict)
# Get a list of all data from user.txt
  tasks_list = view_all()
# Get the length of the list as the total number of all tasks
  number_tasks = len(tasks_list)
# Return the variables to routes.py for rendering by statistics_render function
  return number_users, number_tasks 

#----------Function for determining if the task isoverdue-----------

def overdue(due_date_str):
  due_date = datetime.strptime(due_date_str, '%d %b %Y').date()
  is_due = due_date < datetime.now().date()
  return is_due

#----------Function for generating reports------------

def generate_reports():
    tasks_list = view_all()
    with open ('static/task_overview.txt', 'w') as f_report_task:

      completed_tasks_list = list(filter(lambda x: x.completed == 'Yes', tasks_list))
      incompleted_tasks_list = list(filter(lambda x: x.completed == 'No', tasks_list))
      overdue_incompleted_tasks_list = list(filter(lambda x: overdue(x.due), incompleted_tasks_list))
      
      total_tasks_number = len(tasks_list)
      number_completed = len(completed_tasks_list)
      number_incompleted = len(incompleted_tasks_list)
      number_overdue = len(overdue_incompleted_tasks_list)

      incompleted_percent = round((number_incompleted / total_tasks_number) * 100, 2)
      overdue_percent = round((number_overdue / total_tasks_number) * 100, 2)
      
      f_report_task.write(f'{total_tasks_number}, {number_completed}, {number_incompleted}, {number_overdue}, {incompleted_percent}, {overdue_percent}')

    with open ('static/user_overview.txt', 'w') as f_report_user:
      users_dict = view_mine()

      for user in users_dict:
        username = user
        user_tasks_list = list(filter(lambda x: x.responsible == user, tasks_list))

        number_user_tasks = len(user_tasks_list)

        user_completed_list = list(filter(lambda x: x.completed == 'Yes', user_tasks_list))
        user_incompleted_list = list(filter(lambda x: x.completed == 'No', user_tasks_list))
        user_overdue_list = list(filter(lambda x: overdue(x.due), user_tasks_list))

        user_tasks_percent = number_user_tasks / len(tasks_list)
        user_completed_percent = len(user_completed_list) / len(user_tasks_list)
        user_incompleted_percent = len(user_incompleted_list) / len(user_tasks_list)
        user_overdue_percent = len(user_overdue_list) / len(user_tasks_list)

        f_report_user.write(f'{username}, {number_user_tasks}, {user_tasks_percent}, {user_completed_percent}, {user_incompleted_percent}, {user_overdue_percent}\n')

#----------Function for reading task report------------

def display_report_task():

    with open ('static/task_overview.txt', 'r') as f_read_report_task:
      
      for line in f_read_report_task:
        task_report_split = line.split(', ')
        total_tasks_number = task_report_split[0]
        number_completed = task_report_split[1]
        number_incompleted = task_report_split[2]
        number_overdue = task_report_split[3]
        incompleted_percent = task_report_split[4]
        overdue_percent = task_report_split[5]
    
    task_data_dict = {'total_tasks_number': total_tasks_number, 'number_completed': number_completed, 'number_incompleted': number_incompleted, 'number_overdue': number_overdue, 'incompleted_percent': incompleted_percent, 'overdue_percent': overdue_percent}

    return task_data_dict

#----------Function for reading user report------------

def display_report_user():
   
   user_data_list = []

   with open ('static/user_overview.txt', 'w') as f_read_report_user:
      
    for line in f_read_report_user:
      user_report_split = line.split(', ')
      username = user_report_split[0]
      number_user_tasks = user_report_split[1]
      user_tasks_percent = user_report_split[2]
      user_completed_percent = user_report_split[3]
      user_incompleted_percent = user_report_split[4]
      user_overdue_percent = user_report_split[5].replace('\n', '')
      
      user_data_obj = {'username': username, 'number_user_tasks': number_user_tasks, 'user_tasks_percent': user_tasks_percent, 'user_completed_percent': user_completed_percent, 'user_incompleted_percent': user_incompleted_percent, 'user_overdue_percent': user_overdue_percent}

      user_data_list.append(user_data_obj)
    
   return user_data_list