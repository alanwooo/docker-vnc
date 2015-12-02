FROM centos:centos6
MAINTAINER Alan Wu <herobzyy@gmail.com>

RUN yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum -y groupinstall "X Window System"
RUN yum -y groupinstall "Desktop"
RUN yum -y install openssh-server tigervnc-server python-setuptools expect
RUN yum -y install firefox icedtea-web
RUN easy_install supervisor

RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ""
# Fix PAM login issue with sshd
RUN sed -ri 's/session    required     pam_loginuid.so/#session    required     pam_loginuid.so/g' /etc/pam.d/sshd
RUN mkdir -p /root/.ssh && chown root.root /root && chmod 700 /root/.ssh
RUN echo 'root:abcd1234' | chpasswd

RUN mkdir -p /var/log/supervisor  
ADD supervisord.conf /etc/supervisord.conf
ADD startup /usr/bin/startup
RUN chmod 755 /usr/bin/startup
RUN dbus-uuidgen >> /var/lib/dbus/machine-id

EXPOSE 22
EXPOSE 5901
