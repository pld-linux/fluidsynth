#
# Conditional build:
%bcond_with	ladcca		# enable ladcca sesion managment support
%bcond_with	sse		# use the SSE instructions of Pentium3+ or Athlon XP
%bcond_without	static_libs	# don't build static library
#
%ifarch pentium3 pentium4 %{x8664}
%define		with_sse	1
%endif
#
Summary:	FluidSynth - a software, real-time synthesizer
Summary(pl.UTF-8):	FluidSynth - programowy syntezator działający w czasie rzeczywistym
Name:		fluidsynth
Version:	1.0.8
Release:	1
License:	LGPL
Group:		Applications/Sound
Source0:	http://savannah.nongnu.org/download/fluid/%{name}-%{version}.tar.gz
# Source0-md5:	e2abfd2e69fd8b28d965df968d7d44ee
Patch0:		%{name}-build.patch
URL:		http://www.fluidsynth.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	jack-audio-connection-kit-devel
%{?with_ladcca:BuildRequires:	ladcca-devel < 0.4.0}
%{?with_ladcca:BuildRequires:	ladcca-devel >= 0.3.1}
BuildRequires:	ladspa-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	alsa-lib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fluid Synth is a software, real-time synthesizer based on the
Soundfont 2 specifications.

%description -l pl.UTF-8
Fluid Synth to programowy, działający w czasie rzeczywistym syntezator
oparty na specyfikacji Soundfont 2.

%package devel
Summary:	Development files for the FluidSynth
Summary(pl.UTF-8):	Pliki nagłówkowe dla FluidSynth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files necessary to develop
applications using FluidSynth.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe potrzebne do tworzenia i
kompilacji aplikacji korzystających z bibliotek FluidSynth.

%package static
Summary:	Static FluidSynth library
Summary(pl.UTF-8):	Statyczna wersje biblioteki FluidSynth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of the FluidSynth library.

%description static -l pl.UTF-8
Ten pakiet zawiera bibliotekę statyczną FluidSynth.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	%{!?with_ladcca:--disable-ladcca} \
	%{!?with_static_libs:--disable-static} \
	%{?with_sse:--enable-SSE} \
	--enable-coreaudio \
	--enable-jack-support \
	--enable-ladspa \
	--enable-profiling \
	--without-readline

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/fluidsynth
%attr(755,root,root) %{_libdir}/libfluidsynth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfluidsynth.so.1
%{_mandir}/man1/fluidsynth.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfluidsynth.so
%{_libdir}/libfluidsynth.la
%{_includedir}/fluidsynth.h
%{_includedir}/%{name}
%{_pkgconfigdir}/fluidsynth.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfluidsynth.a
%endif
