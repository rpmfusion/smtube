Name:           smtube
Version:        20.6.0
Release:        1%{?dist}
Summary:        YouTube browser for SMPlayer

License:        GPLv2+
URL:            https://www.smtube.org
Source0:        https://downloads.sourceforge.net/smtube/smtube-%{version}.tar.bz2
Patch3:         smtube-18.11.0-system-qtsingleapplication.patch

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
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
# for unbundle sources
BuildRequires:  qtsingleapplication-qt5-devel

Requires:       hicolor-icon-theme
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:     smplayer
%else
Requires:       smplayer
%endif

%{?kf5_kinit_requires}
#translating kf5_kinit_requires -> Requires: kf5-kinit(x86-64)

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%setup -q
rm -rf src/qtsingleapplication/
%patch3 -p1 -b .qtsingleapplication
# correction for wrong-file-end-of-line-encoding
%{__sed} -i 's/\r//' *.txt
# fix files which are not UTF-8
iconv -f Latin1 -t UTF-8 -o Changelog.utf8 Changelog
mv Changelog.utf8 Changelog

%build
pushd src
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
* Fri Jun 19 2020 Sérgio Basto <sergio@serjux.com> - 20.6.0-1
- Update smtube to 20.6.0

* Sun Jan 26 2020 Sérgio Basto <sergio@serjux.com> - 20.1.0-1
- Update smtube to 20.1.0

* Sun Oct 27 2019 Sérgio Basto <sergio@serjux.com> - 19.6.0-1
- smtube-19.6.0

* Thu Feb 25 2016 Ricardo Villalba <rvm@users.sourceforge.net> - 16.1.0
- Initial Release
