To set up the server to run the application:
	0. Open your terminal and navigate to the site directory
	1. To sync the database without data, continue to 1.1. To sync with data, go to 1.2
		1.1 Run the command "$ python manage.py syncdb"
		1.2 Run the command "$ python manage.py syncdbWithSamples"
			1.2.1 reply "yes" to the first prompt and "no" to the second
	2. Launch the server with "$ python manage.py runserver"
	3. In your web browser, navigate to localhost:8000

To use the web application:
	0. Make sure you are connected to the internet. The app will not work without an
	internet connection.
	1. Either log in using a pre-created username and password ("Dan" & "password" is the
		default ShareZone's shed coordinator) or follow the link on screen to register a new 
		account. Registering will log you in and redirect you to the user homepage.
		1.1 The default, pre-populated ShareZone is at zip code 03545
		1.2 The first user to enter a ShareZone will be promoted to Shed Coordinator
			and notified as such.
	2. To edit your user profile, click on the "Edit profile" link on the left side
		of the screen.
		2.1 Modify the required data. Username is not editable.
		2.2 Press the "save" button to save your changes. Your changes are saved and
			you are redirected to the user homepage.
		2.3 To change your password, click the "Change password" button, edit the required
			information, and click "update password". This form validates in the back end for
			security reasons.
	3. To view your tools, add a new tool to your listings, or view tools you 
		are borrowing, click on the "Manage Tools" link. All of the current user's 
		tools they own or borrow are displayed here. 
		3.1 Rejected borrow transactions will be displayed on a new tab when appropriate.
		3.2 To add a new tool, click on the "Add tool!" link beneath your tool listing.
			3.2.1 Fill in the required information and choose whether you wish to share in the
					community shed or your own personal listing, and if the tool is available.
			3.2.2 Click the "Save" button to save and be redirected to your tool listing.
	4. To browse available tools, click on the "Browse local tools" link on the user homepage.
		4.1 Tools available in your community (determined by area code) are displayed here.
		4.2 To borrow a tool, select the desired tool and click the "Borrow!" button.
		4.3 Use the calendar to determine the length of time you'd like to borrow the tool for,
			and click the "Borrow!" button to finish the transaction. You may also include a
			message for the borrower.
		4.4 When other users request to approve or return tools, you will recieve a notification
			on the left side of the page. You may choose to accept or reject the transaction or return.
			4.4.1 Shed coordinators are asked to approve the return of tools to the community shed.
	5. To view the Community Statistics for your ShareZone, click on the "Community Statistics" link
		on the left navigation bar.




Known bugs & issues:
	-Community Statistics sometimes do not update properly until page refresh.
Features not included in this release:
	-Administration
	-Delete a user
		-This is a function that can only be performed by an admin
	-Messaging
These features are included in the back end, but not the front end.