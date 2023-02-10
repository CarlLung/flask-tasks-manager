from modules.forms.login_form import LoginForm
from modules.forms.command_form import CmdForm
from modules.forms.add_form import AddForm
from modules.forms.register_form import RegisterForm
from functions.functions import *
from flask import render_template, redirect, session, flash, request

#----------Rendering Dashboard------------

def login_form():
# Utilising Flask WTF form
  form = LoginForm()
# Declare variables for error/success messages
  msg_err = ''
  success = ''
# If the user is already logged in, entering this page would be redirected to dashboard page
  if session.get('logged_in'):
    return redirect('/welcome')

# Upon pressing submit button
  if form.validate_on_submit():
# Store values entered in the form
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
# Use check_credentials function in functions.py to check if the form entries matach the data in user.txt
   success, msg_err, isLoggedIn, current_user = check_credentials(username, password, confirm)
# If the data are valid, use flask session to enable viewing of website contents
# By storing necessary information about the log in
   if isLoggedIn:
      session.permanent = True
      session['logged_in'] = True
      session['current_user'] = current_user
# Store log in time to be used for determining if the session has already expired
      session['logged_in_at'] = datetime.now()
# Storing the success/ error message to be rendered
      session['success'] = success
      session['msg_err'] = msg_err
      return redirect('/welcome') 
# If the data is invalid, return error message
   else:
      session.pop('logged_in', None)
      session['msg_err'] = msg_err
      return render_template('login_form.html', form=form)
# If there are errors related to form submisison, return error
  else:
    session.pop('logged_in', None)
    session['msg_err'] = msg_err
    return render_template('login_form.html', form=form)

#----------Rendering Dashboard------------

def welcome():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Get current user from session 
  current_user = session.get('current_user')

# The form for user to enter a command
  form = CmdForm()
# Upon entering command, user would be directed to respective page
# Reviewer can check the which function is used in each functionality in main.py
  if form.validate_on_submit():
   command = form.command.data
   if command.lower() == 'r':
      return redirect('/register')
   elif command.lower() == 'a':
      return redirect('/add_task')
   elif command.lower() == 'va':
      return redirect('/all_tasks')
   elif command.lower() == 'vm':
      return redirect('/my_tasks')
   elif command.lower() == 'e':
      return redirect('/logout')
   elif current_user == 'admin' and command.lower() == 's':
      return redirect('/statistics')
# If user enters the incorrect command, return error
   else:
     msg_err = "Invalid input. Please enter your command according to the options menu."
     session['msg_err'] = msg_err
     return render_template('welcome.html', form=form, current_user=current_user)
# Render the page if passing the check (by not_logged_in and expired_session at the start of this function)
  if not not_login:
   return render_template('welcome.html', form=form, current_user=current_user)

#----------Rendering Add new task------------

def add_task_render():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Get current user from session 
  current_user = session.get('current_user')

# Utilising Flask WTF form
  form = AddForm()

# Call on view_mine function in functions.py to get a dictionary of users
  users_dict = view_mine()
# Upon form submission, store values entered in the form
  if form.validate_on_submit():
   responsible = form.responsible.data
   title = form.title.data
   description = form.description.data
   due = form.due.data
# Use python any method to check if the entered user to be assigned a task exists in user.txt
   user_exists = any(key == responsible for key in users_dict)
# Check if the due date entered is prior to today, return error if this is the case
   invalid_due = form.due.data < datetime.now().date()
   if invalid_due:
     msg_err  = 'You cannot enter a date prior to today.'
     session['msg_err'] = msg_err
     return render_template('add_form.html', form=form, current_user=current_user)
# If the python any method returned false, i.e. entered username does not exist in user.txt, return error
   elif not user_exists:
     msg_err  = 'Cannot find user in our system.'
     session['msg_err'] = msg_err
     return render_template('add_form.html', form=form, current_user=current_user)
# If passing the validations, use try...except... to call on the add_task function (passing in form entries) in functions.py
   else:
     try:
      add_task(responsible, title, description, due)
