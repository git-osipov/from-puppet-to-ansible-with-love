# install assistant
class assistant (
  Enum[present, latest, absent] $assistant_pkg_status = 'latest',
  Boolean $assistant_service_enable = true,
) {
  package { 'assistant':
    ensure => $assistant_pkg_status,
  }

  $assistant_service_ensure = $assistant_service_enable ? { true => 'running', false => 'stopped' }

  service { 'assistant':
    ensure   => $assistant_service_ensure,
    enable   => $assistant_service_enable,
    provider => 'systemd',
  }
}
