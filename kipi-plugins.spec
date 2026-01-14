%bcond clang 1
%bcond gpod 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kipi-plugins
%define tde_prefix /opt/trinity


%define kipi-plugins %{_lib}kipi

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.6
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Image manipulation/handling plugins for KIPI aware programs [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/
#URL:		http://www.kipi-plugins.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires: make

BuildRequires: trinity-tdelibs-devel >= %{tde_version}
BuildRequires: trinity-tdepim-devel >= %{tde_version}
BuildRequires: trinity-libkdcraw-devel >= %{tde_version}
BuildRequires: trinity-libkexiv2-devel >= %{tde_version}
BuildRequires: trinity-libkipi-devel >= %{tde_version}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: nas-devel

%{!?with_clang:BuildRequires: gcc-c++}

# JPEG support
BuildRequires:  pkgconfig(libjpeg)

# EXIV2
BuildRequires:  pkgconfig(exiv2)

# GPOD (ipod) support
%{?with_gpod:BuildRequires:  pkgconfig(libgpod-1.0)}

# LCMS support
BuildRequires:  pkgconfig(lcms)

# GPHOTO2 support
BuildRequires:  pkgconfig(libgphoto2)

# TIFF support
BuildRequires:  pkgconfig(libtiff-4)

# XSLT support
BuildRequires:  pkgconfig(libxslt)

# MESA support
BuildRequires:  pkgconfig(glu)

BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xft)

# AUTOTOOLS
BuildRequires: automake autoconf libtool
BuildRequires:	%{_lib}ltdl-devel

%description
KIPI plugins (TDE Image Plugin Interface) is an effort to develop a
common plugin structure for Digikam, KPhotoAlbum (formerly known as
KimDaBa), Showimg and Gwenview.
Its aim is to share image plugins among graphic applications.

Plugins available are:

RawConverter:        Raw image converter for digital cameras
SlideShow:           Slideshow with effects ripped out from kslideshow
                     and 3D effects using OpenGL
MpegEncoder:         Create an MPEG slideshow from your images
PrintWizard:         A wizard to print images in various format
JpegLossLess:        Batch process your JPEG images without losing meta
                     information and compression
CdArchiving:         Archive your albums on CD or DVD using K3b
ScanImages:          Scanner management using Kooka
ScreenshotImages:    Snap screen based on KSnapshot and adapted to Kipi
Calendar:            Sreate calendars with images
SendImages:          Send images by email, allowing resizing
                     and recompressing before sending
RenameImages:        Batch image renamer
ConvertImages:       Batch image converter
BorderImages:        Add border to your images in batch
FilterImages:        Batch image enhancer using digital filters
ColorImages:         Batch image color enhancer
EffectImages:        Batch image transformation effects
ResizeImages:        Batch image resizer
RecompressImages:    Batch image recompressor
FindDuplicateImages: Find duplicate images in albums
TimeAdjust:          Adjust image file time and date
WallPaper:           Set your image as wallpaper
FindImages:          Find duplicate images in albums
GalleryExport:       Interface for export images collections to remote
                     Gallery (and Gallery 2) servers
FlickrExport:        Export images to a remote Flickr web service
HTMLGallery:         Export images to HTML
SimpleviewerExport:  Export images in a nice flash movie
GPSSync:             Geolocalize pictures
MetadataEdit:        Edit EXIF and IPTC pictures metadata
%if %{with gpod}
IpodExport:          Export images to an ipod device
%endif
PicasaWebExport:     Export pictures to Picasa web service


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/"*"/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --datadir=%{tde_prefix}/share \
  --libdir=%{tde_prefix}/%{_lib} \
  --mandir=%{tde_prefix}/share/man \
  --includedir=%{tde_prefix}/include/tde \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  %{?with_clang:--disable-gcc-hidden-visibility}

%__make %{?_smp_mflags}