# Error catching
     except:
      msg_err  = 'An error occured.'
      session['msg_err'] = msg_err
      return render_template('add_form.html', form=form, current_user=current_user)
# If no errors, return a success message
     else: 
      success = 'Add Task Successful.'
      session['success'] = success
     return render_template('add_form.html', form=form, current_user=current_user)
  return render_template('add_form.html', form=form, current_user=current_user)

#----------Rendering All tasks------------

def view_all_render():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Get current user from session 
  current_user = session.get('current_user')

# Call view_all function in functions.py to get the full list of tasks in tasks.txt and render the tasks
  tasks_list = view_all()
  return render_template('all_tasks.html', tasks_list=tasks_list, current_user=current_user)

#----------Rendering All current user's tasks------------

def view_mine_render():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Call view_all function in functions.py to get the full list of tasks in tasks.txt
  tasks_list = view_all()
# Use python filter method to return a new list of tasks with the key equals to the current user's username
  current_user = session.get('current_user')
  my_tasks_list = filter(lambda x: x.responsible == current_user, tasks_list)
# Render page
  return render_template('my_tasks.html', my_tasks_list=my_tasks_list, current_user=current_user)

#----------Rendering New User Registration------------

def reg_user_render():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Utilsing Flask WTF form
  form = RegisterForm()
# Declare boolean variable to be used in conditional checking if the entries submitted by the form are valid
  valid_entries = False
# Get current user from session 
  current_user = session.get('current_user')

# Use conditional on current user to ensure only admin can access this page
  if current_user != 'admin':
   return render_template('unauthorised.html', current_user=current_user)
# Upon form submission, store form inputs into variables
  if form.validate_on_submit():
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
# use try...except to call on register function in functions.py (passing in form entries)
# to check if the extries passes the validation conditions
   try:
    valid_entries, msg_err, success  = reg_user(username, password, confirm)
# Errors catching
   except:
    session['msg_err'] = msg_err
    return render_template('register_form.html', form=form, current_user=current_user)
# Write entries into user.txt if the register function aboves approve the form entries
# and return success message
   else:
     if valid_entries:
      with open ('static/user.txt', 'a') as f_user:
       f_user.write(f"{username}, {password}\n")
       session['success'] = success
      return render_template('register_form.html', form=form, current_user=current_user)
# If the form entries failed to pass the register function check, return error message
     else:
       session['msg_err'] = msg_err
       return render_template('register_form.html', form=form, current_user=current_user)
# Render page
  return render_template('register_form.html', form=form, current_user=current_user)

#----------Rendering Statistics------------

def statistics_render():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Get current user from session 
  current_user = session.get('current_user')

# If the current user is not admin, return unauthorised page
  if current_user != 'admin':
   return render_template('unauthorised.html', current_user=current_user)

# Call on the statistics functions in functions.py to get the numbers required for display statistics
  number_users, number_tasks = statistics()
# Render page
  return render_template('statistics.html', number_users=number_users, number_tasks=number_tasks, current_user=current_user )




#----------Rendering Reports------------

def reports_render():
    
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

# Get current user from session 
  current_user = session.get('current_user')

# If the current user is not admin, return unauthorised page
  if current_user != 'admin':
   return render_template('unauthorised.html', current_user=current_user)

  generate_reports()
  task_data_dict = display_report_task()
  user_data_list = display_report_user()

  return render_template('reports.html', task_data_dict=task_data_dict, user_data_list=user_data_list, current_user=current_user )

#----------Rendering Unauthorised page------------

def unauthorised():
# Call not_logged_in and expired_session in functions,py to check if the user is logged in or not/ or the session expired
# If not logged in or session expired, return to login page with messages
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
# Get current user from session 
  current_user = session.get('current_user')
# Render page
  return render_template('unauthorised.html', current_user=current_user)

#----------Log out functionality------------

def logout():
# When user entered log out command or clicked log out on the side menu
# Clear the logged in information stored in the session and redirect to login page with success message
  session.clear()
  session['success'] = 'You have logged out the system. See you next time!'
  return redirect('/home')



        
        
