Summary:	An open-source memory debugger
Summary(pl):	Otwarty odpluskwiacz pami�ci
Name:		valgrind
Version:	3.1.0
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	d92156e9172dc6097e56c69ea9c88013
URL:		http://valgrind.org/
BuildRequires:	autoconf
BuildRequires:	automake
# Needs libc.a
BuildRequires:	glibc-static
Conflicts:	valgrind-calltree
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/vgpreload.*\\.so

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs.
With the tools that come with Valgrind, you can automatically detect
many memory management and threading bugs, avoiding hours of frustrating
bug-hunting, making your programs more stable. You can also perform
detailed profiling to help speed up your programs.

%description -l pl
Valgrind jest systemem s�u��cym do odpluskwiania i profilowania
program�w na Linuksie. U�ywaj�c dostarczanych z nim narz�dzi mo�na
automatycznie wykrywa� wiele b��d�w zwi�zanych z zarz�dzaniem pami�ci� i
w�tkowaniem, dzi�ki czemu unika si� frustruj�cego polowania na b��dy, a
tak�e czyni si� programy bardziej stabilnymi. Mo�liwe jest r�wnie�
dok�adne profilowanie, dzi�ki kt�remu programy zaczn� szybciej pracowa�.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	LDFLAGS="" # no strip!
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

strip $RPM_BUILD_ROOT%{_libdir}/%{name}/hp2ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS AUTHORS FAQ.txt NEWS README README_MISSING_SYSCALL_OR_IOCTL
%doc $RPM_BUILD_ROOT%{_docdir}/valgrind/html
%doc $RPM_BUILD_ROOT%{_docdir}/valgrind/valgrind_manual.pdf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*-linux
%attr(755,root,root) %{_libdir}/%{name}/*-linux/*
%attr(755,root,root) %{_libdir}/%{name}/hp2ps
%{_libdir}/%{name}/*.supp
%{_includedir}/*
%{_pkgconfigdir}/*.pc
%{_mandir}/man1/*.1*
