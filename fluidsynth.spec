Summary:	FluidSynth is a software, real-time synthesizer
Summary(pl):	FluidSynth to programowy , czasu rzeczywistego syntezator
Name:		fluidsynth
Version:	1.0.1
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://savannah.nongnu.org/download/fluid/stable.pkg/%{version}/%{name}-%{version}.tar.gz
URL:		http://www.fluidsynth.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	jack-audio-connection-kit-devel
Requires:	alsa-lib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fluid Synth is a software, real-time synthesizer based on the
Soundfont 2 specifications.

%description -l pl
Fluid Synth to programowy, czasu rzeczywistego syntezator bazuj±cy na
specyfikacji Soundfont 2

%package devel
Summary:	Development files for the FluidSynth
Summary(pl):	Pliki nag³ówkowe dla FluidSynth
Group:		Development/Libraries

%description devel
This package contains the header files necessary to develop
applications using FluidSynth - header files.

%description devel -l pl
Pakiet tem zawiera pliki nag³ówkowe potrzebne do tworzenia i
kompilacji aplikacji korzystaj±cych z bibliotek FluidSynth


%prep
%setup -q

%build
%configure \
	--enable-ladspa \
	--enable-midishare \
	--enable-jack-support \
	--enable-coreaudio
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib%{name}.so*
%attr(755,root,root) %{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/fluidsynth.pc

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}.h
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
