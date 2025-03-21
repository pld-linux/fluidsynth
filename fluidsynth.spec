#
# Conditional build:
%bcond_with	midishare	# MidiShare support
%bcond_without	pipewire	# pipewire support
%bcond_without	portaudio	# portaudio support
%bcond_without	readline	# readline line editing (GPL)
%bcond_without	systemd		# systemd notify support
#
Summary:	FluidSynth - a software, real-time synthesizer
Summary(pl.UTF-8):	FluidSynth - programowy syntezator działający w czasie rzeczywistym
Name:		fluidsynth
Version:	2.4.4
Release:	1
%if %{with readline}
License:	GPL v2+ (enforced by readline), LGPL v2+ (fluidsynth itself)
%else
License:	LGPL v2+
%endif
Group:		Applications/Sound
#Source0Download: https://github.com/FluidSynth/fluidsynth/releases
Source0:	https://github.com/FluidSynth/fluidsynth/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4c8389840fbcc7c3a3acab1519d9d20a
URL:		https://www.fluidsynth.org/
BuildRequires:	SDL3-devel >= 3
BuildRequires:	alsa-lib-devel >= 0.9.1
BuildRequires:	cmake >= 3.13
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	ladspa-devel
# OpenMP 4.0
BuildRequires:	libgomp-devel >= 6:4.9
BuildRequires:	libinstpatch-devel >= 1.1.0
BuildRequires:	libsndfile-devel >= 1.0.18
%{?with_midishare:BuildRequires:	midishare-devel}
BuildRequires:	pkgconfig
%{?with_pipewire:BuildRequires:	pipewire-devel >= 0.3}
%{?with_portaudio:BuildRequires:	portaudio-devel >= 19}
BuildRequires:	pulseaudio-devel >= 0.9.8
%{?with_readline:BuildRequires:	readline-devel}
BuildRequires:	rpmbuild(macros) >= 1.213
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
Requires:	alsa-lib >= 0.9.1
Requires:	glib2 >= 1:2.26.0
Requires:	libsndfile >= 1.0.18
Suggests:	soundfont-fluid
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
Requires:	alsa-lib-devel >= 0.9.1
Requires:	dbus-devel >= 1.0.0
Requires:	glib2-devel >= 1:2.26.0
Requires:	jack-audio-connection-kit-devel
Requires:	libsndfile-devel >= 1.0.18
%{?with_midishare:Requires: midishare-devel}
%{?with_pipewire:Requires:	pipewire-devel >= 0.3}
%{?with_portaudio:Requires:	portaudio-devel >= 19}
Requires:	pulseaudio-devel >= 0.9.8
%{?with_readline:Requires: readline-devel}
Obsoletes:	fluidsynth-static < 2

%description devel
This package contains the header files necessary to develop
applications using FluidSynth.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe potrzebne do tworzenia i
kompilacji aplikacji korzystających z bibliotek FluidSynth.

%prep
%setup -q

%build
%cmake -B build \
	-Denable-midishare=%{with midishare} \
	%{!?with_pipewire:-Denable-pipewire=OFF} \
	-Denable-portaudio=%{with portaudio} \
	-Denable-readline=%{with readline} \
	%{!?with_systemd:-Denable-systemd=OFF}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md THANKS TODO
%attr(755,root,root) %{_bindir}/fluidsynth
%attr(755,root,root) %{_libdir}/libfluidsynth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfluidsynth.so.3
%{_mandir}/man1/fluidsynth.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfluidsynth.so
%{_includedir}/fluidsynth.h
%{_includedir}/fluidsynth
%{_pkgconfigdir}/fluidsynth.pc
%{_libdir}/cmake/fluidsynth
