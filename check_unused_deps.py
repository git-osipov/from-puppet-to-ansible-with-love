#!/usr/bin/env python3
"""
Script to check for unused dependencies in the project.
"""

import os
import re
import glob

def check_puppet_modules():
    """Check if Puppet modules are actually used in manifests"""
    print("=== Checking Puppet Module Usage ===")
    
    # Read Puppetfile to get installed modules
    puppetfile_path = "Puppetfile"
    if not os.path.exists(puppetfile_path):
        print("No Puppetfile found")
        return
    
    with open(puppetfile_path, 'r') as f:
        puppetfile_content = f.read()
    
    # Extract module names
    module_pattern = r"mod\s+['\"]([^'\"]+)['\"]"
    modules = re.findall(module_pattern, puppetfile_content)
    
    print(f"Found modules in Puppetfile: {modules}")
    
    # Check usage in manifests
    manifest_files = glob.glob("puppet/manifests/*.pp")
    all_manifest_content = ""
    
    for manifest in manifest_files:
        with open(manifest, 'r') as f:
            all_manifest_content += f.read() + "\n"
    
    used_modules = set()
    for module in modules:
        module_name = module.split('/')[-1]  # Get just the module name part
        
        # Check for various usage patterns
        patterns = [
            rf"\b{module_name}::",  # Class/resource usage
            rf"include\s+{module_name}",  # Include statements
            rf"class\s*{{\s*['\"]?{module_name}",  # Class declarations
            rf"require\s+{module_name}",  # Require statements
        ]
        
        for pattern in patterns:
            if re.search(pattern, all_manifest_content, re.IGNORECASE):
                used_modules.add(module)
                break
    
    unused_modules = set(modules) - used_modules
    
    print(f"Used modules: {sorted(used_modules)}")
    print(f"Potentially unused modules: {sorted(unused_modules)}")
    
    return unused_modules

def check_ansible_collections():
    """Check if Ansible collections are actually used in playbooks/roles"""
    print("\n=== Checking Ansible Collection Usage ===")
    
    # Read requirements.yml to get installed collections
    requirements_path = "ansible/requirements.yml"
    if not os.path.exists(requirements_path):
        print("No requirements.yml found")
        return
    
    import yaml
    with open(requirements_path, 'r') as f:
        requirements = yaml.safe_load(f)
    
    collections = []
    if 'collections' in requirements:
        for collection in requirements['collections']:
            if isinstance(collection, dict) and 'name' in collection:
                collections.append(collection['name'])
            elif isinstance(collection, str):
                collections.append(collection)
    
    print(f"Found collections in requirements.yml: {collections}")
    
    # Check usage in playbooks and roles
    yaml_files = []
    yaml_files.extend(glob.glob("ansible/**/*.yml", recursive=True))
    yaml_files.extend(glob.glob("ansible/**/*.yaml", recursive=True))
    
    all_ansible_content = ""
    for yaml_file in yaml_files:
        if yaml_file != requirements_path:  # Skip the requirements file itself
            with open(yaml_file, 'r') as f:
                all_ansible_content += f.read() + "\n"
    
    used_collections = set()
    for collection in collections:
        # Check for FQCN usage (e.g., ansible.posix.acl, community.general.package)
        if re.search(rf"\b{re.escape(collection)}\.", all_ansible_content):
            used_collections.add(collection)
    
    unused_collections = set(collections) - used_collections
    
    print(f"Used collections: {sorted(used_collections)}")
    print(f"Potentially unused collections: {sorted(unused_collections)}")
    
    return unused_collections

def check_ruby_gems():
    """Check if Ruby gems are actually used"""
    print("\n=== Checking Ruby Gem Usage ===")
    
    gemfile_path = "Gemfile"
    if not os.path.exists(gemfile_path):
        print("No Gemfile found")
        return
    
    with open(gemfile_path, 'r') as f:
        gemfile_content = f.read()
    
    # Extract gem names
    gem_pattern = r"gem\s+['\"]([^'\"]+)['\"]"
    gems = re.findall(gem_pattern, gemfile_content)
    
    print(f"Found gems in Gemfile: {gems}")
    
    # Check if gems are used in Rakefile or other Ruby files
    ruby_files = glob.glob("*.rb") + glob.glob("**/*.rb", recursive=True)
    all_ruby_content = ""
    
    for ruby_file in ruby_files:
        with open(ruby_file, 'r') as f:
            all_ruby_content += f.read() + "\n"
    
    used_gems = set()
    for gem in gems:
        # Check for require statements or direct usage
        patterns = [
            rf"require\s+['\"]?{gem}['\"]?",
            rf"require\s+['\"]?{gem.replace('-', '/')}['\"]?",  # Handle gems with dashes
        ]
        
        for pattern in patterns:
            if re.search(pattern, all_ruby_content):
                used_gems.add(gem)
                break
    
    # Some gems are used implicitly (like puppet, facter)
    implicit_gems = {'puppet', 'facter', 'r10k'}
    used_gems.update(gem for gem in gems if gem in implicit_gems)
    
    unused_gems = set(gems) - used_gems
    
    print(f"Used gems: {sorted(used_gems)}")
    print(f"Potentially unused gems: {sorted(unused_gems)}")
    
    return unused_gems

def main():
    """Main function"""
    print("Checking for unused dependencies...\n")
    
    unused_puppet = check_puppet_modules()
    unused_ansible = check_ansible_collections()
    unused_ruby = check_ruby_gems()
    
    print("\n=== Summary ===")
    if unused_puppet:
        print(f"Unused Puppet modules: {sorted(unused_puppet)}")
    if unused_ansible:
        print(f"Unused Ansible collections: {sorted(unused_ansible)}")
    if unused_ruby:
        print(f"Unused Ruby gems: {sorted(unused_ruby)}")
    
    if not (unused_puppet or unused_ansible or unused_ruby):
        print("No obviously unused dependencies found!")

if __name__ == '__main__':
    main()