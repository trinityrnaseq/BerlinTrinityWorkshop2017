# BernWorkshop2016
workshop in Bern, Switzerland in Oct 2016

trinity ws materials:

*  pull workshop supporting code: git clone https://github.com/trinityrnaseq/BernWorkshop2016.git
*  ftp'd data from Broad as: <https://data.broadinstitute.org/Trinity/RNASEQ_WORKSHOP/TRINITY_Bern_2016_ws_data_bundle.tar.gz>

single cell ws materials:
*  git clone https://github.com/TimothyTickle/single_cell_analysis.git


## Server Setup:

### Create a user:pass of training:training

    sudo groupadd -g 2000 training
    sudo useradd -m -u 2000 -g 2000 training
    echo 'training:training' | sudo chpasswd
    sudo usermod -G training,www-data training
    sudo chsh training -s /bin/bash


### Pull the Docker images from Dockerhub:

    docker pull bernws2016/trinity
    docker pull trinityctat/scell



### Prep shared folders under /home/training

    sudo mv TRINITY_Bern_2016_ws_data_bundle.tar.gz /home/training
    su training
    cd $HOME
    tar xvf TRINITY_Bern_2016_ws_data_bundle.tar.gz

    # pull down the single cell workshop materials into the shared resources area
    cd workshop_shared/shared
    git clone https://github.com/TimothyTickle/single_cell_analysis.git
    
    exit


### Create user workspaces

Here's where the magic of Docker comes in.  Instead of creating different unix users for workshop attendees, we'll just create separate workspace directories for each user, and then mount that workspace area in as the home directory of a user as running in a Docker container.  All communication of the user with the docker container will happen via a unique port assignment and easily accessed via the web browser.

Each student will have two Docker containers running:  1. for the Trinity workshop, involving an SSH terminal and an Apache webserver, and 2. for the single cell workshop, where all work will be done via Rstudio.

Every user will be assigned a numerical ID (eg. in the range 1..50) and ports will be assigned in the following ranges for each of the applications: SSH (9k), Apache (8k), and Rstudio (10k).

We'll run the following to both create user directories and create commands that will be used for launching Docker containers.

    ~/BernWorkshop2016/__setup/user_setup/init_users.py \
        --num_users 30 \
	--ip_addr binfservapp05.unibe.ch \
	--apache_base_port 8001 \
	--gateone_base_port 9001 \
	--rstudio_base_port 10001  > cmds.list

The above will create directories:

    user_spaces/user_01
    user_spaces/user_02
    user_spaces/user_03
    user_spaces/user_04
    ...

and the cmds.list has the commands required to update permissions on these user directories and for launching the docker containers for the students:

    ex.  head -n4 cmds.list

    sudo chown -R training user_spaces
    sudo chgrp -R training user_spaces
    docker run -v /home/bhaas/user_spaces/user_01:/home/training  -v /home/training/workshop_shared/shared:/home/training/shared_ro:ro  -v /home/bhaas/user_spaces/user_01:/var/www/html  -v /home/training/workshop_shared/js:/var/www/html/js:ro  -v /home/training/workshop_shared/css:/var/www/html/css:ro  -p 8001:80 -p 9001:443  --name trinity_user_01 -d bernws2016/trinity
    docker run  -v /home/bhaas/user_spaces/user_01:/home/training  -v /home/training/workshop_shared/shared:/home/training/shared_ro:ro  -p 10001:8787  --name rstudio_user_01 -d trinityctat/scell


Simply running 'sh cmds.list' would run through all the commands in that list.  Notice that the workspace for user with ID 1 is being set up in Docker has having the user_01/ area mounted as /home/training in the docker container, and that the various ports (8001, 9001, and 10001) are being mapped to the ports that each of the applications listen to in the docker container.



### Create a student landing page

On your main server (outside of Docker), be sure to install apache2:

    sudo apt-get  update && sudo apt-get install -y apache2


Run the following script to generate a web page that provides links for each student to their corresponding ssh, apache, and rstudio instances with proper port assignments.

You simply need a file 'attendees.list' that contains a single column with the names of the students as you want them to appear on the web page.


    ~/BernWorkshop2016/__setup/user_setup/attendee_list_to_html_table.py  \
        --ip_addr binfservapp05.unibe.ch \
	--apache_base_port 8001 \
	--gateone_base_port 9001 \
	--rstudio_base_port 10001 \
	--attendee_list attendees.list \
	--user_id_start 1 \
	> course_page.html

Further edit the course_page.html file to your liking, and then drop it into:

     sudo cp course_page.html /var/www/html/.

and then visit:

    http://binfservapp05.unibe.ch/course_page.html

to view the page in your web browser.

# Other Docker tidbits:

## Removing all docker containers:

If you want to remove all the student Docker containers, you can run the following script:

    ~/BernWorkshop2016/__setup/user_setup/remove_user_dockers.sh

which essentially runs 'docker stop' and 'docker rm' to first stop and then remove the docker container.

## Dealing with hang-ups

If the ssh-terminal or Rstudio ends up hanging for some reason, you can just restart that user's docker container.  Examine the port number in the student's web URL and then find that running docker instance:

    docker ps | grep $port_number

Get the 'CONTAINER ID' (ex. 1326d98012af)  and then restart it:

    docker restart 1326d98012af

This will immediately reset it and the student will carry on from where they left off.

## Running all of this on Amazon:

See this excellent documentation from Nico Delhomme [here on github](https://github.com/ekorpela/cloud-vm-workshop/blob/master/materials/NicolasDelhomme/using_docker_on_aws_for_bioinformatics_workshops-practical.pdf), which provides a walkthrough for setting up a system just like this on Amazon. You simply need to just set up your instance, and then follow the instructions above for further setup.  Get the IP address for your Amazon machine and use that in place of the http://binfservapp05.unibe.ch/ server.


