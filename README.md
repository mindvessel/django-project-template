# Mindvessel Project Template for Django 4.2

Replace this README file with your own project's info.

## How to use it

To use this repository as a project template for Django, use the following command to
create your Django project, replacing URL and PROJECT_NAME:

    django-admin startproject --template URL -x .git PROJECT_NAME

OR simply create a new repository
[using this repository as a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template),
and rename the `project_name` directory to the name of your project.

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

If you find this template doesn't suit your needs, for a more comprehensive Django
template (with notably different opinions) take a look at the
[Django Cookiecutter](https://github.com/cookiecutter/cookiecutter-django).

### Common Dependencies

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

Dependencies are listed in a `requirements.in` file. See the section "Dependency
Management" for how to manage dependencies for your project.

### Local Development Enhancements

- Django Debug Toolbar is included. It will automatically load and configure itself if
  DEBUG is on. URLs and middleware are added automatically.
- IPython is included. Django shell will use it automatically to provide an enhanced
  experience.
- Black and isort are included. The included VS Code configurations will keep your code
  tidy as you edit, or you can run the tools manually.
- Tox configurations are included for testing, code checks, and code coverage.
- Runserver's console log output is enhanced using `rich.logging.RichHandler`.
- `manage.py` contains a `devsetup` command to bootstrap your dev environment, and
  additional commands to help manage dependencies (see the section "Dependency
  Management" for details).

### Continuous Integration and Testing

This template includes configurations for continuous integration and release automation
using Github Actions. It implements a testing matrix using
[tox](https://tox.wiki/en/latest/) allowing you to test against multiple versions of
Python and, if desired, Django (by default it only tests against Django 4.2 LTS). Out of
the box, the test automation checks for common errors, missing database migrations, and
invalid template syntax. Additional checks may be added in the future.

Support for enhanced test output has been added via
[django-rich](https://pypi.org/project/django-rich/).

### Editors

This template includes some extra configuration for users of Visual Studio Code, because
it's a lightweight and free code editor, and it's what I use. If you prefer PyCharm, you
can just ignore or delete the .vscode directory. Both are excellent tools for developing
Django apps. This is purely a matter of personal preference.

I will accept pull requests that add support for other editors, within reason.

### Copyright License

Source code in this template is derived from Django's project template. Django does not
include license information in generated projects, but Django itself is licensed under a
[BSD 3-Clause License](https://github.com/django/django/blob/main/LICENSE).

Source code modifications provided as part of this template are licensed under the same
terms as would be applied to the standard output of Django's `startproject` command.

### Final Word

I hope you find this template useful!

You may wish to retain the Dependency Management section below as part of your project's
documentation.

## Dependency Management

This project includes [pip-tools](https://pypi.org/project/pip-tools/) for dependency
management. There are two requirements files: `requirements.in` provides the acceptable
ranges of packages to install in a production environment (or any other environment);
`requirements-dev.in` provides packages to install in development environments. Both of
these have corresponding "pin" files: `requirements.txt` and `requirements-dev.txt`.

To add a new dependency, add it to the correct `.in` file, and then run
`manage.py pipsync` to regenerate the pin files and synchronize your current virtual
environment with the new pin files.

Any arguments passed to `manage.py pipsync` will be passed through to the underlying
`pip-compile` command. For example, to bump to the latest Django patch release use
`manage.py pipsync --upgrade-package django`. See the
[pip-tools docs](https://pypi.org/project/pip-tools/) for complete details.

The pin files are not included in the template repository, but will be generated when
you run `manage.py devsetup`. This ensures you will get the latest version of Django and
related packages when starting a new project.
