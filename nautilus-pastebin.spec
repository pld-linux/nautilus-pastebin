# TODO
# - not really gnome3 compatible (gir and static import conflict)
# - complete python deps (pynotify, etc)
# - Exec line missing in .desktop file, bug?
Summary:	Nautilus extension to send files to a pastebin
Name:		nautilus-pastebin
Version:	0.5.0
Release:	0.7
License:	GPL v2+
Group:		X11/Applications
URL:		http://launchpad.net/nautilus-pastebin/
Source0:	https://launchpad.net/nautilus-pastebin/trunk/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	978d0e9007d1dd332a678207b05cf7dd
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	python-distutils-extra
BuildRequires:	sed >= 4.0
Requires:	nautilus-python
Requires(post,preun):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# The package should be a noarch, but the usage the %{_libdir} macro needs removal
# noarch
%define		_enable_debug_packages	0

%description
A Nautilus extension written in Python, which allows users to upload
text-only files to a pastebin service just by right-clicking on them.
Users can also add their favorite service just by creating new
presets.

%prep
%setup -q

# removes the line from the desktop file since this is a meaningless tag here
%{__sed} -i 's|X-Ubuntu-Gettext-Domain=nautilus-pastebin||g' data/%{name}-configurator.desktop
# this as well, as it confuses gconf in pld
# WARNING: node <gettext_domain> not understood below <schema>
%{__sed} -i -e '/<gettext_domain>/d' data/nautilus-pastebin.schemas

%{__sed} -i -e '/^#!\//, 1d' pastebin/core.py

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--install-scripts=%{_datadir}/nautilus-pastebin \
	--root=$RPM_BUILD_ROOT

install -p -D build/scripts-?.?/%{name}.py $RPM_BUILD_ROOT%{_datadir}/nautilus-python/extensions/%{name}.py

%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}-configurator.desktop

install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf
mv $RPM_BUILD_ROOT%{_datadir}/gconf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas

%preun
%gconf_schema_uninstall %{name}.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog GPL-2 NEWS PKG-INFO README
%config(noreplace) %{_sysconfdir}/gconf/schemas/*
%{_datadir}/nautilus-python/extensions/nautilus-pastebin.py
%dir %{py_sitescriptdir}/pastebin
%{py_sitescriptdir}/pastebin/*.py[co]
%{py_sitescriptdir}/nautilus_pastebin-%{version}-*.egg-info
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}-configurator.desktop
