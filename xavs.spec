#
# Conditional build:
%bcond_without	asm	# MMX/SSE* x86 assembler optimizations

%ifnarch %{ix86} %{x8664}
%undefine	with_asm
%endif
Summary:	Audio Video Standard of China library
Summary(pl.UTF-8):	Biblioteka kodeka AVS (Audio Video Standard of China)
Name:		xavs
Version:	0
%define	svnver	55
Release:	0.svn%{svnver}.2
License:	GPL v2+
Group:		Libraries
# svn co https://xavs.svn.sourceforge.net/svnroot/xavs/trunk xavs
Source0:	%{name}-r%{svnver}.tar.xz
# Source0-md5:	c4f73561424d850a5c59ef202d85f0d7
Patch0:		%{name}-dynamic-xavs.patch
Patch1:		%{name}-asm.patch
URL:		http://xavs.sourceforge.net/
BuildRequires:	tar >= 1:1.22
# for svnversion
BuildRequires:	subversion
BuildRequires:	xz
%if %{with asm}
BuildRequires:	binutils >= 2:2.17
BuildRequires:	yasm >= 0.6.1
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AVS is the Audio Video Standard of China. This project aims to
implement high quality AVS encoder and decoder.

%description -l pl.UTF-8
AVS (Audio Video Standard of China) to standardowy kodek A/V dla Chin.
Celem projektu jest zaimplementowanie wysokiej jakości kodera i
dekodera AVS.

%package devel
Summary:	Header files for AVS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AVS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for AVS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AVS.

%package static
Summary:	Static AVS library
Summary(pl.UTF-8):	Statyczna biblioteka AVS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AVS library.

%description static -l pl.UTF-8
Statyczna biblioteka AVS.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
# not autoconf script
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--enable-asm%{!?with_asm:=no} \
	--enable-shared \
	--extra-cflags="%{rpmcflags} %{rpmcppflags} -fno-strict-aliasing" \
	--extra-ldflags="%{rpmldflags}"

# linking hack
ln -sf libxavs.so.1 libxavs.so

%{__make} default libxavs.a \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xavs
%attr(755,root,root) %{_libdir}/libxavs.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxavs.so
%{_includedir}/xavs.h
%{_pkgconfigdir}/xavs.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libxavs.a