%install
export PATH="%{tde_prefix}/bin:${PATH}"
%__make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%{tde_prefix}/bin/images2mpg
%{tde_prefix}/%{_lib}/libkipiplugins.la
%{tde_prefix}/%{_lib}/libkipiplugins.so
%{tde_prefix}/%{_lib}/libkipiplugins.so.0
%{tde_prefix}/%{_lib}/libkipiplugins.so.0.0.1
%{tde_prefix}/%{_lib}/trinity/kipiplugin_acquireimages.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_acquireimages.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_batchprocessimages.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_batchprocessimages.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_calendar.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_calendar.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_cdarchiving.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_cdarchiving.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_findimages.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_findimages.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_flickrexport.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_flickrexport.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_galleryexport.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_galleryexport.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_gpssync.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_gpssync.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_htmlexport.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_htmlexport.so
%if %{with gpod}
%{tde_prefix}/%{_lib}/trinity/kipiplugin_ipodexport.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_ipodexport.so
%endif
%{tde_prefix}/%{_lib}/trinity/kipiplugin_jpeglossless.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_jpeglossless.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_kameraklient.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_kameraklient.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_metadataedit.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_metadataedit.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_mpegencoder.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_mpegencoder.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_picasawebexport.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_picasawebexport.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_printwizard.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_printwizard.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_rawconverter.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_rawconverter.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_sendimages.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_sendimages.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_simpleviewer.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_simpleviewer.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_slideshow.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_slideshow.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_timeadjust.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_timeadjust.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_viewer.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_viewer.so
%{tde_prefix}/%{_lib}/trinity/kipiplugin_wallpaper.la
%{tde_prefix}/%{_lib}/trinity/kipiplugin_wallpaper.so
%{tde_prefix}/share/applnk/.hidden/kipi-plugins.desktop
%{tde_prefix}/share/apps/kipi/
%{tde_prefix}/share/apps/kipiplugin_batchprocessimages/
%{tde_prefix}/share/apps/kipiplugin_findimages/
%{tde_prefix}/share/apps/kipiplugin_galleryexport/
%{tde_prefix}/share/apps/kipiplugin_gpssync/
%{tde_prefix}/share/apps/kipiplugin_htmlexport/
%{tde_prefix}/share/apps/kipiplugin_jpeglossless/
%{tde_prefix}/share/apps/kipiplugin_rawconverter/
%{tde_prefix}/share/apps/kipiplugin_simpleviewerexport/
%{tde_prefix}/share/apps/kipiplugin_slideshow/
%{tde_prefix}/share/apps/kipiplugin_viewer/
%{tde_prefix}/share/config.kcfg/htmlexportconfig.kcfg
%{tde_prefix}/share/services/kipiplugin_acquireimages.desktop
%{tde_prefix}/share/services/kipiplugin_batchprocessimages.desktop
%{tde_prefix}/share/services/kipiplugin_calendar.desktop
%{tde_prefix}/share/services/kipiplugin_cdarchiving.desktop
%{tde_prefix}/share/services/kipiplugin_findimages.desktop
%{tde_prefix}/share/services/kipiplugin_flickrexport.desktop
%{tde_prefix}/share/services/kipiplugin_galleryexport.desktop
%{tde_prefix}/share/services/kipiplugin_gpssync.desktop
%{tde_prefix}/share/services/kipiplugin_htmlexport.desktop
%if %{with gpod}
%{tde_prefix}/share/services/kipiplugin_ipodexport.desktop
%endif
%{tde_prefix}/share/services/kipiplugin_jpeglossless.desktop
%{tde_prefix}/share/services/kipiplugin_kameraklient.desktop
%{tde_prefix}/share/services/kipiplugin_metadataedit.desktop
%{tde_prefix}/share/services/kipiplugin_mpegencoder.desktop
%{tde_prefix}/share/services/kipiplugin_picasawebexport.desktop
%{tde_prefix}/share/services/kipiplugin_printwizard.desktop
%{tde_prefix}/share/services/kipiplugin_rawconverter.desktop
%{tde_prefix}/share/services/kipiplugin_sendimages.desktop
%{tde_prefix}/share/services/kipiplugin_simpleviewer.desktop
%{tde_prefix}/share/services/kipiplugin_slideshow.desktop
%{tde_prefix}/share/services/kipiplugin_timeadjust.desktop
%{tde_prefix}/share/services/kipiplugin_viewer.desktop
%{tde_prefix}/share/services/kipiplugin_wallpaper.desktop
%{tde_prefix}/share/man/man1/images2mpg.1*
%{tde_prefix}/share/doc/tde/HTML/de/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/en/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/es/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/et/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/it/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/nl/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/pt_BR/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/ru/kipi-plugins/
%{tde_prefix}/share/doc/tde/HTML/sv/kipi-plugins/
%lang(ar) %{tde_prefix}/share/locale/ar/LC_MESSAGES/*.mo
%lang(be) %{tde_prefix}/share/locale/be/LC_MESSAGES/*.mo
%lang(br) %{tde_prefix}/share/locale/br/LC_MESSAGES/*.mo
%lang(ca) %{tde_prefix}/share/locale/ca/LC_MESSAGES/*.mo
%lang(cs) %{tde_prefix}/share/locale/cs/LC_MESSAGES/*.mo
%lang(cy) %{tde_prefix}/share/locale/cy/LC_MESSAGES/*.mo
%lang(da) %{tde_prefix}/share/locale/da/LC_MESSAGES/*.mo
%lang(de) %{tde_prefix}/share/locale/de/LC_MESSAGES/*.mo
%lang(el) %{tde_prefix}/share/locale/el/LC_MESSAGES/*.mo
%lang(en_GB) %{tde_prefix}/share/locale/en_GB/LC_MESSAGES/*.mo
%lang(es) %{tde_prefix}/share/locale/es/LC_MESSAGES/*.mo
%lang(et) %{tde_prefix}/share/locale/et/LC_MESSAGES/*.mo
%lang(fi) %{tde_prefix}/share/locale/fi/LC_MESSAGES/*.mo
%lang(fr) %{tde_prefix}/share/locale/fr/LC_MESSAGES/*.mo
%lang(ga) %{tde_prefix}/share/locale/ga/LC_MESSAGES/*.mo
%lang(gl) %{tde_prefix}/share/locale/gl/LC_MESSAGES/*.mo
%lang(hu) %{tde_prefix}/share/locale/hu/LC_MESSAGES/*.mo
%lang(is) %{tde_prefix}/share/locale/is/LC_MESSAGES/*.mo
%lang(it) %{tde_prefix}/share/locale/it/LC_MESSAGES/*.mo
%lang(ja) %{tde_prefix}/share/locale/ja/LC_MESSAGES/*.mo
%lang(lt) %{tde_prefix}/share/locale/lt/LC_MESSAGES/*.mo
%lang(ms) %{tde_prefix}/share/locale/ms/LC_MESSAGES/*.mo
%lang(mt) %{tde_prefix}/share/locale/mt/LC_MESSAGES/*.mo
%lang(nb) %{tde_prefix}/share/locale/nb/LC_MESSAGES/*.mo
%lang(nds) %{tde_prefix}/share/locale/nds/LC_MESSAGES/*.mo
%lang(nl) %{tde_prefix}/share/locale/nl/LC_MESSAGES/*.mo
%lang(nn) %{tde_prefix}/share/locale/nn/LC_MESSAGES/*.mo
%lang(pa) %{tde_prefix}/share/locale/pa/LC_MESSAGES/*.mo
%lang(pl) %{tde_prefix}/share/locale/pl/LC_MESSAGES/*.mo
%lang(pt) %{tde_prefix}/share/locale/pt/LC_MESSAGES/*.mo
%lang(pt_BR) %{tde_prefix}/share/locale/pt_BR/LC_MESSAGES/*.mo
%lang(ru) %{tde_prefix}/share/locale/ru/LC_MESSAGES/*.mo
%lang(rw) %{tde_prefix}/share/locale/rw/LC_MESSAGES/*.mo
%lang(sk) %{tde_prefix}/share/locale/sk/LC_MESSAGES/*.mo
%lang(sr) %{tde_prefix}/share/locale/sr/LC_MESSAGES/*.mo
%lang(sr@Latn) %{tde_prefix}/share/locale/sr@Latn/LC_MESSAGES/*.mo
%lang(sv) %{tde_prefix}/share/locale/sv/LC_MESSAGES/*.mo
%lang(ta) %{tde_prefix}/share/locale/ta/LC_MESSAGES/*.mo
%lang(th) %{tde_prefix}/share/locale/th/LC_MESSAGES/*.mo
%lang(tr) %{tde_prefix}/share/locale/tr/LC_MESSAGES/*.mo
%lang(uk) %{tde_prefix}/share/locale/uk/LC_MESSAGES/*.mo
%lang(zh_CN) %{tde_prefix}/share/locale/zh_CN/LC_MESSAGES/*.mo

