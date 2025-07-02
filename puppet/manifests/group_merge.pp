# create local group with name and id of domain group 

# Class: group_merge
#
# usage 
#class {'group_merge':
#      groups => { 'vboxusers' => { 
#                      ensure => present, 
#                      gid => '10050' }, 
#                    'libvirt' => { 
#                      ensure => absent,
#                      gid => '10051'}}
#     }
class group_merge (
  Hash $groups,
) {
  $groups.each | $group, $params | {
    file_line { $group:
      ensure => $params[ensure],
      line   => "${group}:x:${params[gid]}:",
      match  => "^${group}:x",
      path   => '/etc/group',
    }
  }
}
