Name:       Modello_Installer
Summary:    Installer for Modello
Version:    0.0.1
Release:    1
Group:      Applications/System
License:    Apache 2.0
URL:        http://www.tizen.org
Source0:    %{name}-%{version}.tar.bz2

%description
Installer for Modello

%prep
%setup -q -n %{name}-%{version}

%install
%make_install

%package xwalk
Summary: The Xwalk version of Modello Installer
Requires:   crosswalk

%description xwalk
Installs Modello using Xwalk

%post xwalk

for list in $(find /opt/usr/apps/.preinstallWidgets/ -name "Modello*")
do
	#XWalk requires you be app to install files
	su app -c "xwalkctl -i $list"
done

for list2 in $(ls -d /opt/home/app/.config/xwalk-service/applications/*/)
do
        mkdir -p "$list2/css"
	mkdir -p "$list2/js"
	cp -r /opt/usr/apps/_common/js/services "$list2/js/"
	cp -r /opt/usr/apps/_common/css/* "$list2/css/"
done

%package wrt
Summary: The WRT version of Modello Installer
Requires:   wrt-installer

%description wrt
Installs Modello using wrt-installer

%post wrt

for list in $(find /opt/usr/apps/.preinstallWidgets/ -name "Modello*")
do
	#wrt-installer requires you be root to install files
        wrt-installer -i $list
done

for list2 in $(ls -d /opt/usr/apps/*/)
do
        mkdir -p "$list2/css"
        mkdir -p "$list2/js"
        cp -r /opt/usr/apps/_common/js/services "$list2/res/wgt/js/"
        cp -r /opt/usr/apps/_common/css/* "$list2/res/wgt/css/"
done

%files xwalk
%defattr(-,root,root,-)

%files wrt
%defattr(-,root,root,-)
