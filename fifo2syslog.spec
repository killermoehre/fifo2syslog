Summary: A daemon reading from a FIFO and outputting it to SYSLOG
Name: fifo2syslog
Version: 1.0
Release: 1
Copyright: GPL2+
Group: System Environment/Daemons
URL: https://github.com/killermoehre/fifo2syslog
Packager: Silvio Knizek <knizek@b1-systems.de>
Requires: python2

Source0: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.init
Source1: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.py
Source2: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.conf

%prep
rm -rf $RPM_BUILD_DIR/*
git clone %Source

%install
install -o root -g root -m 755 fifo2syslog.py $RPM_BUILD_ROOT/usr/bin/fifo2syslog
install -o root -g root -m 755 fifo2syslog.init $RPM_BUILD_ROOT/etc/init.d/fifo2syslog
install -o root -g root -m 644 fifo2syslog.conf $RPM_BUILD_ROOT/etc/sysconfig/fifo2syslog

%files
/usr/bin/fifo2syslog
/etc/init.d/fifo2syslog
%config /etc/sysconfig/fifo2syslog
