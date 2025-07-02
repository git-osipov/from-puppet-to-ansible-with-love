#facl
# class facl (
# Hash $files = {'test'                      => { member     => 'vagrant',
#                                                 location   => '/home/vagrant/02/3',
#                                                 permission => '---',
#                                                 type       => 'group'
#                                               },
#               'python2.7'                  => { member     => 'bamboo-agent',
#                                                 location   => '/home/vagrant/02/4',
#                                                 permission => 'rwx',
#                                                 type       => 'user'
#                                               },
#               },
# )

class facl (
    Hash $files = {},
  ){
$files.each | $name, $params | {
    posix_acl { $params[location]:
      action     => set,
      permission => join([$params['type'],":",$params[member],":",$params[permission]]),
      provider   => posixacl,
      recursive  => false,
    }
}
}
