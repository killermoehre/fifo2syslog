Name: fifo2syslog
Version: 1.0.1
Release: 1
Summary: A daemon reading from a FIFO and outputting it to SYSLOG
License: GPL2+
Group: System Environment/Daemons
URL: https://github.com/killermoehre/fifo2syslog
Packager: Silvio Knizek <knizek@b1-systems.de>
Requires: python2
BuildRoot: %{_tmppath}/%{name}

Source0: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.init
Source1: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.py
Source2: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.conf
Source3: https://raw.githubusercontent.com/killermoehre/fifo2syslog/master/fifo2syslog.sh

%description
This daemon reads from a named pipe (mkfifo(1)) and outputs it into syslog(8). This is done via python2.

%prep

%install
rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT/usr/bin"
mkdir -p "$RPM_BUILD_ROOT/usr/share/fifo2syslog"
mkdir -p "$RPM_BUILD_ROOT/etc/init.d"
mkdir -p "$RPM_BUILD_ROOT/etc/sysconfig"
install -m755 %{SOURCE0} $RPM_BUILD_ROOT/etc/init.d/fifo2syslog
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/fifo2syslog/fifo2syslog.py
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/fifo2syslog
install -m755 %{SOURCE3} $RPM_BUILD_ROOT/usr/bin/fifo2syslog

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
/usr/bin/fifo2syslog
/usr/share/fifo2syslog/fifo2syslog.py
/etc/init.d/fifo2syslog
%config /etc/sysconfig/fifo2syslog
