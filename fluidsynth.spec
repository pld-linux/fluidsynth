#
# Conditional build:
%bcond_with	ladcca	# enable ladcca sesion managment support
%bcond_with	sse	# use the SSE instructions of Pentium3+ or Athlon XP
#
%ifarch pentium3 pentium4 amd64
%define		with_sse	1
%endif
#
Summary:	FluidSynth is a software, real-time synthesizer
Summary(pl):	FluidSynth to programowy syntezator dzia³aj±cy w czasie rzeczywistym
Name:		fluidsynth
Version:	1.0.3
Release:	4
License:	LGPL
Group:		Applications/Sound
Source0:	http://savannah.nongnu.org/download/fluid/stable.pkg/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fbdccd05e538626888e27b58d3bdbc2b
URL:		http://www.fluidsynth.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	jack-audio-connection-kit-devel
%{?with_ladcca:BuildRequires:	ladcca-devel >= 0.3.1}
%{?with_ladcca:BuildRequires:	ladcca-devel < 0.4.0}
BuildRequires:	ladspa-devel
Requires:	alsa-lib
# supports also Mac OS X Darwin, so probably it is easy to extend
ExclusiveArch:	%{ix86} amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fluid Synth is a software, real-time synthesizer based on the
Soundfont 2 specifications.

%description -l pl
Fluid Synth to programowy, dzia³aj±cy w czasie rzeczywistym syntezator
oparty na specyfikacji Soundfont 2.

%package devel
Summary:	Development files for the FluidSynth
Summary(pl):	Pliki nag³ówkowe dla FluidSynth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files necessary to develop
applications using FluidSynth.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe potrzebne do tworzenia i
kompilacji aplikacji korzystaj±cych z bibliotek FluidSynth.

%package static
Summary:	Static FluidSynth library
Summary(pl):	Statyczna wersje biblioteki FluidSynth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of the FluidSynth library.

%description static -l pl
Ten pakiet zawiera bibliotekê statyczn± FluidSynth.

%prep
%setup -q

%build

cp /usr/share/automake/config.sub .

%configure \
	%{!?with_ladcca:--disable-ladcca} \
	%{?with_sse:--enable-SSE} \
	--enable-coreaudio \
	--enable-jack-support \
	--enable-ladspa \
	--enable-midishare \
	--enable-profiling
	
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
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%attr(755,root,root) %{_libdir}/lib%{name}.la
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_libdir}/pkgconfig/fluidsynth.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib%{name}.a
