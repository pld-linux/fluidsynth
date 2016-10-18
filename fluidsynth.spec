#
# Conditional build:
%bcond_with	ladcca		# ladcca sesion management support (deprecated) (GPL)
%bcond_without	lash		# LASH support (GPL)
%bcond_with	midishare	# MidiShare support
%bcond_without	readline	# readline line editing (GPL)
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
Version:	1.1.6
Release:	2
%if %{with ladcca} || %{with lash} || %{with readline}
License:	GPL v2+ (enforced by ladcca/lash/readline), LGPL v2+ (fluidsynth itself)
%else
License:	LGPL v2+
%endif
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/fluidsynth/%{name}-%{version}.tar.bz2
# Source0-md5:	f6e696690e989098f70641364fdffad7
Patch0:		%{name}-midishare.patch
URL:		http://www.fluidsynth.org/
BuildRequires:	alsa-lib-devel >= 0.9.1
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.6.5
BuildRequires:	jack-audio-connection-kit-devel
%{?with_ladcca:BuildRequires:	ladcca-devel < 0.4.0}
%{?with_ladcca:BuildRequires:	ladcca-devel >= 0.3.1}
BuildRequires:	ladspa-devel
%{?with_lash:BuildRequires:	lash-devel >= 0.3}
BuildRequires:	libsndfile-devel >= 1.0.18
BuildRequires:	libtool
%{?with_midishare:BuildRequires:	midishare-devel}
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel >= 19
BuildRequires:	pulseaudio-devel >= 0.9.8
%{?with_readline:BuildRequires:	readline-devel}
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	alsa-lib >= 0.9.1
Requires:	glib2 >= 1:2.6.5
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
Requires:	glib2-devel >= 1:2.6.5
Requires:	jack-audio-connection-kit-devel
%{?with_lash:Requires:	lash-devel >= 0.3}
Requires:	libsndfile-devel >= 1.0.18
%{?with_midishare:Requires:	midishare-devel}
Requires:	portaudio-devel >= 19
Requires:	pulseaudio-devel >= 0.9.8
%{?with_readline:Requires:	readline-devel}

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
	%{!?with_lash:--disable-lash} \
	%{!?with_midishare:--disable-midishare} \
	%{!?with_static_libs:--disable-static} \
	%{?with_sse:--enable-SSE} \
	--enable-jack-support \
	--enable-ladspa \
	--enable-profiling \
	%{!?with_readline:--without-readline}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfluidsynth.la

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
%{_includedir}/fluidsynth.h
%{_includedir}/%{name}
%{_pkgconfigdir}/fluidsynth.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfluidsynth.a
%endif
