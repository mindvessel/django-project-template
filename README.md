# Django 4.2 Project Template

Replace this README file with your own project's info.

## How to use it

To use this repository as a project template for Django, use the following command to
create your Django project, replacing URL and PROJECT_NAME:

    django-admin startproject --template URL -e env,ini,py -x __pycache__,.git PROJECT_NAME

## Why to use it

Django's built-in project template is very minimalistic. In practice, every time I start
a new Django project, there are dozens of changes and additions I must make to the
repository to make it a "complete" project, even before writing any custom code. This
template adds those changes to save time.

This template is opinionated. It is not intended to cover all use cases or workflows. It
is optimized for solo projects and small teams, and incorporates the best practices I
have discovered in over a decade of Django development. The structure is designed to
ease long term maintenance, providing scripts for common tasks that otherwise might
require complex commands, extra research, etc.

### Common Dependencies and Dependency Management

Django requires Pillow to use ImageField, and docutils to use Admin Docs, but these are
not installed with a default Django setup, and the default template does not include a
requirements.txt.

This template includes requirements files for both production and local development,
adding the following dependencies:

- Django 4.2.x – This template is specifically designed for Django 4.2 LTS.
- Pillow – For ImageField support.
- docutils – For Django Admin Docs support (which is enabled by default in this
  template)
- django-environ – Environment-specific settings are pulled from the process
  environment. This prevents having to juggle multiple settings files as in other
  templates, and reduces the risk that you will accidentally leak secrets that might be
  stored in one of those settings files. An `example.env` file is included. Copy this to
  `.env` to quickly setup your local dev environment variables.
- django-extensions – This has been promoted from an optional dev dependency to a hard
  dependency. It provides many useful management commands, and the base models also have
  good utility. We use its `validate_templates` command to check template syntax, and
  its `shell_plus` is also useful.
- django-rich – Provides enhanced output from the test runner, as well as a base for
  management commands that gives you rich terminal output.
- gunicorn and setproctitle – For production deployment. Comment these out if you prefer
  to use a different WSGI server.
- pip-tools – Included in the dev dependencies for managing production requirements.

Dependencies are listed in a `requirements.in` file. Use `pip-compile` to generate a
locked `requirements.txt` for repeatable installs.

### Local Development Enhancements

- Django Debug Toolbar is included. It will automatically load and configure itself if
  DEBUG is on. URLs and middleware are added automatically.
- IPython is included. Django shell will use it automatically to provide an enhanced
  experience.
- Black and isort are included. The included VS Code configurations will keep your code
  tidy as you edit, or you can run the tools manually.
- Tox configurations are included for testing, code checks, and code coverage.
- pycodestyle is used to check code formatting.
- Runserver's console log output is enhanced using `rich.logging.RichHandler`.

### Continuous Integration and Testing

This template includes configurations for continuous integration and release automation
using Github Actions. It implements a testing matrix using
[tox](https://tox.wiki/en/latest/) allowing you to test against multiple versions of
Python and, if desired, Django (by default it only tests against Django 4.2 LTS). Out of
the box, the test automation checks for common errors, missing database migrations, and
invalid template syntax. It also enforces code style rules. Additional checks may be
added in the future.

The requirement for pytest has been removed, but configuration for pytest is retained in
the tox.ini file for those who prefer it as a test runner.

Support for enhanced test output has been added via
[django-rich](https://pypi.org/project/django-rich/).

### Editors

This template includes some extra configuration for users of Visual Studio Code, because
it's a lightweight and free code editor, and it's what I use. If you prefer PyCharm, you
can just ignore or delete the .vscode directory. Both are excellent tools for developing
Django apps. This is purely a matter of personal preference.

I will accept pull requests that add support for other editors, within reason.
