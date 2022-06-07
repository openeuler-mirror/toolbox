Name:          toolbox
Version:       0.0.99

%global goipath github.com/containers/%{name}

Release:       2
Summary:       Unprivileged development environment

License:       ASL 2.0
URL:           https://github.com/containers/toolbox

Source0:       toolbox-0.0.99.3.tar.xz
Source1:       https://github.com/cpuguy83/go-md2man/archive/v1.0.10.tar.gz

BuildRequires: golang >= 1.13 meson
BuildRequires: pkgconfig(bash-completion) systemd

Requires:      podman >= 1.4.0


%description
Toolbox is a tool for Linux operating systems, which allows the use of
containerized command line environments. It is built on top of Podman and
other standard container technologies from OCI.


%package       tests
Summary:       Tests for toolbox.

Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   tests
The toolbox-tests package contains system tests for toolbox.


%prep
%setup -q

GOBUILDDIR="$(pwd)/_build"
GOSOURCEDIR="$(pwd)"
if [[ ! -e "$GOBUILDDIR/bin" ]] ; then
  install -m 0755 -vd "$GOBUILDDIR/bin"
fi
if [[ ! -e "$GOBUILDDIR/src/%{goipath}" ]] ; then
  install -m 0755 -vd "$(dirname $GOBUILDDIR/src/%{goipath})"
  ln -fs "$GOSOURCEDIR" "$GOBUILDDIR/src/%{goipath}"
fi
cd "$GOBUILDDIR/src/%{goipath}"

tar -xf %SOURCE1

%build
GO_MD2MAN_PATH="$(pwd)%{_bindir}"
mkdir -p _build/bin $GO_MD2MAN_PATH
cd go-md2man-*
go build -mod=vendor -o ../_build/bin/go-md2man .
cp ../_build/bin/go-md2man $GO_MD2MAN_PATH/go-md2man
export PATH=$GO_MD2MAN_PATH:$PATH
cd -

export GO111MODULE=off
GOBUILDDIR="$(pwd)/_build"
export GOPATH="$GOBUILDDIR:%{gopath}"
export CGO_CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
ln -s src/cmd cmd
ln -s src/pkg pkg
ln -s src/vendor vendor
%meson --buildtype=plain -Dprofile_dir=%{_sysconfdir}/profile.d
%meson_build


%install
%meson_install


%files
%doc CODE-OF-CONDUCT.md NEWS README.md SECURITY.md
%license COPYING
%{_bindir}/%{name}
%{_datadir}/bash-completion
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-*.1*
%{_sysconfdir}/profile.d/%{name}.sh
%{_tmpfilesdir}/%{name}.conf

%files tests
%{_datadir}/%{name}

%changelog
* Tue Jun 07 2022 fushanqing <fushanqing@kylinos.cn> - 0.0.99.3-2
- update Source0

* Thu Feb 10 2022 duyiwei <duyiwei@kylinos.cn> - 0.0.99.3-1
- Package init
