
# Ledger app 

## Udacity Full Stack Web Developer
## Project 4 - Build an Item Catalog Application

>by Gene Ting-Chun Kao




## Preparations

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads). 
(Tested with version 5.2.6 r120293 Qt5.6.3)

- [Vagrant](https://www.vagrantup.com/downloads.html). 
(Tested with 2.0.2)


## Installation

### Fetch the Source Code and VM Configuration

**Windows:** Use the Git Bash program (installed with Git) to get a Unix-style terminal.
**Other systems:** Use your favorite terminal program.

From the terminal, run:

    git clone https://github.com/GeneKao/ledger-app.git ledger-app

This will give you a directory named **ledger-app** complete with the source code for the flask application, a vagrantfile, and a bootstrap.sh file for installing all of the necessary tools. 


### Run the virtual machine!

Using the terminal, change directory to oauth (**cd ledger-app**), then type **vagrant up** to launch your virtual machine.

## Running the Ledger App
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.


Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.

Type **cd app** to go to applicaiton folder. 

Type **ls** to ensure that you are inside the directory that contains application.py, models.py, and two directories named 'templates' and 'static'

Now type **python3 models.py** to initialize the database.

Type **python3 application.py** to run the Flask web server. In your browser visit **http://localhost:8000** to view the restaurant menu app.  You should be able to view, add, edit, and delete menu items and restaurants.


## Contact
Any suggestion please contact [me](https://github.com/GeneKao).
