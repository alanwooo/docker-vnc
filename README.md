# Introduction:

    To start a desktop in docker container.

# Getting started:

 1. Install docker on your host.

	$ sudo yum install docker-io

 2. Clone the code.

	$ cd $your_workspace

 3. Build docker image.

	$ cd ./docker-vnc

	$ sudo docker build --rm -t alanwooo/centos6-gnome-vnc:last .

 4. Copy docker-vnc file to /usr/bin/.

	$ sudo chmod a+x ./src/docker-vnc

	$ sudo cp ./src/docker-vnc /usr/bin/

# Usage:

	1. Access container by VNC client(vncviewer).
		$ sudo docker-vnc
	2. Access the firefox in the container by SSH X11 forwarding.
		$ sudo docker-vnc -x
