%define MODELLO_INSTALL_USER app
%define MODELLO_COMMON_DIR   %{_datadir}/Modello/Common

Name:       Modello-Installer
Summary:    Installer for Modello
Version:    0.0.2
Release:    0
Group:      Automotive/Modello
License:    Apache-2.0
URL:        http://www.tizen.org
Source0:    %{name}-%{version}.tar.bz2
Source1001: Modello-Installer.manifest

%description
Installer for Modello package

%package xwalk
Summary: The Xwalk version of Modello Installer
Requires:   crosswalk
Requires:   Modello-AMBSimulator
Requires:   Modello-Appmanager
Requires:   Modello-Common
Requires:   Modello-Dashboard
Requires:   Modello-Homescreen
Requires:   Modello-Hvac
Requires:   Modello-Multimediaplayer
Requires:   Modello-Nav
Requires:   Modello-Phone
Requires:   Modello-SDL
Requires:   tizen-platform-config

%description xwalk
The Xwalk version of Modello Installer package

%package wrt
Summary: The WRT version of Modello Installer
Requires:   wrt-installer

%description wrt
Installs Modello using wrt-installer package

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
#build section

%install
%make_install

%post xwalk
source %{_sysconfdir}/tizen-platform.conf

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/5000/dbus/user_bus_socket"

for list in $(find $TZ_SYS_APP_PREINSTALL -name "Modello*")
do
	#XWalk requires you not be root to install files
	echo "Installing $list"
	su %{MODELLO_INSTALL_USER} -c "pkgcmd -q -i -t wgt -p $list"
done

for list2 in $(ls -d $TZ_SYS_HOME/%{MODELLO_INSTALL_USER}/apps_rw/xwalk-service/applications/*/)
do
        su %{MODELLO_INSTALL_USER} -c "mkdir -p '$list2/css'"
        su %{MODELLO_INSTALL_USER} -c "mkdir -p '$list2/js'"
        su %{MODELLO_INSTALL_USER} -c "cp -r %{MODELLO_COMMON_DIR}/js/services '$list2/js/'"
        su %{MODELLO_INSTALL_USER} -c "cp -r %{MODELLO_COMMON_DIR}/css/* '$list2/css/'"
        su %{MODELLO_INSTALL_USER} -c "cp -r %{MODELLO_COMMON_DIR}/icons '$list2/'"
done

%postun xwalk
source %{_sysconfdir}/tizen-platform.conf

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/5000/dbus/user_bus_socket"

for list3 in $(su %{MODELLO_INSTALL_USER} -c "xwalkctl" | grep Modello | cut -c 1-10)
do
	echo "Uninstalling $list3"
	su %{MODELLO_INSTALL_USER} -c "pkgcmd -q -u -n $list3"
done

%post wrt
source %{_sysconfdir}/tizen-platform.conf

for list in $(find $TZ_SYS_APP_PREINSTALL -name "Modello*")
do
#wrt-installer requires you be root to install files
        wrt-installer -i $list
done

for list2 in $(ls -d /opt/usr/apps/*/)
do
        mkdir -p "$list2/css"
        mkdir -p "$list2/js"
        cp -r %{MODELLO_COMMON_DIR}/js/services "$list2/res/wgt/js/"
        cp -r %{MODELLO_COMMON_DIR}/css/* "$list2/res/wgt/css/"
done

%files xwalk
%defattr(-,root,root,-)
%manifest %{name}.manifest

%files wrt
%defattr(-,root,root,-)
%manifest %{name}.manifest
