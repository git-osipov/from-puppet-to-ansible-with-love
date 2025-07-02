# Install ansible-lint venv (python 3.8)
class ansible_lint_venv (
  Enum[latest,absent] $ansible_lint_venv_pkg_status = latest,
) {
  package {'ansible-lint-venv':
    ensure => $ansible_lint_venv_pkg_status
  }
}
