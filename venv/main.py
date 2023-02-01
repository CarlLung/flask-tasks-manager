import string
from modules import routes
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
app.route('/all_tasks')(routes.all_tasks_render)
app.route('/add_task', methods=['GET', 'POST'])(routes.add_task_render)
app.route('/my_tasks')(routes.my_tasks_render)
app.route('/register', methods=['GET', 'POST'])(routes.register_form)
app.route('/statistcs')(routes.statistics_render)
app.route('/unauthorised')(routes.unauthorised)
app.route('/logout')(routes.logout)


app.config['SECRET_KEY'] = '123456'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

""" if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
	app.debug = True
	app.config['SECRET_KEY'] = '123456' """

