To set up the server to run the application:
	0. Open your terminal and navigate to the site directory
	1. Run the command "$ python setup.py install" from this directory
	2. Run the command "$ python manage.py syncdb" from this directory
	3. If you'd like to include a selection of sample usernames and passwords,
		3.1 Enter the python shell by using "$ python manage.py shell"
		3.2 Run the command "import populatedatabase"
	4. Launch the server with "$ python manage.py runserver"
	5. In your web browser, navigate to localhost:8000

To use the web application:
	0. Make sure you are connected to the internet. The app will not work without an
	internet connection.
	1. Either log in using a pre-created username and password ("Dan", "password") or
	follow the link on screen to register a new account. Registering will log you in
	and redirect you to the user homepage.
	2. To edit your user profile, click on the "Edit profile" link on the left side
		of the scree.
		2.1 Modify the required data. Username and Password are not editable.
		2.2 Press the "save" button to save your changes. Your changes are saved and
			you are redirected to the user homepage.
	3. To view your tools, add a new tool to your listings, or view tools you 
		are borrowing, click on the	"Manage Tools" link. All of the current user's 
		tools they own or borrow are displayed here. You are currently unable to edit tools.
		3.2 To add a new tool, click on the "Add a new tool!" link beneath your tool listing.
			3.2.1 Fill in the required information and choose whether you wish to share in the
					community shed or your own personal listing.
			3.2.2 Click the "Save" button to save and be redirected to your tool listing.
	4. To browse available tools, click on the "Browse local tools" link on the user homepage.
		4.1 Tools available in your community (determined by area code) are displayed here.
		4.2 To borrow a tool, select the desired tool and click the "Borrow!" button.
		4.3 Use the calendar to determine the length of time you'd like to borrow the tool for,
			and click the "Borrow!" button to finish the transaction.




Currently Included Functionality:
	-Register a new user
	-Log in
	-Log out
	-Create a tool
	-Delete a tool
	-Borrow a tool
	-See tools you're borrowing
	-See tools people are borrowing from you
	-See tools available in your area
Known bugs & issues:
	-
Features not included in this release:
	-Administration
	-Approving a borrow request
	-Delete a user
	-Stop borrowing a tool
	-edit a tool


If you have any questions, contact our group leader Dan Inglin at dinglin22@live.com


