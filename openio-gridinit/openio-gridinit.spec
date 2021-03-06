%define         realname gridinit
Name:           openio-%{realname}
Version:        1.5
Release:        1%{?dist}
Summary:        OpenIO gridinit daemon

License:        AGPLv3
#URL:
Source0:        https://github.com/open-io/gridinit/archive/v%{version}.tar.gz
Source1:        %{realname}.systemd
Source2:        %{name}.tmpfiles
Source3:        %{name}-rsyslog.conf
Source4:        %{name}-logrotate.conf

# Requires
BuildRequires:  autoconf,automake,libtool
BuildRequires:  git,bison,flex,cmake
BuildRequires:  glib2-devel    >= 2.28.8
BuildRequires:  libevent-devel >= 2.0

Requires:       glib2         >= 2.28.8
Requires:       libevent      >= 2.0
Requires:       %{name}-utils  = %{version}


%description
Init program used by the  OpenIO Open Source Project. It forks processes
and respawns them as soon as they die. It also provides a simple management
interface through a UNIX socket. Services can be started/stopped/monitored.
OpenIO gridinit is a fork of Redcurrant gridinit, from Worldline by Atos.


%package        utils
Summary:        Grid Init utilities libraries
License:        GPL v3
Requires:       glib2 >= 2.28.8
%description	utils
C code library with children processes management features. This library is
internally used by the gridinit process.

%package        devel
Summary:        Grid Init devel headers
License:        GPL v3
Requires:       %{name}-utils
%description    devel
Devel files for OpenIO gridinit.


%prep
%setup -q -n %{realname}-%{version}


%build
cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DGRIDINIT_SOCK_PATH="/run/%{realname}/%{realname}.sock" \
  .

make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

# Default config file
%{__mkdir_p} -m755 %{buildroot}%{_sysconfdir}/%{realname}
%{__install} -m644 gridinit.conf.default %{buildroot}%{_sysconfdir}/%{realname}/gridinit.conf

# Install init script
%{__mkdir_p} %{buildroot}/usr/lib/systemd/system
%{__install} -m644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/gridinit.service

# Install tmpfiles
%{__mkdir_p} -v ${RPM_BUILD_ROOT}%{_prefix}/lib/tmpfiles.d
%{__install} -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/lib/tmpfiles.d/gridinit.conf
%{__mkdir_p} -v %{buildroot}/run/%{realname}

# Install rsyslog configuration
%{__mkdir_p} -v ${RPM_BUILD_ROOT}/etc/rsyslog.d
%{__install} -m644 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rsyslog.d/gridinit.conf

# Install logrotate configuration
%{__mkdir_p} -v ${RPM_BUILD_ROOT}/etc/logrotate.d
%{__install} -m644 %{SOURCE4} ${RPM_BUILD_ROOT}/etc/logrotate.d/gridinit.conf

# Remove dirty .la
%{__rm} -vf %{buildroot}%{_libdir}/gridinit/*.la


%files
%defattr(-,root,root,-)
/usr/lib/systemd/system/gridinit.service
%{_bindir}/*
%dir %{_sysconfdir}/%{realname}
%config(noreplace) %{_sysconfdir}/%{realname}/*
%{_prefix}/lib/tmpfiles.d/*
/run/%{realname}
%{_sysconfdir}/rsyslog.d/*
%{_sysconfdir}/logrotate.d/*

%files utils
%defattr(-,root,root,-)
%{_libdir}/libgridinit-utils.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h


%post
if [ $1 -eq 1 ] ; then 
  # Initial installation 
  /usr/bin/systemctl preset gridinit.service >/dev/null 2>&1 || : 
else
   /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || : 
fi
/usr/bin/systemctl reload-or-restart rsyslog.service
%preun
if [ $1 -eq 0 ] ; then 
  # Package removal, not upgrade 
  /usr/bin/systemctl --no-reload disable gridinit.service > /dev/null 2>&1 || : 
  /usr/bin/systemctl stop gridinit.service > /dev/null 2>&1 || : 
fi
%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || : 
if [ $1 -ge 1 ] ; then 
  # Package upgrade, not uninstall 
  /usr/bin/systemctl try-restart gridinit.service >/dev/null 2>&1 || : 
fi
/usr/bin/systemctl reload-or-restart rsyslog.service

%post utils
/sbin/ldconfig
%postun utils
/sbin/ldconfig


%changelog
* Wed Nov 25 2015 - 1.5-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix GCC version detection
- Fix default socket path
* Thu Jun 04 2015 - 1.4-3%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix tmpfiles
* Thu Apr 09 2015 - 1.4-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release to come with OpenIO SDS 0.3
* Thu Mar 19 2015 - 1.3.1-2%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix systemd reload on update
* Thu Mar 19 2015 - 1.3.1-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix PREFIX in spec file
- Fix socket path
- Add rsyslog support
- Add logrotate rule
* Wed Mar 18 2015 - 20150310-2%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Add tmpfiles
- Cleaned spec file
- Moved from /run to /run/gridinit
* Tue Mar 10 2015 - 20150310-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- New release
* Fri Mar 06 2015 - 20150309-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix socket path
- Remove runstatedir (using /run)
* Fri Mar 06 2015 - 20150203-2%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Fix for systemd
* Tue Feb 03 2015 - 20150203-1%{?dist} - Romain Acciari <romain.acciari@openio.io>
- Inital release
