import string
from functions import routes
from flask import Flask
from datetime import timedelta


app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits

app.jinja_env.add_extension('jinja2.ext.do')

app.route('/home', methods=['GET', 'POST'])(routes.login_form)
app.route('/welcome', methods=['GET', 'POST'])(routes.welcome)
app.route('/all_tasks')(routes.view_all_render)
app.route('/add_task', methods=['GET', 'POST'])(routes.add_task_render)
app.route('/my_tasks')(routes.view_mine_render)
app.route('/my_tasks/edit', methods=['GET', 'POST'])(routes.edit_task_render)
app.route('/my_tasks/complete', methods=['GET', 'POST'])(routes.complete_task_render)
app.route('/register', methods=['GET', 'POST'])(routes.reg_user_render)
app.route('/statistics', methods=['GET', 'POST'])(routes.statistics_render)
app.route('/reports')(routes.reports_render)
app.route('/unauthorised')(routes.unauthorised)
app.route('/logout')(routes.logout)



app.config['SECRET_KEY'] = '123456'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

""" if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
	app.debug = True
	app.config['SECRET_KEY'] = '123456' """

