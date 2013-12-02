# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.26
# 

Name:       ohm

# >> macros
# << macros

Summary:    Open Hardware Manager
Version:    1.1.14
Release:    1
Group:      System/Resource Policy
License:    LGPLv2.1
URL:        http://meego.gitorious.org/maemo-multimedia/ohm
Source0:    %{name}-%{version}.tar.gz
Source1:    ohm-rpmlintrc
Source100:  ohm.yaml
Requires:   ohm-configs
Requires:   boardname >= 0.4.1
Requires:   systemd
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1) >= 0.70
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.70
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(libsimple-trace)
BuildRequires:  pkgconfig(boardname)

%description
Open Hardware Manager.


%package configs-default
Summary:    Common configuration files for %{name}
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Provides:   ohm-config > 1.1.15
Provides:   ohm-configs
Obsoletes:  ohm-config <= 1.1.15

%description configs-default
This package contains common OHM configuration files.


%package plugin-core
Summary:    Common %{name} libraries
Group:      System/Resource Policy
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description plugin-core
This package contains libraries needed by both for running OHM and
developing OHM plugins.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%autogen --disable-static
%configure --disable-static \
    --without-xauth \
    --with-distro=meego \
    --disable-legacy

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
# make sure we get a plugin config dir even with legacy plugins disabled
mkdir -p %{buildroot}/%{_sysconfdir}/ohm/plugins.d

# enable ohmd in the basic systemd target
install -d %{buildroot}/%{_lib}/systemd/system/basic.target.wants
ln -s ../ohmd.service %{buildroot}/%{_lib}/systemd/system/basic.target.wants/ohmd.service
# << install post

%preun
if [ "$1" -eq 0 ]; then
systemctl stop ohmd.service
fi

%post
systemctl daemon-reload
systemctl reload-or-try-restart ohmd.service

%postun
systemctl daemon-reload

%post plugin-core -p /sbin/ldconfig

%postun plugin-core -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%{_sbindir}/*ohm*
/%{_lib}/systemd/system/ohmd.service
/%{_lib}/systemd/system/basic.target.wants/ohmd.service
# << files

%files configs-default
%defattr(-,root,root,-)
# >> files configs-default
%dir %{_sysconfdir}/ohm
%dir %{_sysconfdir}/ohm/plugins.d
%config %{_sysconfdir}/ohm/modules.ini
%config %{_sysconfdir}/dbus-1/system.d/ohm.conf
# << files configs-default

%files plugin-core
%defattr(-,root,root,-)
# >> files plugin-core
%{_libdir}/libohmplugin.so.*
%{_libdir}/libohmfact.so.*
# << files plugin-core

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_includedir}/ohm
%{_libdir}/pkgconfig/*
%{_libdir}/libohmplugin.so
%{_libdir}/libohmfact.so
# << files devel
