#
# Conditional build:
%bcond_without	gtk	# GTK+ 2 GUI
#
Summary:	Floppy formatting utility
Summary(pl.UTF-8):	Narzędzie do formatowania dyskietek
Name:		floppy
Version:	0.18
Release:	1
License:	GPL v3
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/floppyutil/%{name}-%{version}.tar.bz2
# Source0-md5:	a02aac97c74259ca1b24972c89147ca4
Source1:	floppygtk.desktop
URL:		http://floppyutil.sourceforge.net/
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
Requires:	uname(release) >= 2.4.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The floppy utility does low-level formatting of floppy disks. This
utility supports formatting of disks in LS-120 drives.

%description -l pl.UTF-8
Narzędzie floppy wykonuje niskopoziomowe formatowanie dyskietek. To
narzędzie obsługuje także formatowanie dyskietek w napędach LS-120.

%package gtk
Summary:	GTK+ floppy formatting utility
Summary(pl.UTF-8):	Narzędzie GTK+ do formatowania dyskietek
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
This package contains a GTK+ interface to the floppy formatting
utility.

%description gtk -l pl.UTF-8
Ten pakiet zawiera graficzny interfejs GTK+ do narzędzia floppy
służącego do formatowania dyskietek.

%prep
%setup -q

%build
%configure \
	%{!?with_gtk:--disable-gtk2}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
: >$RPM_BUILD_ROOT%{_sysconfdir}/floppy

%if %{with gtk}
install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/floppy ]; then
	umask 022
	%{_bindir}/floppy --createrc >%{_sysconfdir}/floppy 2>/dev/null || rm -f %{_sysconfdir}/floppy
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README 
%attr(755,root,root) %{_bindir}/floppy
%ghost %{_sysconfdir}/floppy
%{_mandir}/man8/floppy.8*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/floppygtk
%{_desktopdir}/floppygtk.desktop
%endif
