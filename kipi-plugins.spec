#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg kipi-plugins
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define kipi-plugins %{_lib}kipi
%else
%define kipi-plugins kipi-plugins
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.6
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Image manipulation/handling plugins for KIPI aware programs [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/
#URL:		http://www.kipi-plugins.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires: autoconf automake libtool 
BuildRequires: trinity-tdelibs-devel >= %{tde_version}
BuildRequires: trinity-tdepim-devel >= %{tde_version}
BuildRequires: trinity-libkdcraw-devel >= %{tde_version}
BuildRequires: trinity-libkexiv2-devel >= %{tde_version}
BuildRequires: trinity-libkipi-devel >= %{tde_version}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext
%if "%{?toolchain}" != "clang"
BuildRequires: gcc-c++
%endif

# JPEG support
BuildRequires:  pkgconfig(libjpeg)

# EXIV2
BuildRequires:  pkgconfig(exiv2)

# GPOD (ipod) support
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?rhel} == 8 || 0%{?fedora} || 0%{?mdkversion} || 0%{?mgaversion} || 0%{?suse_version}
%define with_gpod 1
BuildRequires:  pkgconfig(libgpod-1.0)
%endif

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
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}ltdl-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 5 || 0%{?suse_version} >= 1220
BuildRequires:	libtool-ltdl-devel
%endif

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
%if 0%{?with_gpod}
IpodExport:          Export images to an ipod device
%endif
PicasaWebExport:     Export pictures to Picasa web service

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/"*"/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%{tde_bindir}/images2mpg
%{tde_libdir}/libkipiplugins.la
%{tde_libdir}/libkipiplugins.so
%{tde_libdir}/libkipiplugins.so.0
%{tde_libdir}/libkipiplugins.so.0.0.1
%{tde_tdelibdir}/kipiplugin_acquireimages.la
%{tde_tdelibdir}/kipiplugin_acquireimages.so
%{tde_tdelibdir}/kipiplugin_batchprocessimages.la
%{tde_tdelibdir}/kipiplugin_batchprocessimages.so
%{tde_tdelibdir}/kipiplugin_calendar.la
%{tde_tdelibdir}/kipiplugin_calendar.so
%{tde_tdelibdir}/kipiplugin_cdarchiving.la
%{tde_tdelibdir}/kipiplugin_cdarchiving.so
%{tde_tdelibdir}/kipiplugin_findimages.la
%{tde_tdelibdir}/kipiplugin_findimages.so
%{tde_tdelibdir}/kipiplugin_flickrexport.la
%{tde_tdelibdir}/kipiplugin_flickrexport.so
%{tde_tdelibdir}/kipiplugin_galleryexport.la
%{tde_tdelibdir}/kipiplugin_galleryexport.so
%{tde_tdelibdir}/kipiplugin_gpssync.la
%{tde_tdelibdir}/kipiplugin_gpssync.so
%{tde_tdelibdir}/kipiplugin_htmlexport.la
%{tde_tdelibdir}/kipiplugin_htmlexport.so
%if 0%{?with_gpod}
%{tde_tdelibdir}/kipiplugin_ipodexport.la
%{tde_tdelibdir}/kipiplugin_ipodexport.so
%endif
%{tde_tdelibdir}/kipiplugin_jpeglossless.la
%{tde_tdelibdir}/kipiplugin_jpeglossless.so
%{tde_tdelibdir}/kipiplugin_kameraklient.la
%{tde_tdelibdir}/kipiplugin_kameraklient.so
%{tde_tdelibdir}/kipiplugin_metadataedit.la
%{tde_tdelibdir}/kipiplugin_metadataedit.so
%{tde_tdelibdir}/kipiplugin_mpegencoder.la
%{tde_tdelibdir}/kipiplugin_mpegencoder.so
%{tde_tdelibdir}/kipiplugin_picasawebexport.la
%{tde_tdelibdir}/kipiplugin_picasawebexport.so
%{tde_tdelibdir}/kipiplugin_printwizard.la
%{tde_tdelibdir}/kipiplugin_printwizard.so
%{tde_tdelibdir}/kipiplugin_rawconverter.la
%{tde_tdelibdir}/kipiplugin_rawconverter.so
%{tde_tdelibdir}/kipiplugin_sendimages.la
%{tde_tdelibdir}/kipiplugin_sendimages.so
%{tde_tdelibdir}/kipiplugin_simpleviewer.la
%{tde_tdelibdir}/kipiplugin_simpleviewer.so
%{tde_tdelibdir}/kipiplugin_slideshow.la
%{tde_tdelibdir}/kipiplugin_slideshow.so
%{tde_tdelibdir}/kipiplugin_timeadjust.la
%{tde_tdelibdir}/kipiplugin_timeadjust.so
%{tde_tdelibdir}/kipiplugin_viewer.la
%{tde_tdelibdir}/kipiplugin_viewer.so
%{tde_tdelibdir}/kipiplugin_wallpaper.la
%{tde_tdelibdir}/kipiplugin_wallpaper.so
%{tde_datadir}/applnk/.hidden/kipi-plugins.desktop
%{tde_datadir}/apps/kipi/
%{tde_datadir}/apps/kipiplugin_batchprocessimages/
%{tde_datadir}/apps/kipiplugin_findimages/
%{tde_datadir}/apps/kipiplugin_galleryexport/
%{tde_datadir}/apps/kipiplugin_gpssync/
%{tde_datadir}/apps/kipiplugin_htmlexport/
%{tde_datadir}/apps/kipiplugin_jpeglossless/
%{tde_datadir}/apps/kipiplugin_rawconverter/
%{tde_datadir}/apps/kipiplugin_simpleviewerexport/
%{tde_datadir}/apps/kipiplugin_slideshow/
%{tde_datadir}/apps/kipiplugin_viewer/
%{tde_datadir}/config.kcfg/htmlexportconfig.kcfg
%{tde_datadir}/services/kipiplugin_acquireimages.desktop
%{tde_datadir}/services/kipiplugin_batchprocessimages.desktop
%{tde_datadir}/services/kipiplugin_calendar.desktop
%{tde_datadir}/services/kipiplugin_cdarchiving.desktop
%{tde_datadir}/services/kipiplugin_findimages.desktop
%{tde_datadir}/services/kipiplugin_flickrexport.desktop
%{tde_datadir}/services/kipiplugin_galleryexport.desktop
%{tde_datadir}/services/kipiplugin_gpssync.desktop
%{tde_datadir}/services/kipiplugin_htmlexport.desktop
%if 0%{?with_gpod}
%{tde_datadir}/services/kipiplugin_ipodexport.desktop
%endif
%{tde_datadir}/services/kipiplugin_jpeglossless.desktop
%{tde_datadir}/services/kipiplugin_kameraklient.desktop
%{tde_datadir}/services/kipiplugin_metadataedit.desktop
%{tde_datadir}/services/kipiplugin_mpegencoder.desktop
%{tde_datadir}/services/kipiplugin_picasawebexport.desktop
%{tde_datadir}/services/kipiplugin_printwizard.desktop
%{tde_datadir}/services/kipiplugin_rawconverter.desktop
%{tde_datadir}/services/kipiplugin_sendimages.desktop
%{tde_datadir}/services/kipiplugin_simpleviewer.desktop
%{tde_datadir}/services/kipiplugin_slideshow.desktop
%{tde_datadir}/services/kipiplugin_timeadjust.desktop
%{tde_datadir}/services/kipiplugin_viewer.desktop
%{tde_datadir}/services/kipiplugin_wallpaper.desktop
%{tde_mandir}/man1/images2mpg.1*
%{tde_tdedocdir}/HTML/de/kipi-plugins/
%{tde_tdedocdir}/HTML/en/kipi-plugins/
%{tde_tdedocdir}/HTML/es/kipi-plugins/
%{tde_tdedocdir}/HTML/et/kipi-plugins/
%{tde_tdedocdir}/HTML/it/kipi-plugins/
%{tde_tdedocdir}/HTML/nl/kipi-plugins/
%{tde_tdedocdir}/HTML/pt_BR/kipi-plugins/
%{tde_tdedocdir}/HTML/ru/kipi-plugins/
%{tde_tdedocdir}/HTML/sv/kipi-plugins/
%lang(ar) %{tde_datadir}/locale/ar/LC_MESSAGES/*.mo
%lang(be) %{tde_datadir}/locale/be/LC_MESSAGES/*.mo
%lang(br) %{tde_datadir}/locale/br/LC_MESSAGES/*.mo
%lang(ca) %{tde_datadir}/locale/ca/LC_MESSAGES/*.mo
%lang(cs) %{tde_datadir}/locale/cs/LC_MESSAGES/*.mo
%lang(cy) %{tde_datadir}/locale/cy/LC_MESSAGES/*.mo
%lang(da) %{tde_datadir}/locale/da/LC_MESSAGES/*.mo
%lang(de) %{tde_datadir}/locale/de/LC_MESSAGES/*.mo
%lang(el) %{tde_datadir}/locale/el/LC_MESSAGES/*.mo
%lang(en_GB) %{tde_datadir}/locale/en_GB/LC_MESSAGES/*.mo
%lang(es) %{tde_datadir}/locale/es/LC_MESSAGES/*.mo
%lang(et) %{tde_datadir}/locale/et/LC_MESSAGES/*.mo
%lang(fi) %{tde_datadir}/locale/fi/LC_MESSAGES/*.mo
%lang(fr) %{tde_datadir}/locale/fr/LC_MESSAGES/*.mo
%lang(ga) %{tde_datadir}/locale/ga/LC_MESSAGES/*.mo
%lang(gl) %{tde_datadir}/locale/gl/LC_MESSAGES/*.mo
%lang(hu) %{tde_datadir}/locale/hu/LC_MESSAGES/*.mo
%lang(is) %{tde_datadir}/locale/is/LC_MESSAGES/*.mo
%lang(it) %{tde_datadir}/locale/it/LC_MESSAGES/*.mo
%lang(ja) %{tde_datadir}/locale/ja/LC_MESSAGES/*.mo
%lang(lt) %{tde_datadir}/locale/lt/LC_MESSAGES/*.mo
%lang(ms) %{tde_datadir}/locale/ms/LC_MESSAGES/*.mo
%lang(mt) %{tde_datadir}/locale/mt/LC_MESSAGES/*.mo
%lang(nb) %{tde_datadir}/locale/nb/LC_MESSAGES/*.mo
%lang(nds) %{tde_datadir}/locale/nds/LC_MESSAGES/*.mo
%lang(nl) %{tde_datadir}/locale/nl/LC_MESSAGES/*.mo
%lang(nn) %{tde_datadir}/locale/nn/LC_MESSAGES/*.mo
%lang(pa) %{tde_datadir}/locale/pa/LC_MESSAGES/*.mo
%lang(pl) %{tde_datadir}/locale/pl/LC_MESSAGES/*.mo
%lang(pt) %{tde_datadir}/locale/pt/LC_MESSAGES/*.mo
%lang(pt_BR) %{tde_datadir}/locale/pt_BR/LC_MESSAGES/*.mo
%lang(ru) %{tde_datadir}/locale/ru/LC_MESSAGES/*.mo
%lang(rw) %{tde_datadir}/locale/rw/LC_MESSAGES/*.mo
%lang(sk) %{tde_datadir}/locale/sk/LC_MESSAGES/*.mo
%lang(sr) %{tde_datadir}/locale/sr/LC_MESSAGES/*.mo
%lang(sr@Latn) %{tde_datadir}/locale/sr@Latn/LC_MESSAGES/*.mo
%lang(sv) %{tde_datadir}/locale/sv/LC_MESSAGES/*.mo
%lang(ta) %{tde_datadir}/locale/ta/LC_MESSAGES/*.mo
%lang(th) %{tde_datadir}/locale/th/LC_MESSAGES/*.mo
%lang(tr) %{tde_datadir}/locale/tr/LC_MESSAGES/*.mo
%lang(uk) %{tde_datadir}/locale/uk/LC_MESSAGES/*.mo
%lang(zh_CN) %{tde_datadir}/locale/zh_CN/LC_MESSAGES/*.mo

