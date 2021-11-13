#!/bin/bash

pkgver='1.0'
install_root=${install_root:-""}

set -e
# shellcheck disable=SC2015
[ "$install_root" != "" ] && {
  mkdir -p "$install_root"/usr/{bin,share/{applications,pixmaps,insta/icon_status},doc/insta-"$pkgver"}
} || {
  mkdir -p /usr/{share/insta/icon_status,doc/insta-"$pkgver"}
}

install -Dm 0644 appdata/insta.svg "$install_root"/usr/share/pixmaps
install -Dm 0644 appdata/insta.desktop "$install_root"/usr/share/applications
install -Dm 0644 icon_status/* "$install_root"/usr/share/insta/icon_status

cp -a ChangeLog LICENSE README.md "$install_root"/usr/doc/insta-"$pkgver"
cp -Tr src "$install_root"/usr/share/insta

echo "#!/bin/bash
cd /usr/share/insta
python3 insta.py" > "$install_root"/usr/bin/insta

chmod 755 "$install_root"/usr/bin/insta
exit 0
