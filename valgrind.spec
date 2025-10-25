# TODO:
# - fix CC detection in configure, so CC=gcc won't be needed
#
# Conditional build:
%bcond_with	mpi	# MPI wrapper module
#
Summary:	An open-source memory debugger
Summary(pl.UTF-8):	Otwarty odpluskwiacz pamięci
Name:		valgrind
Version:	3.26.0
Release:	1
License:	GPL v2+
Group:		Development/Tools
Source0:	https://sourceware.org/pub/valgrind/%{name}-%{version}.tar.bz2
# Source0-md5:	856da1bc568212df6df502295a0439c0
Patch0:		%{name}-native-cpuid.patch
Patch1:		%{name}-ld_linux_strlen.patch
Patch2:		%{name}-datadir.patch
URL:		https://www.valgrind.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.10
BuildRequires:	gcc >= 5:3.0
%ifarch x32
BuildRequires:	gcc-multilib-64 >= 5:3.0
%endif
# check in configure.ac:882 AC_MSG_CHECKING([the GLIBC_VERSION version])
BuildRequires:	glibc-devel >= 6:2.2
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
%{?with_mpi:BuildRequires:	mpi-devel}
BuildRequires:	rpmbuild(macros) >= 2.007
Obsoletes:	valgrind-callgrind < 0.11
Obsoletes:	valgrind-calltree < 0.10
ExclusiveArch:	%{ix86} %{x8664} %{armv7} ppc ppc64 s390x x32 aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/vgpreload.*\\.so
%define		filterout_c	-fstack-protector-strong
# ld portion broken
%undefine	with_ccache

%define		specflags_arm	-marm

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs.
With the tools that come with Valgrind, you can automatically detect
many memory management and threading bugs, avoiding hours of
frustrating bug-hunting, making your programs more stable. You can
also perform detailed profiling to help speed up your programs.

%description -l pl.UTF-8
Valgrind jest systemem służącym do odpluskwiania i profilowania
programów na Linuksie. Używając dostarczanych z nim narzędzi można
automatycznie wykrywać wiele błędów związanych z zarządzaniem pamięcią
i wątkowaniem, dzięki czemu unika się frustrującego polowania na
błędy, a także czyni się programy bardziej stabilnymi. Możliwe jest
również dokładne profilowanie, dzięki któremu programy zaczną szybciej
pracować.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
	cachegrind/cg_annotate.in \
	cachegrind/cg_merge.in \
	cachegrind/cg_diff.in

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
	callgrind/callgrind_annotate.in \
	callgrind/callgrind_control.in

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	GDB=/usr/bin/gdb \
	--enable-tls \
	%{!?with_mpi:--with-mpicc=/bin/false} \
%if "%{_lib}" != "lib"
	--enable-only64bit \
%endif \
	--enable-lto \
	LDFLAGS="" # no strip!

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc
cp -p docs/index.pdf docs/valgrind_manual.pdf
cp -p docs/index.ps docs/valgrind_manual.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README README_MISSING_SYSCALL_OR_IOCTL
%doc docs/html docs/valgrind_manual.pdf docs/valgrind_manual.ps
%attr(755,root,root) %{_bindir}/callgrind_annotate
%attr(755,root,root) %{_bindir}/callgrind_control
%attr(755,root,root) %{_bindir}/cg_annotate
%attr(755,root,root) %{_bindir}/cg_diff
%attr(755,root,root) %{_bindir}/cg_merge
%attr(755,root,root) %{_bindir}/ms_print
%attr(755,root,root) %{_bindir}/valgrind
%attr(755,root,root) %{_bindir}/valgrind-di-server
%attr(755,root,root) %{_bindir}/valgrind-listener
%attr(755,root,root) %{_bindir}/vgdb
%attr(755,root,root) %{_bindir}/vgstack
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib*-linux.a
%if %{with mpi}
# TODO: subpackage?
%attr(755,root,root) %{_libdir}/%{name}/libmpiwrap-*-linux.so
%endif
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/%{name}
%endif
%attr(755,root,root) %{_libexecdir}/%{name}/*-linux
%attr(755,root,root) %{_libexecdir}/%{name}/valgrind-monitor.py
%attr(755,root,root) %{_libexecdir}/%{name}/valgrind-monitor-def.py
%attr(755,root,root) %{_libexecdir}/%{name}/vgpreload_*-linux.so
%{_libexecdir}/%{name}/*.xml
%{_libexecdir}/%{name}/default.supp
%{_datadir}/%{name}
%{_includedir}/valgrind
%{_mandir}/man1/callgrind_annotate.1*
%{_mandir}/man1/callgrind_control.1*
%{_mandir}/man1/cg_annotate.1*
%{_mandir}/man1/cg_diff.1*
%{_mandir}/man1/cg_merge.1*
%{_mandir}/man1/ms_print.1*
%{_mandir}/man1/valgrind.1*
%{_mandir}/man1/valgrind-di-server.1*
%{_mandir}/man1/valgrind-listener.1*
%{_mandir}/man1/vgdb.1*
%{_pkgconfigdir}/valgrind.pc
