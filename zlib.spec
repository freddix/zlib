Summary:	A Massively Spiffy Yet Delicately Unobtrusive Compression Library
Name:		zlib
Version:	1.2.8
Release:	6
License:	BSD
Group:		Core/Libraries
Source0:	http://www.zlib.net/%{name}-%{version}.tar.gz
# Source0-md5:	44d667c142d7cda120332623eab69f40
URL:		http://www.zlib.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
zlib is designed to be a free, general-purpose, legally unencumbered
-- that is, not covered by any patents -- lossless data-compression
library for use on virtually any computer hardware and operating
system. The zlib data format is itself portable across platforms.

%package devel
Summary:	Header files and libraries for zlib development
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files and libraries needed
to develop programs that use the zlib library.

%package static
Summary:	Static zlib libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static zlib libraries.

%prep
%setup -q

grep -A 24 '^  Copyright' zlib.h > LICENSE

%build
export CFLAGS="%{rpmcflags}"
export CC="%{__cc}"
./configure			\
	--prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
	--sharedlibdir=%{_libdir}

%{__make}

%check
%{__make} -j1 test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},%{_includedir},%{_libdir},%{_mandir}/man3}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install libz.a $RPM_BUILD_ROOT%{_libdir}
install zutil.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ LICENSE README doc/algorithm.txt
%attr(755,root,root) %ghost %{_libdir}/libz.so.?
%attr(755,root,root) %{_libdir}/libz.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libz.so
%{_includedir}/*.h
%{_pkgconfigdir}/zlib.pc
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

