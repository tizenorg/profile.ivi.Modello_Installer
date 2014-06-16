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
Requires:   Modello_AMBSimulator
Requires:   Modello_Appmanager
Requires:   Modello_Common
Requires:   Modello_Dashboard
Requires:   Modello_Homescreen
Requires:   Modello_Hvac
Requires:   Modello_Multimediaplayer
Requires:   Modello_Nav
Requires:   Modello_Phone
Requires:   Modello_SDL
Requires:   tizen-platform-config

%description xwalk
Installs Modello using Xwalk

%post xwalk

source %_sysconfdir/tizen-platform.conf

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/5000/dbus/user_bus_socket"

for list in $(find $TZ_SYS_APP_PREINSTALL -name "Modello*")
do
	#XWalk requires you not be root to install files
	echo "Installing $list"
	su "$TZ_USER_NAME" -c "xwalkctl -i $list"
done

for list2 in $(ls -d $TZ_SYS_HOME/$TZ_USER_NAME/.config/xwalk-service/applications/*/)
do
        su "$TZ_USER_NAME" -c "mkdir -p '$list2/css'"
	su "$TZ_USER_NAME" -c "mkdir -p '$list2/js'"
	su "$TZ_USER_NAME" -c "cp -r $TZ_USER_APP/_common/js/services '$list2/js/'"
	su "$TZ_USER_NAME" -c "cp -r $TZ_USER_APP/_common/css/* '$list2/css/'"
	su "$TZ_USER_NAME" -c "cp -r $TZ_USER_APP/_common/icons '$list2/'"
done

%postun xwalk

source %_sysconfdir/tizen-platform.conf

for list3 in $(su "$TZ_USER_NAME" -c "xwalkctl" | grep Modello | cut -c 1-32)
do
	echo "Uninstalling $list3"
	su "$TZ_USER_NAME" -c "xwalkctl -u $list3"
done

#------------------------------------------------------------------------------------

%package wrt
Summary: The WRT version of Modello Installer
Requires:   wrt-installer

%description wrt
Installs Modello using wrt-installer

%post wrt

source %_sysconfdir/tizen-platform.conf

for list in $(find $TZ_SYS_APP_PREINSTALL -name "Modello*")
do
	#wrt-installer requires you be root to install files
        wrt-installer -i $list
done

for list2 in $(ls -d $TZ_USER_APP/*/)
do
        mkdir -p "$list2/css"
        mkdir -p "$list2/js"
        cp -r $TZ_USER_APP/_common/js/services "$list2/res/wgt/js/"
        cp -r $TZ_USER_APP/_common/css/* "$list2/res/wgt/css/"
done

%files xwalk
%defattr(-,root,root,-)

%files wrt
%defattr(-,root,root,-)
