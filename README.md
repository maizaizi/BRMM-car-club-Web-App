# COMP-636
Web application structure
1. List of Courses
Route: /listcourses
Function: listcourses()
Method: GET
Template: "courselist.html" (extends "base.html")
This section of the web application displays a list of courses. When a user visits /listcourses, the listcourses() function fetches course data from the database and sends it to the "courselist.html" template. This template then dynamically generates a list of courses on the web page, showing details like course name and description. The layout is consistent across the application since "courselist.html" extends the "base.html" template.

2. Driver’s Run Details
Route: /driverrundetails
Function: Fetches drivers' run details and displays them.
Method: GET
Template: "driverrundetails.html" (extends "base.html")
Data: List of drivers with their run details.
Summary: Shows run details for each driver.
/viewdetails
Function: Displays and possibly edits detailed information.
Methods: GET, POST
Template: "viewdetails.html" (extends "base.html")
Data: Specific details for a driver or run.
Summary: Used for viewing or editing details, supporting various interactions.

3. List of Drivers:
Route: /driverlistdetails
Function: Fetches and displays details for a specific driver.
Template: "driverlistdetails.html" (extends "base.html")
Method: GET
Data: Specific driver's details.
Route: /listdrivers
Function: Displays a list of drivers, handles driver additions or updates if submitted.
Template: "driverlist.html" (extends "base.html")
Methods: GET, POST
Data: List of drivers, updated drivers' information if submitted.
Summary:
/driverlistdetails provides details for a specific driver.
/listdrivers shows all drivers and can update driver information.

4. Overall Results:
Route: /overall
Function: Fetches and displays overall results or standings.
Template: "overall.html" (extends "base.html")
Method: GET
Data: Overall results or standings data.
Summary:
/overall provides a view of the overall results or standings, summarizing the performance of participants or drivers in a competition or over a series of events.


5. Bar Graph:
Route: /graph
Function: Fetches data and displays a bar graph, likely showing the top 5 performances.
Template: "top5graph.html" (extends "base.html")
Method: GET
Data: Data necessary to generate the bar graph.
Summary:
/graph provides a visual representation of performances, possibly highlighting the top 5 results in a bar graph format.



6. Junior Driver List:
Route: /junior_drivers
Function: Fetches and displays a list of junior drivers.
Template: "junior_drivers.html"  (extends "admin.html")
Method: GET
Data: List of junior drivers and their relevant details.
Summary:
/junior_drivers provides a specific view focusing on junior drivers, showcasing their details and possibly their performance or participation in events. This helps in easily accessing and managing information pertinent to this particular group of drivers.

7.  Driver Search:
/search_drivers
Function: Provides a search functionality to find drivers based on specific criteria.
Template: "search_drivers.html" (extends "admin.html")
Methods: GET, POST
Data: Search results or search criteria.
Summary:
/search_drivers is designed for administrators to easily find drivers by using various search criteria. The results are then presented in a user-friendly format.
/searchdriverdetails
Function: Displays detailed information for a specific driver found from the search.
Template: "searchdriverdetails.html" (extends "search_drivers.html")
Method: GET
Data: Detailed information of a specific driver.
Summary:
/searchdriverdetails offers a detailed view of a driver’s information, accessible from the search results provided by "/search_drivers". It serves to give a comprehensive view of a driver’s profile or performance.

8. Edit Runs:
This functionality is likely related to managing and updating the details of various runs in the application.
Functions:
fetch_drivers(cursor): Retrieves a list of drivers from the database.
fetch_courses(cursor): Retrieves a list of courses from the database.
fetch_runs(cursor, driver_id=None, course_id=None): Fetches run details, with optional filters for specific drivers or courses.
Routes and Templates:
/search_runs
Function: Searches for runs based on certain criteria.
Methods: POST
Data: Search criteria for runs.
/update_run
Function: Updates the details of a specific run.
Methods: POST
Data: Updated run details.
/editrun
Function: Provides an interface for editing run details.
Template: "editrun.html" (extends "admin.html")
Methods: GET, POST
Data: Run details for editing, and updated details upon submission.
Summary:
/search_runs is used to search for specific runs.
/update_run is used to submit updates to a run’s details.
/editrun provides a user-friendly interface for editing run details, interacting with the other routes and functions to fetch and update data as needed.
The combination of these routes and functions facilitates the management of run details, allowing for easy searching, viewing, and updating of run information within the application. To provide a more detailed analysis, it would be helpful to analyze the specific code in "editrun.html" and the associated Python functions and routes.



