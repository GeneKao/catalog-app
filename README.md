
# My Ledger App 

## Udacity Full Stack Web Developer
## Project 4 - Build an Item Catalog Application

>by Gene Ting-Chun Kao




## Preparations

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads). 
(Tested with version 5.2.6 r120293 Qt5.6.3)

- [Vagrant](https://www.vagrantup.com/downloads.html). 
(Tested with 2.0.2)


## Installation

### Fetch the Source Code

**Windows:** Use the Git Bash program (installed with Git) to get a Unix-style
terminal. 
**Other systems:** Use your favorite terminal program.

From the terminal, run:

    git clone https://github.com/GeneKao/ledger-app.git ledger-app

This will give you a directory named **ledger-app** complete with the source
code for the flask application, a vagrantfile, and a bootstrap.sh file for
installing all of the necessary tools. 


## Register Google Oauth

Register and login to your Google Console https://console.cloud.google.com/ and
create a new project. 

Go to **APIs & Services / Credentials** then add http://localhost:8000 to your
**Authorized JavaScript origins**. 

Download JSON and save it to ledger-app/app as **client_secrets.json**. 


## VM Configuration

### Run the virtual machine!

Using the terminal, change directory to oauth (**cd ledger-app**), then type
**vagrant up** to launch your virtual machine. 

### Running the Ledger App
Once it is up and running, type **vagrant ssh**. This will log your terminal
into the virtual machine, and you'll get a Linux shell prompt. When you want to
log out, type **exit** at the shell prompt. 
To turn the virtual machine off (without deleting anything), type **vagrant
halt**. 
If you do this, you'll need to run **vagrant up** again before you can log into it.


Now that you have Vagrant up and running type **vagrant ssh** to log into your
VM. change to the /vagrant directory by typing **cd /vagrant**. 
This will take you to the shared folder between your virtual machine and host
machine.

Type **cd app** to go to applicaiton folder. 

Type **ls** to ensure that you are inside the directory that contains
application.py, models.py, and two directories named 'templates' and 'static'. 


## Run the Code! 

### Set up database 

Now type **python3 models.py** to initialize the database.

### Run the server 

Type **python3 application.py** to run the Flask web server. In your browser
visit **http://localhost:8000** to view the restaurant menu app.  You should be
able to view, add, edit, and delete menu items and restaurants. 


## Usage and highlight

### http://localhost:8000/project/

![Ledgers](/images/Projects.png)


### http://localhost:8000/project/JSON

![Ledgers](/images/ProjectsJSON.png)


### http://localhost:8000/project/3/ledger/

![Ledgers](/images/AddLedger.png)


### http://localhost:8000/project/3/ledger/

![Ledgers](/images/Ledgers.png)


### http://localhost:8000/project/3/ledger/JSON

![Ledgers](/images/LedgersJSON.png)



## Credits

The started code was from [Full stack
Foundations](https://www.udacity.com/course/full-stack-foundations--ud088)'s repo: [Udacity Restaurant Menu
App](https://github.com/udacity/Full-Stack-Foundations/tree/master/Lesson-4/Final-Project)
and from [my OAuth2.0 exercise](https://github.com/GeneKao/OAuth2.0) .



## Contact
Any suggestion please contact [me](https://github.com/GeneKao).
