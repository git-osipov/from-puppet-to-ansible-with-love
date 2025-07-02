# install bsign and fly-fm-bsign
class bsign (
  Enum[present, latest, absent] $bsign_pkg_status = 'present',
  Enum[present, latest, absent] $fly_fm_bsign_pkg_status = 'present',
) {
  package { 'bsign':
    ensure => $bsign_pkg_status,
  }
  package { 'fly-fm-bsign':
    ensure => $fly_fm_bsign_pkg_status,
  }
}
