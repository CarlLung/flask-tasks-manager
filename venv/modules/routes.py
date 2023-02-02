from modules.forms.login_form import LoginForm
from modules.forms.command_form import CmdForm
from modules.forms.add_form import AddForm
from modules.forms.register_form import RegisterForm
from modules.functions import *
from flask import render_template, redirect, session, flash


def login_form():
  form = LoginForm()
  msg_err = ''
  success = ''
  if session.get('logged_in'):
    return redirect('/welcome')
  if form.validate_on_submit():
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
   success, msg_err, isLoggedIn, current_user = check_credentials(username, password, confirm)
   if isLoggedIn:
      session.permanent = True
      session['logged_in'] = True
      session['logged_in_at'] = datetime.now()
      session['current_user'] = current_user
      session['success'] = success
      session['msg_err'] = msg_err
      return redirect('/welcome') 
   else:
      session.pop('logged_in', None)
      session['msg_err'] = msg_err
      return render_template('login_form.html', form=form)
  else:
    session.pop('logged_in', None)
    session['msg_err'] = msg_err
    return render_template('login_form.html', form=form)

def welcome():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user')

  form = CmdForm()
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
   else:
     msg_err = "Invalid input. Please enter your command according to the options menu."
     session['msg_err'] = msg_err
     return render_template('/welcome', form=form, current_user=current_user)

  if not not_login:
   return render_template('welcome.html', form=form, current_user=current_user)

def add_task_render():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

  current_user = session.get('current_user')

  form = AddForm()
  users_dict = get_users()
  if form.validate_on_submit():
   responsible = form.responsible.data
   title = form.title.data
   description = form.description.data
   due = form.due.data

   user_exists = any(key == responsible for key in users_dict)
   invalid_due = form.due.data < datetime.now().date()
   
   if invalid_due:
     msg_err  = 'You cannot enter a date prior to today.'
     session['msg_err'] = msg_err
     return render_template('add_form.html', form=form, current_user=current_user)
   elif not user_exists:
     msg_err  = 'Cannot find user in our system.'
     session['msg_err'] = msg_err
     return render_template('add_form.html', form=form, current_user=current_user)
   else:
     try:
      add_task(responsible, title, description, due)
     except:
      msg_err  = 'An error occured.'
      session['msg_err'] = msg_err
      return render_template('add_form.html', form=form, current_user=current_user)
     else: 
      success = 'Add Task Successful.'
      session['success'] = success
     return render_template('add_form.html', form=form, current_user=current_user)
  return render_template('add_form.html', form=form, current_user=current_user)

def all_tasks_render():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

  current_user = session.get('current_user')

  tasks_list = get_tasks()
  return render_template('all_tasks.html', tasks_list=tasks_list, current_user=current_user)

def my_tasks_render():
  
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user')

  tasks_list = get_tasks()
  current_user = session.get('current_user')
  my_tasks_list = filter(lambda x: x.responsible == current_user, tasks_list)
  return render_template('my_tasks.html', my_tasks_list=my_tasks_list, current_user=current_user)

def register_form():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user') 

  form = RegisterForm()
  valid_entries = False
  current_user = session.get('current_user')
  if current_user != 'admin':
   return render_template('unauthorised.html', current_user=current_user)
  if form.validate_on_submit():
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
   try:
    valid_entries, msg_err, success  = register(username, password, confirm)
   except:
    session['msg_err'] = msg_err
    return render_template('register_form.html', form=form, current_user=current_user)
   else:
     if valid_entries:
      with open ('static/user.txt', 'a') as f_user:
       f_user.write(f"{username}, {password}\n")
       session['success'] = success
      return render_template('register_form.html', form=form, current_user=current_user)
     else:
       session['msg_err'] = msg_err
       return render_template('register_form.html', form=form, current_user=current_user)
  return render_template('register_form.html', form=form, current_user=current_user)

def statistics_render():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user')

  number_users, number_tasks = statistics()
  return render_template('statistics.html', number_users=number_users, number_tasks=number_tasks, current_user=current_user )

def unauthorised():
  not_login = not_logged_in()
  if not_login:
    flash("Content only available for logged in users.")
    return redirect('/home')

  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user')

  return render_template('unauthorised.html', current_user=current_user)

def logout():
  session.clear()
  session['success'] = 'You have logged out the system. See you next time!'
  return redirect('/home')



        
        
