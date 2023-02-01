from datetime import datetime
from flask import session
import pytz

current_user = ''
users_dict = {}
tasks_list =[]

class Task:
   def __init__(self, responsible, title, description, due, created_date = datetime.today().strftime('%-d %b %Y'), completed = 'No'):
       self.responsible = responsible
       self.title = title
       self.description = description
       self.due = due
       self.created_date = created_date
       self.completed = completed

def get_users():
 users_dict = {}
 with open ('static/user.txt', 'r') as f_user:
    for line in f_user:
      split = line.split(', ')
      users_dict.update({split[0] : split[1].replace('\n', '')})
 return users_dict

def check_credentials(name, pw, pw2):
     users_dict = get_users()
     message = ''
     isLoggedIn = False
     current_user = ''
     if pw != pw2:
       message = 'Second password entry does not match first password entry.'
     else:
      if name in users_dict.keys():
        if pw == users_dict[name] and pw == pw2:
          current_user = name
          message = 'Login successful.'
          isLoggedIn = True
        else:    
          message = 'Incorrect credentials. Please enter again.'
          isLoggedIn = False
      else:
        message = 'Incorrect credentials. Please enter again.'
        isLoggedIn = False
     return message, isLoggedIn, current_user

def expired_session():
  expired = False
  if 'logged_in_at' in session:
    session['logged_in_at'] = pytz.utc.localize(session['logged_in_at'].replace(tzinfo=None))
    elapsed_time = datetime.now(pytz.utc) - session['logged_in_at']

    if elapsed_time.seconds > 30 * 60: 
      session.clear()
      expired = True
  return expired

def not_logged_in():
  not_login = False
  if session.get('logged_in') == None:
    not_login = True
  return not_login

def add_task(responsible, title, description, due):
  description.replace(', ', ',')
  due = due.strftime('%-d %b %Y')
  task = Task(responsible, title, description, due)
  with open ('static/tasks.txt', 'a') as f_task:
   f_task.write(f"{task.responsible}, {task.title}, {task.description}, {task.due}, {task.created_date}, {task.completed}\n")

def get_tasks():
  tasks_list = []
  with open ('static/tasks.txt', 'r') as f_task:
   for line in f_task:
    split = line.split(', ')
    task = Task(split[0], split[1], split[2], split[4], split[3], split[5].replace('\n', ''))
    tasks_list.append(task)
  return tasks_list

def register(name, pw, pw2):
  users_dict = get_users()
  duplicate_name = any(key == name for key in users_dict)
  valid_entries = False
  if pw != pw2:
    message = 'Second password entry does not match first password entry.'
  elif duplicate_name:
    message = 'Username is taken. Try another one.'
  else:
    valid_entries = True
    message = 'New user succesfully registered.'
  return valid_entries, message

def statistics():
  users_dict = get_users()
  number_users = len(users_dict)
  tasks_list = get_tasks()
  number_tasks = len(tasks_list)
  return number_users, number_tasks 

