Summary:	An open-source memory debugger
Summary(pl.UTF-8):	Otwarty odpluskwiacz pamięci
Name:		valgrind
Version:	3.2.3
Release:	4
License:	GPL
Group:		Development/Tools
Source0:	http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	978847992b136c8d8cb5c6559a91df1c
Patch0:		%{name}-debuginfo.patch
Patch1:		%{name}-glibc2.6.patch
# the same as glibc 2.6 for now
Patch2:		%{name}-glibc2.7.patch
URL:		http://valgrind.org/
BuildRequires:	autoconf
BuildRequires:	automake
# Needs libc.a
BuildRequires:	glibc-static
Obsoletes:	valgrind-callgrind
Obsoletes:	valgrind-calltree
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/vgpreload.*\\.so
# ld portion broken
%undefine	with_ccache

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs.
With the tools that come with Valgrind, you can automatically detect
many memory management and threading bugs, avoiding hours of frustrating
bug-hunting, making your programs more stable. You can also perform
detailed profiling to help speed up your programs.

%description -l pl.UTF-8
Valgrind jest systemem służącym do odpluskwiania i profilowania
programów na Linuksie. Używając dostarczanych z nim narzędzi można
automatycznie wykrywać wiele błędów związanych z zarządzaniem pamięcią i
wątkowaniem, dzięki czemu unika się frustrującego polowania na błędy, a
także czyni się programy bardziej stabilnymi. Możliwe jest również
dokładne profilowanie, dzięki któremu programy zaczną szybciej pracować.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e 's:^CFLAGS="-Wno-long-long":CFLAGS="$CFLAGS -Wno-long-long":' configure.in

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
%if %{_lib} != "lib"
	--enable-only64bit \
%endif
	LDFLAGS="" # no strip!
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

strip $RPM_BUILD_ROOT%{_libdir}/%{name}/hp2ps
rm -rf _docs
mv $RPM_BUILD_ROOT%{_docdir}/valgrind _docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS AUTHORS FAQ.txt NEWS README README_MISSING_SYSCALL_OR_IOCTL
%doc _docs/html
%doc _docs/valgrind_manual.pdf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*-linux
%attr(755,root,root) %{_libdir}/%{name}/*-linux/*
%attr(755,root,root) %{_libdir}/%{name}/hp2ps
%{_libdir}/%{name}/*.supp
%{_includedir}/*
%{_pkgconfigdir}/*.pc
%{_mandir}/man1/*.1*