9. Add Driver:
This functionality is designed to facilitate the addition of new drivers to the system.
Routes and Templates:
/add_driver
Function: Provides a form to input details for a new driver.
Template: "add_driver.html"(extends "admin.html")
Methods: GET, POST
Data: Empty form for GET requests, and submitted driver details for POST requests.
Summary: The /add_driver route displays a form for adding a new driver when accessed with a GET request. When the form is submitted (POST request), the new driver’s details are processed, and the user is likely redirected to the success page.
/add_driver_success
Function: Confirms that a new driver has been successfully added.
Template: "add_driver_success.html" (extends "add_driver.html")
Method: GET
Data: Confirmation message or details of the added driver.
Summary: The /add_driver_success route provides a confirmation message to the user, indicating that the new driver has been successfully added to the system.
Overall Summary:
The “Add Driver” functionality consists of two main parts: a form for inputting new driver details (/add_driver), and a confirmation page to inform the user of a successful addition (/add_driver_success). This process ensures that administrators can easily and efficiently add new drivers to the system, with clear feedback provided upon completion.







Assumptions and design decisions:
1. Detail any assumptions that you made (what isn't clear or stated in this brief that you had to assume or ask about).
While analyzing the web application structure and functionality based on the provided routes, templates, and brief descriptions, I made several assumptions to fill in the gaps where information was not explicitly provided. Here are the assumptions detailed:

1.1 Template Inheritance:
I assumed that the HTML templates, such as "driverrundetails.html", "viewdetails.html", "overall.html", "top5graph.html", "admin.html", "junior_drivers.html", "search_drivers.html", "searchdriverdetails.html", "editrun.html", "add_driver.html", and "add_driver_success.html" extend from a base template, which could be "base.html" or "admin.html". This is a common practice in web development to ensure consistency in the layout and style across different pages of the application.

1.2 Data Flow:
I assumed that data fetched or processed in the functions associated with the routes is passed to the templates for rendering. The nature of the data and how it is used within the templates was inferred based on the route descriptions and typical web application behavior.

1.3 Functionality of Routes:
For routes like "/driverrundetails", "/viewdetails", "/overall", "/graph", "/search_drivers", "/searchdriverdetails", "/editrun", "/add_driver", and "/add_driver_success", I made assumptions about their functionality based on their names and common web application patterns. For example, "/driverrundetails" was assumed to fetch and display run details for drivers, and "/add_driver" was assumed to handle the addition of new drivers.

1.4 HTTP Methods:
The HTTP methods associated with each route were used to infer the type of actions they handle. GET requests were assumed to fetch and display data, while POST requests were assumed to handle data submission and updates.
User Roles and Access:
I assumed that there are different user roles in the application, such as drivers and administrators, and that access to certain routes and functionalities is restricted based on these roles to ensure security and data integrity.

1.5 Use of Jinja Templating:
I assumed that Jinja templating is used within the HTML templates to dynamically generate content based on the data passed from the functions.
Validation and Error Handling:
While not explicitly stated, I assumed that there is proper validation and error handling in place for form submissions and data updates, ensuring that only valid and authorized changes are made.

1.6 Database Interaction:
I assumed that the functions associated with the routes interact with a database to fetch, update, or insert data, and that this interaction is handled using a cursor object passed to the functions.
These assumptions were made to provide a coherent and comprehensive analysis based on the limited information provided. They are based on common practices and patterns in web development, particularly with Flask, a popular web framework in Python.

2. Discuss the design decisions you made when designing and developing your app
When I embarked on the journey of developing this web application, I was faced with a myriad of design choices, each pivotal in shaping the user experience, maintainability, and overall functionality of the application.

2.1 Modularity and Template Inheritance
I decided to harness the power of Flask’s template inheritance to create a consistent and maintainable UI across the application. By developing a base template and specific templates like "admin.html" for administrative pages, I ensured a uniform look while providing tailored experiences for different user roles. This approach was chosen over creating individual styles for each page, as it offered a balance between clarity and maintainability, and prevented potential inefficiencies in updating the UI.

2.2 Route Design and Data Flow
Embracing RESTful principles, I implemented clear and descriptive route names, following standard HTTP methods to enhance readability and intuitiveness. This decision was crucial in making the application more developer-friendly and adhering to web standards. I chose to pass data from backend functions directly to templates and handle form submissions via POST requests, ensuring dynamic content delivery and secure data handling. This approach was preferred over client-side logic to reduce dependency on client-side resources and uphold data integrity.

2.3 User Roles, Access Control, and Navigation
Understanding the importance of security and tailored user experiences, I differentiated routes and functionalities based on user roles, such as drivers and administrators. This not only bolstered security but also provided customized interfaces for different user groups. A clear and intuitive navigation bar complemented by a user-friendly layout was implemented across the application, ensuring ease of access to functionalities and enhancing overall user experience.

2.4 Validation, Error Handling, and Database Interaction
I committed to implementing robust server-side validation and comprehensive error handling to ensure data integrity and provide immediate user feedback on issues. This approach was favored over client-side validation for its reliability and ability to uphold data integrity. Additionally, I encapsulated database interactions in functions, utilizing cursor objects and ensuring that database connections were properly managed, which contributed to the application’s maintainability.

2.5 Personal Reflections and Balancing Act
In using multiple similar pages for distinct functionalities and shared templates with conditional rendering, I struck a balance between specificity and reusability. Hidden items in templates were used to adapt pages based on context, ensuring functionality without sacrificing clarity. The use of GET for data retrieval and POST for data submission followed web best practices, ensuring simplicity in data display and security in data submission. Throughout the design process, my focus remained on creating a seamless user experience, maintaining a clear navigation structure, and ensuring the application’s responsiveness through dynamic content updates.
In reflecting on these design decisions, my goal was to create an application that was not just functional, but also intuitive and easy to maintain. Balancing various aspects of web development, from UI consistency and security to data integrity and user experience, was crucial in guiding my design process and ensuring the success of the application.


Database Questions
1. What SQL statement creates the car table and defines its three fields/columns?
CREATE TABLE IF NOT EXISTS car
(
  car_num INT PRIMARY KEY NOT NULL,
  model VARCHAR(20) NOT NULL,
  drive_class VARCHAR(3) NOT NULL
);

2. Which line of SQL code sets up the relationship between the car and driver tables?
FOREIGN KEY (car) REFERENCES car(car_num) ON UPDATE CASCADE ON DELETE CASCADE

3. Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?
INSERT INTO car VALUES
(11,'Mini','FWD'),
(17,'GR Yaris','4WD'),

4. Set a default value of ‘RWD’ for the driver_class field
CREATE TABLE IF NOT EXISTS car
(
  car_num INT PRIMARY KEY NOT NULL,
  model VARCHAR(20) NOT NULL,
  drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
);

5. Why is it important for drivers and the club admin to access different routes?
- Unauthorized Data Modification:
Problem: If drivers can access and alter event results, they might change their own scores or those of others, compromising the fairness of the competition and damaging the club’s credibility.
- Exposure of Sensitive Information:
Problem: If a page displaying personal information of all drivers is accessible to everyone, it could result in a privacy breach, violating data protection regulations and tarnishing the club’s reputation.

5.1 Security and Privacy:
Sensitive Information: Club admins handle sensitive data. Keeping driver access restricted prevents potential misuse of this information.
User Data Protection: Limiting access to personal information of drivers helps in preventing data breaches and protecting privacy.

5.2 Data Integrity:
Controlled Data Modification: Restricting modification capabilities to admins helps in preventing unauthorized changes and maintaining data accuracy.
Clear Accountability: Having separate routes makes it easier to track actions and hold users accountable.

5.3 User Experience:
Simplified Interfaces: Providing tailored access ensures that drivers and admins interact with relevant tools and information, enhancing usability.
Efficiency: This approach helps in making the application more efficient by streamlining access to necessary tools and information based on the user's role.

5.4 Compliance:
Ensuring that only authorized personnel can access sensitive information is often a legal requirement.

Reference
Welcome page video link: https://www.facebook.com/garage5nz/videos/motorkhana-in-the-race-car-at-canterbury_car_club-ruapuna_raceway-today-followed/265847199078341/
