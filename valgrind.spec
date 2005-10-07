#%define		_snap	20040612
Summary:	An open-source memory debugger for x86-GNU/Linux
Summary(pl):	Otwarty odpluskwiacz pamiêci dla Linuksa x86
Name:		valgrind
Version:	3.0.1
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	c29efdb7d1a93440f5644a6769054681
URL:		http://valgrind.org/
BuildRequires:	autoconf
BuildRequires:	automake
# Needs libc.a
BuildRequires:	glibc-static
Conflicts:	valgrind-calltree
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Valgrind binaries should _never_ be stripped
%define		no_install_post_strip	1

# Same name as libpthread
%define		_noautoprovfiles %{_libdir}/%{name}/libpthread.so.0 %{_libdir}/%{name}/libpthread.so %{_libdir}/%{name}/valgrind.so %{_libdir}/%{name}/valgrinq.so

%description
Valgrind is a GPL'd system for debugging and profiling x86-Linux
programs. With the tools that come with Valgrind, you can
automatically detect many memory management and threading bugs,
avoiding hours of frustrating bug-hunting, making your programs more
stable. You can also perform detailed profiling to help speed up your
programs.

%description -l pl
Valgrind jest systemem s³u¿±cym do odpluskwiania i profilowania
programów na Linuksie uruchomionym na procesorach x86. U¿ywaj±c
dostarczanych z nim narzêdzi mo¿na automatycznie wykrywaæ wiele
b³êdów zwi±zanych z zarz±dzaniem pamiêci± i w±tkowaniem, dziêki
czemu unika siê frustruj±cego polowania na b³êdy, a tak¿e czyni
siê programy bardziej stabilnymi. Mo¿liwe jest równie¿ dok³adne
profilowanie, dziêki któremu programy zaczn± szybciej pracowaæ.

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
%attr(755,root,root) %{_libdir}/%{name}/*.so
#%{_libdir}/%{name}/*.so.*
%attr(755,root,root) %{_libdir}/%{name}/hp2ps
%attr(755,root,root) %{_libdir}/%{name}/stage2
%{_libdir}/%{name}/*.supp
%{_includedir}/*
%{_pkgconfigdir}/*.pc
%{_mandir}/man1/*.1*
