# Install iperf
class iperf (
  String $iperf_status = '2.0.5+dfsg1-2'
) {
  Class['configure_apt']~>Class['iperf']
  package { 'iperf':
    ensure => $iperf_status,
  }
}
