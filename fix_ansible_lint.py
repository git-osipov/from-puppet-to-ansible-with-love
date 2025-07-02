#!/usr/bin/env python3
"""
Script to fix common ansible-lint issues in the Ansible roles and playbooks.
"""

import os
import re
import glob

def fix_yaml_truthy(content):
    """Fix YAML truthy values (yes/no -> true/false)"""
    # Replace 'yes' with 'true' and 'no' with 'false' in YAML boolean contexts
    content = re.sub(r'\bbecome:\s+yes\b', 'become: true', content)
    content = re.sub(r'\bbecome:\s+no\b', 'become: false', content)
    content = re.sub(r'\benabled:\s+yes\b', 'enabled: true', content)
    content = re.sub(r'\benabled:\s+no\b', 'enabled: false', content)
    content = re.sub(r'\bstate:\s+yes\b', 'state: true', content)
    content = re.sub(r'\bstate:\s+no\b', 'state: false', content)
    return content

def fix_fqcn(content):
    """Fix FQCN issues by adding ansible.builtin. prefix to core modules"""
    core_modules = [
        'package', 'apt', 'yum', 'dnf', 'file', 'copy', 'template', 
        'service', 'systemd', 'user', 'group', 'lineinfile', 'blockinfile',
        'pip', 'package_facts', 'stat', 'debug', 'fail', 'assert',
        'set_fact', 'include_vars', 'include_tasks', 'import_tasks'
    ]
    
    for module in core_modules:
        # Replace module: with ansible.builtin.module:
        pattern = rf'^(\s+){module}:$'
        replacement = rf'\1ansible.builtin.{module}:'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Fix ansible.posix.acl
    content = re.sub(r'^(\s+)acl:$', r'\1ansible.posix.acl:', content, flags=re.MULTILINE)
    
    return content

def fix_trailing_spaces(content):
    """Remove trailing spaces"""
    lines = content.split('\n')
    fixed_lines = [line.rstrip() for line in lines]
    return '\n'.join(fixed_lines)

def ensure_newline_at_end(content):
    """Ensure file ends with newline"""
    if content and not content.endswith('\n'):
        content += '\n'
    return content

def fix_meta_files(content):
    """Fix meta/main.yml files"""
    # Replace None with a proper company name
    content = re.sub(r'company:\s*None', 'company: "Example Company"', content)
    return content

def process_file(filepath):
    """Process a single file"""
    print(f"Processing {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_yaml_truthy(content)
    content = fix_fqcn(content)
    content = fix_trailing_spaces(content)
    content = ensure_newline_at_end(content)
    
    if 'meta/main.yml' in filepath:
        content = fix_meta_files(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Fixed {filepath}")
    else:
        print(f"  No changes needed for {filepath}")

def main():
    """Main function"""
    # Find all YAML files in ansible directory
    yaml_files = []
    yaml_files.extend(glob.glob('ansible/**/*.yml', recursive=True))
    yaml_files.extend(glob.glob('ansible/**/*.yaml', recursive=True))
    
    for filepath in yaml_files:
        if os.path.isfile(filepath):
            process_file(filepath)

if __name__ == '__main__':
    main()