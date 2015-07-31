Summary: A daemon reading from a FIFO and outputting it to SYSLOG
Name: fifo2syslog
Version: 1.0
Release: 1
Copyright: GPL2+
Group:
Source:
URL: http://fireclown2.lasg/wiki/index.php/Fifo2syslog
Packager: Silvio Knizek <sknizek@airplus.com>

%install
install -o root -g root -m 755 fifo2syslog.py /usr/bin/fifo2syslog
install -o root -g root -m 755 fifo2syslog.init /etc/init.d/fifo2syslog
install -o root -g root -m 644 fifo2syslog.conf /etc/sysconfig/fifo2syslog

%files
/usr/bin/fifo2syslog
/etc/init.d/fifo2syslog
/etc/sysconfig/fifo2syslog