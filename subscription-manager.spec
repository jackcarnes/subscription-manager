Name: subscription-manager      
Version: 0.12
Release: 1
Summary: Supported tools and libraries for subscription and repo Management       
Group:   System Environment/Base         
License: GPL       
Source0: %{name}-%{version}.tar.gz       
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: python-dmidecode
Requires:  python-ethtool 
Requires:  python-simplejson
Requires:  m2crypto 
Requires: yum >= 3.2.19-15
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
#Requires: pygtk2 pygtk2-libglade gnome-python2 gnome-python2-canvas
#Requires: usermode-gtk

%description
Subscription Manager package provides programs and libraries to allow users to manager subscriptions and repos from a unified entitlement or a deployment Platform.

%prep
%setup -q

%build
mkdir bin
cc src/rhsmcertd.c -o bin/rhsmcertd

%install
# TODO: Need clean/Makefile
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/rhsm
mkdir -p $RPM_BUILD_ROOT/usr/share/rhsm/gui
mkdir -p $RPM_BUILD_ROOT/usr/share/rhsm/gui/data
mkdir -p $RPM_BUILD_ROOT/usr/lib/yum-plugins/
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/rhsm
mkdir -p $RPM_BUILD_ROOT/etc/yum/pluginconf.d/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
mkdir -p $RPM_BUILD_ROOT/var/log/rhsm 
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
cp -R src/*.py $RPM_BUILD_ROOT/usr/share/rhsm
cp -R src/gui/*.py $RPM_BUILD_ROOT/usr/share/rhsm/gui
cp -R src/gui/data/* $RPM_BUILD_ROOT/usr/share/rhsm/gui/data/
cp -R src/plugin/*.py $RPM_BUILD_ROOT/usr/lib/yum-plugins/
cp src/subscription-manager-cli $RPM_BUILD_ROOT/usr/sbin
cp src/subscription-manager-gui $RPM_BUILD_ROOT/usr/sbin
cp etc-conf/rhsm.conf $RPM_BUILD_ROOT/etc/rhsm/
cp etc-conf/rhsmplugin.conf $RPM_BUILD_ROOT/etc/yum/pluginconf.d/
cp bin/* $RPM_BUILD_ROOT/%{_bindir}
cp src/rhsmcertd.init.d $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/rhsmcertd
cp man/* $RPM_BUILD_ROOT/%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

# dirs
%dir /usr/share/rhsm
%dir /usr/share/rhsm/gui

#files
/usr/share/rhsm/__init__.py*
/usr/share/rhsm/connection.py*
/usr/share/rhsm/managercli.py*
/usr/share/rhsm/managerlib.py*
/usr/share/rhsm/repolib.py*
/usr/lib/yum-plugins/rhsmplugin.py*
/usr/share/rhsm/certificate.py*
/usr/share/rhsm/certlib.py*
/usr/share/rhsm/hwprobe.py*
/usr/share/rhsm/config.py*
/usr/share/rhsm/logutil.py*
/usr/share/rhsm/OptionsCli.py*
/usr/share/rhsm/managergui.py*
/usr/share/rhsm/messageWindow.py*
/usr/share/rhsm/gui/firstboot.py  
/usr/share/rhsm/gui/managergui.py  
/usr/share/rhsm/gui/messageWindow.py  
/usr/share/rhsm/gui/data/standalone.glade  
/usr/share/rhsm/gui/data/standaloneH.glade  
/usr/share/rhsm/gui/data/subsgui.glade  
/usr/share/rhsm/gui/data/subsMgr.glade
#/usr/share/rhsm/rhsmcertd.*
%attr(755,root,root) %{_sbindir}/subscription-manager-cli
%attr(755,root,root) %{_sbindir}/subscription-manager-gui
%attr(700,root,root) %dir %{_var}/log/rhsm
%attr(755,root,root) %{_bindir}/rhsmcertd
%attr(755,root,root) %{_sysconfdir}/init.d/rhsmcertd

# config files
%attr(644,root,root) /etc/rhsm/rhsm.conf
%attr(644,root,root) /etc/yum/pluginconf.d/rhsmplugin.conf

%doc
%{_mandir}/man8/subscription-manager-cli.8*

%post
chkconfig --add rhsmcertd
/sbin/service rhsmcertd start

%preun
if [ $1 = 0 ] ; then
   /sbin/service rhsmcertd stop >/dev/null 2>&1
   /sbin/chkconfig --del rhsmcertd
fi

%changelog
* Wed Mar 03 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.12-1
- Resolves: #568433 - Flushed out hardware info
- man page for cli

* Mon Feb 22 2010 Pradeep Kilambi <pkilambi@redhat.com> 0.1-1
- packaging subscription-manager

