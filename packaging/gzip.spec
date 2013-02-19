Name:       gzip
Summary:    The GNU data compression program
Version:    1.3.14
Release:    2
Group:      Applications/File
License:    GPLv2 and GFDL
URL:        http://www.gzip.org/
Source0:    ftp://alpha.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Source1001: packaging/gzip.manifest 
Patch0:     gzip-1.3.12-openbsd-owl-tmp.patch
Patch1:     gzip-1.3.5-zforce.patch
Patch2:     gzip-1.3.9-stderr.patch
Patch3:     gzip-1.3.10-zgreppipe.patch
Patch4:     gzip-1.3.9-rsync.patch
Patch5:     gzip-1.3.9-addsuffix.patch
Patch6:     gzip-1.3.5-cve-2006-4338.patch
Patch7:     gzip-1.3.9-cve-2006-4337.patch
Patch8:     gzip-1.3.5-cve-2006-4337_len.patch
Patch9:     gzip-1.3.12-cve-2010-0001.patch
Requires:   /bin/mktemp


%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.



%package -n zless
Summary:    file perusal filter for crt viewing of compressed text
License:    GPLv2
Group:      Applications/File
Requires:   %{name} = %{version}-%{release}
Requires:   /usr/bin/less

%description -n zless
Zless  is  a filter which allows examination of compressed or plain text files one
screenful at a time on a soft-copy terminal.  It is the equivalent of setting the
environment variable LESSOPEN to '|gzip -cdfq -- %s', and the environment variable
LESSMETACHARS to and then running less.  However,  enough people seem to think that
having the command zless available is important to be worth providing it.



%prep
%setup -q -n %{name}-%{version}

# gzip-1.3.12-openbsd-owl-tmp.patch
%patch0 -p1
# gzip-1.3.5-zforce.patch
%patch1 -p1
# gzip-1.3.9-stderr.patch
%patch2 -p1
# gzip-1.3.10-zgreppipe.patch
%patch3 -p1
# gzip-1.3.9-rsync.patch
%patch4 -p1
# gzip-1.3.9-addsuffix.patch
%patch5 -p1
# gzip-1.3.5-cve-2006-4338.patch
%patch6 -p1
# gzip-1.3.9-cve-2006-4337.patch
%patch7 -p1
# gzip-1.3.5-cve-2006-4337_len.patch
%patch8 -p1
# gzip-1.3.12-cve-2010-0001.patch
%patch9 -p1

%build
cp %{SOURCE1001} .
export CPPFLAGS="-DHAVE_LSTAT"

%configure --disable-static \
    --bindir=/bin

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_bindir}
ln -sf ../../bin/gzip %{buildroot}%{_bindir}/gzip
ln -sf ../../bin/gunzip %{buildroot}%{_bindir}/gunzip

for i in  zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
mv %{buildroot}/bin/$i %{buildroot}%{_bindir}/$i
done

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -f %{buildroot}%{_infodir}/dir
# uncompress is a part of ncompress package
rm -f %{buildroot}/bin/uncompress

mkdir -p $RPM_BUILD_ROOT%{_datadir}/license
for keyword in LICENSE COPYING COPYRIGHT;
do
	for file in `find %{_builddir} -name $keyword`;
	do
		cat $file >> $RPM_BUILD_ROOT%{_datadir}/license/%{name};
		echo "";
	done;
done

%docs_package

%files
%manifest gzip.manifest
%defattr(-,root,root,-)
%{_datadir}/license/%{name}
/bin/*
%{_bindir}/gzip
%{_bindir}/gunzip
%{_bindir}/zcmp
%{_bindir}/zegrep
%{_bindir}/zforce
%{_bindir}/znew
%{_bindir}/gzexe
%{_bindir}/zdiff
%{_bindir}/zfgrep
%{_bindir}/zgrep
%{_bindir}/zmore


%files -n zless
%manifest gzip.manifest
%defattr(-,root,root,-)
%{_bindir}/zless

