#
# Conditional build:
# _with_sse	- use the SSE instructions of Pentium3+ or Athlon XP
#
Summary:	FluidSynth is a software, real-time synthesizer
Summary(pl):	FluidSynth to programowy syntezator dzia³aj±cy w czasie rzeczywistym
Name:		fluidsynth
Version:	1.0.1
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://savannah.nongnu.org/download/fluid/stable.pkg/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7a0ab811d68afcd1d5a40e04a25eaad7
Source1:	%{name}-fluid_sse.h
URL:		http://www.fluidsynth.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	jack-audio-connection-kit-devel
Requires:	alsa-lib
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
Requires:       %{name} = %{version}

%description devel
This package contains the header files necessary to develop
applications using FluidSynth.

%description devel -l pl
Pakiet tem zawiera pliki nag³ówkowe potrzebne do tworzenia i
kompilacji aplikacji korzystaj±cych z bibliotek FluidSynth.

%package static
Summary:        Static FluidSynth library
Summary(pl):    Statyczna wersje biblioteki FluidSynth
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}

%description static
This package contains static version of the FluidSynth library.

%description static -l pl
Ten pakiet zawiera bibliotekê statyczn± FluidSynth.

%prep
%setup -q
cp %{SOURCE1} src/fluid_sse.h

%build
%configure \
	--enable-ladspa \
	--enable-midishare \
	--enable-jack-support \
	--enable-coreaudio \
	%{?_with_sse:--enable-SSE}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
