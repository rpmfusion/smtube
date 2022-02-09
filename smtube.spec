Name:           smtube
Version:        21.10.0
Release:        3%{?dist}
Summary:        YouTube browser for SMPlayer

License:        GPLv2+
URL:            https://www.smtube.org
Source0:        https://downloads.sourceforge.net/smtube/smtube-%{version}.tar.bz2

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5PrintSupport)
#BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)

Requires:       hicolor-icon-theme
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:     smplayer
%else
Requires:       smplayer
%endif

%if 0%{?fedora}
# we only have yt-dlp on fedora
Requires:       yt-dlp
%endif

%{?kf5_kinit_requires}
#translating kf5_kinit_requires -> Requires: kf5-kinit(x86-64)

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%setup -q
# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
rm -r src/qt-json/

%build
pushd src
%if 0%{?fedora}
    sed -i 's/DEFINES += CODEDOWNLOADER/DEFINES -= CODEDOWNLOADER/' smtube.pro
%endif
    %{qmake_qt5}
    %make_build TRANSLATION_PATH="\\\"%{_datadir}/smtube/translations\\\""
    %{_bindir}/lrelease-qt5 smtube.pro
popd


%install
%make_install PREFIX=%{_prefix} DOC_PATH=%{_docdir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%if (0%{?rhel} && 0%{?rhel} <= 7)
%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%files
%license Copying.txt
%{_bindir}/smtube
%{_datadir}/applications/smtube.desktop
%{_datadir}/icons/hicolor/*/apps/smtube.png
%{_datadir}/smtube
#{_mandir}/man1/smtube.1.gz
%{_docdir}/%{name}/

%changelog
* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 21.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 30 2021 Sérgio Basto <sergio@serjux.com> - 21.10.0-2
- After require install yt-dlp, we disable "donwload and install yt-dlp" feature

* Mon Nov 01 2021 Sérgio Basto <sergio@serjux.com> - 21.10.0-1
- Update smtube to 21.10.0

* Mon Aug 16 2021 Sérgio Basto <sergio@serjux.com> - 21.7.0-1
- Update smtube to 21.7.0

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 19 2020 Sérgio Basto <sergio@serjux.com> - 20.6.0-1
- Update smtube to 20.6.0

* Sun Jan 26 2020 Sérgio Basto <sergio@serjux.com> - 20.1.0-1
- Update smtube to 20.1.0

* Sun Oct 27 2019 Sérgio Basto <sergio@serjux.com> - 19.6.0-1
- smtube-19.6.0

* Thu Feb 25 2016 Ricardo Villalba <rvm@users.sourceforge.net> - 16.1.0
- Initial Release
