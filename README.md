# Essential Contacts

How many times were you urgently in need of a plumber in your area due to a leak in the house?
This small starter project tries to solve this exact problem.
It enables you to quickly find an essential contact in your area.
If you offer a service and would like people to reach out, upload your details on the website.

### Required Libraries, Softwares and Dependencies

#### Git

If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads). Install the version for your operating system.

#### VirtualBox

VirtualBox is the software that actually runs the VM. You can download it from [virtualbox.org](virtualbox.org). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

#### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. You can download it from [vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

### How To Run Project

#### Download the project

Download the project zip file to you computer and unzip the file. Or clone this repository from the terminal
`https://github.com/mohitlal31/Essential-Contacts.git`

#### Run the virtual machine!

Using the terminal, change directory using the command `cd fullstack/vagrant`, then type `vagrant up` to launch your virtual machine.

Once it is up and running, type `vagrant ssh`. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type `exit` at the shell prompt. To turn the virtual machine off (without deleting anything), type `vagrant halt`. If you do this, you'll need to run vagrant up again before you can log into it.

Now that you have Vagrant up and running type `vagrant ssh` to log into your virtual machine (VM). Change directory to the /vagrant directory by typing `cd /vagrant`. This will take you to the shared folder between your virtual machine and host machine.

#### Run the project!

Change directory to the /catalog directory by typing `cd /catalog`. Once inside the /catalog directory, type `ls` to see a list of directories. You should be able to see a file called **application.py**. Run this file by typing `python application.py`.
Now open your favorite browser and enter the URL `localhost:5000`. That's about it. This should open up the application. Enjoy
