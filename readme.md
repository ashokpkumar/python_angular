RMG-Application For Indium software

This tool helps in resource management for software application developement or any other project based companies.
The technology stacks are:
Backend: Python Flask based Rest API
Frontend: Angular 9 based frontend
MS SQL for Database

Installation Steps:

1. Tools:
1.a Install the below tools to start with.
1.b Vscode-for code editing.
1.c vscode extensions-install the below extensions for easy python and angular programming.
    1.c.1 Live Share
    1.c.2 Python ms-python.python
    1.c.3 Python for VSCode
    1.c.4 Beautify hookyqr.beautify
    1.c.5 Flask Snippets    codeyard.flask-snippets
    1.c.6 Flask-snippetscstrap.flask-snippets
    1.c.7 GitLens — Git supercharged
    1.c.8 HTML CSS Support
    1.c.9 HTML Snippets
    1.c.10 Kite AutoComplete AI Code: Python, Java, Go, PHP, C/C#/C++, Javascript, HTML/CSS, Typescript, React, Ruby, Scala, Kotlin, Bash, Vue, React
1.d postman
1.e github desktop

2. Database:
    2.a Install latest version of sql server express from microsoft website. the latest version at the time of writing is 2019 edition. download for your OS.
    2.b Choose basic installation and complete the installation. 
    2.c once completed, the sql server express will provide on set of credentials to connect with the database. 
        please keep a note of this as we will need  this in later steps.
    2.d Install Sql Server Management Studio. Download the latest version available for your OS and install choosing basic installation steps. 
        this will install and at the end should connect with your DB with the credentials available in step 2.c. 
    2.e Click on connect and you should see your database being created. we use the master database available under the system database. 
        hence no changes needed in the database structure.

3. Backend:
    3.a Install python 3.9 or latest. we prefer a anaconda distribution. feel free to chose any other distribution and add python to path.
    3.b Clone the repo using Github desktop or using Gitbu CLI.
    3.c The repo will consist of both frontend and backen folders.
    3.d open a command prompt and navigate to the folder where you extracted the repo and cd into /backend
    3.e type "pipenv shell" and press enter. this will create a pipenv environment and should show some id for the environment infront like this 
        "(backend-U_eYhxZH) C:\Users\xxxxxxxxx" in your command prompt
    3.f type "pipenv install" this will install all the dependencies from the pipenv lock file.
    3.g once the dependencies installation is done, navigate to the folder /src/entities to the database.py file.
    3.h in this file, change the connection string as per what is shown in your ssms in step 2.c
        engine = create_engine("mssql+pyodbc://localhost\SQLEXPRESS/master?driver=SQL Server?Trusted_Connection=yes")

    3.i now in your command prompt, navigate to the src folder and type "python main.py". this will run the backend server and show the localhost address.
    3.j you can use the localhost address in your postman to call APIs.
    
4. Frontend:
    4.a install latest version of Node from node.js
    4.b install angular CLI using the command "npm install -g @angular/cli" in a new command prompt
    4.c now in command prompt navigate to the folder \frontend\frontend where you can see the src folder.
    4.d type "npm install" in command prompt at this location and press enter. this will install all the angular dependencies. 
        this will take a long time depending on the internet speed.
    4.e once the installtion is done, type "ng serve -o" and press enter. 
        this will build and serve a application and open the frontend in the default browser and show the login page.

5.User credentials:
    5.a Admin> uname: admin password: admin
    5.b manager> uname: manager password: manager
    5.c vp> uname: vp@123 password: vp@123
    5.d sales> uname: sales password: sales
    5.e employee> uname: employee password: employee
 6. Auto Commit






