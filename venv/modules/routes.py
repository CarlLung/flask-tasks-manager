from modules.forms.login_form import LoginForm
from modules.forms.add_form import AddForm
from modules.forms.register_form import RegisterForm
from modules.functions import *
from flask import render_template, redirect, session, flash


def login_form():
  form = LoginForm()
  message = ''
  if session.get('logged_in'):
    return redirect('/welcome')
  if form.validate_on_submit():
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
   message, isLoggedIn, current_user = check_credentials(username, password, confirm)
   if isLoggedIn:
      session.permanent = True
      session['logged_in'] = True
      session['logged_in_at'] = datetime.now()
      session['current_user'] = current_user
      return redirect('/welcome') 
   else:
      session.pop('logged_in', None)
      return render_template('login_form.html', form=form, message=message)
  else:
    session.pop('logged_in', None)
    return render_template('login_form.html', form=form, message=message)



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

  if not not_login:
   return render_template('welcome.html', current_user=current_user)

def add_task_render():
  not_login = not_logged_in()
  if not_login == True:
    flash("Content only available for logged in users.")
    return redirect('/home')
  
  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')

  current_user = session.get('current_user')

  form = AddForm()
  message= ''
  if form.validate_on_submit():
   responsible = form.responsible.data
   title = form.title.data
   description = form.description.data
   due = form.due.data
   try:
    add_task(responsible, title, description, due)
   except:
    message = 'An error occured.'
    return render_template('add_form.html', form=form, message=message, current_user=current_user)
   else:
    message = 'Add Task Successful.'
    return render_template('add_form.html', form=form, message=message, current_user=current_user)
  return render_template('add_form.html', form=form, message=message, current_user=current_user)

def all_tasks_render():
  not_login = not_logged_in()
  if not_login == True:
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
  if not_login == True:
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
  if not_login == True:
    flash("Content only available for logged in users.")
    return redirect('/home')
  
  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user') 

  form = RegisterForm()
  message = ''
  valid_entries = False
  current_user = session.get('current_user')
  if current_user != 'admin':
   return render_template('unauthorised.html', current_user=current_user)
  if form.validate_on_submit():
   username = form.username.data
   password = form.password.data
   confirm = form.confirm.data
   try:
    valid_entries, message = register(username, password, confirm)
   except:
    message = 'An error occured.'
    return render_template('register_form.html', form=form, message=message, current_user=current_user)
   else:
     if valid_entries:
      with open ('static/user.txt', 'a') as f_user:
       f_user.write(f"{username}, {password}\n")
      return render_template('register_form.html', form=form, message=message, current_user=current_user)
  return render_template('register_form.html', form=form, message=message, current_user=current_user)

def statistics():
  return render_template('statistics.html')

def unauthorised():
  not_login = not_logged_in()
  if not_login == True:
    flash("Content only available for logged in users.")
    return redirect('/home')
  
  expired = expired_session()
  if expired:
    flash("Login session timed out. Please login again.")
    return redirect('/home')
  
  current_user = session.get('current_user')

  return render_template('unauthorised.html', current_user=current_user)

def logout():
  #session.pop('logged_in', None)
  session.clear()
  return render_template('logout.html')



        
        
