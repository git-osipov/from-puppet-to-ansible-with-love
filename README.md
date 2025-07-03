# From Puppet to Ansible with Love

A practical guide and reference for migrating from Puppet to Ansible, with side-by-side examples of equivalent implementations.

## Overview

This repository demonstrates how to migrate infrastructure as code from Puppet to Ansible. It provides parallel implementations of common system administration tasks in both tools, allowing for direct comparison and easier migration.

## Project Structure

- `puppet/` - Contains Puppet manifests
  - `puppet/manifests/` - Puppet class definitions
- `ansible/` - Contains Ansible configuration
  - `ansible/playbooks/` - Task-specific playbooks
  - `ansible/roles/` - Reusable Ansible roles
  - `ansible/inventory/` - Host definitions
  - `ansible/tests/` - Test configurations

## Examples

The repository includes several examples of common system administration tasks implemented in both Puppet and Ansible. Each example shows the equivalent implementation in both Puppet and Ansible:

### ACL Management

**Puppet Implementation:**
```puppet
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
```

**Ansible Implementation:**
```yaml
---
# ACL management playbook
- name: Manage POSIX ACLs
  hosts: all
  become: true
  vars:
    files:
      test:
        member: vagrant
        location: /home/vagrant/02/3
        permission: "---"
        type: group
      python2.7:
        member: bamboo-agent
        location: /home/vagrant/02/4
        permission: rwx
        type: user
  roles:
    - facl
```

### Group Management

**Puppet Implementation:**
```puppet
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
```

**Ansible Implementation:**
```yaml
---
# Group management playbook
- name: Manage local groups
  hosts: all
  become: true
  vars:
    local_groups:
      vboxusers:
        ensure: present
        gid: "10050"
      libvirt:
        ensure: present
        gid: "10051"
  roles:
    - group_merge
```

## Dependencies

### Puppet Dependencies

See the [Puppetfile](Puppetfile) for current Puppet module dependencies:

```puppet
forge 'https://forge.puppet.com'

# Core dependencies
mod 'puppetlabs/acl', '5.0.3'
```

### Ansible Dependencies

See [ansible/requirements.yml](ansible/requirements.yml) for current Ansible collection dependencies:

```yaml
---
# Ansible Galaxy requirements
collections:
  - name: ansible.posix
    version: ">=2.0.0"

roles: []
```

## Tool Versions

- **Puppet**: 8.10.0 (latest stable)
- **Ansible**: 11.7.0 with ansible-core 2.18.6 (latest stable)
- **ansible-lint**: 25.6.1 (latest)
- **Python**: 3.12.11
- **Ruby**: 3.1.2

For a detailed summary of dependency updates, see the [Dependency Update Summary](DEPENDENCY_UPDATE_SUMMARY.md).

## Usage

### Running Puppet Manifests

```bash
puppet apply puppet/manifests/acl.pp
```

### Running Ansible Playbooks

```bash
ansible-playbook -i ansible/inventory ansible/playbooks/acl.yml
```

## Testing and Validation

### Puppet Validation

```bash
puppet parser validate puppet/manifests/*.pp
puppet-lint puppet/manifests/
```

### Ansible Validation

```bash
ansible-lint ansible/playbooks/*.yml
ansible-playbook --syntax-check ansible/playbooks/*.yml
```

## Utility Scripts

This repository includes several utility scripts to help with maintenance and analysis:

- [check_unused_deps.py](check_unused_deps.py) - Analyzes dependencies to identify unused modules
- [fix_ansible_lint.py](fix_ansible_lint.py) - Helps fix common ansible-lint issues automatically

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).