"""
Storages that store the manifest file in a unique subdirectory based on the release ID.
This prevents static file conflicts during deployments.
"""

import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
)
from django.utils.module_loading import import_string


def git_hash():
    """Get the current git commit hash."""
    try:
        git_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=settings.BASE_DIR)
            .decode("utf-8")
            .strip()
        )
    except Exception:
        git_hash = "unknown"
    return git_hash


def heroku_build_commit():
    """Get the Heroku build commit hash from the environment.
    Requires the Heroku Labs feature 'runtime-dyno-build-metadata' to be enabled.
    https://devcenter.heroku.com/articles/dyno-metadata
    """
    # For Heroku, we don't always have access to the git history. We can get
    # a unique release ID from the dyno metadata. At BUILD time, Heroku sets
    # the SOURCE_VERSION environment variable to the commit hash. At RELEASE
    # time, it sets the HEROKU_BUILD_COMMIT environment variable to the same
    # value. Works as of December 2025.
    SOURCE_VERSION = os.environ.get("SOURCE_VERSION", "")
    HEROKU_BUILD_COMMIT = os.environ.get("HEROKU_BUILD_COMMIT", "")
    RELEASE_ID = os.environ.get(
        "RELEASE_ID", SOURCE_VERSION or HEROKU_BUILD_COMMIT or "unknown"
    )
    return RELEASE_ID


# Custom static files storage that stores the manifest file in a unique subdirectory.
class ReleaseSpecificManifestLocalStorage(ManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        # Determine the release ID to use for the manifest file location.
        release_id = kwargs.pop("release_id", None)
        release_id_strategy_path = kwargs.pop("release_id_strategy", None)
        if not release_id and not release_id_strategy_path:
            # Raise an error if neither release_id nor release_id_strategy is provided.
            raise ValueError(
                "Either 'release_id' or 'release_id_strategy' must be provided."
            )
        if not release_id:
            release_id_strategy = import_string(release_id_strategy_path)
            release_id = release_id_strategy()
        # Set up the manifest storage to use a subdirectory named after the release ID.
        manifest_storage = StaticFilesStorage(
            location=Path(settings.STATIC_ROOT) / release_id
        )
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)


try:
    from storages.backends.s3 import S3ManifestStaticStorage, S3StaticStorage

    class ReleaseSpecificManifestS3Storage(S3ManifestStaticStorage):
        def __init__(self, *args, **kwargs):
            # Determine the release ID to use for the manifest file location.
            release_id = kwargs.pop("release_id", None)
            release_id_strategy_path = kwargs.pop("release_id_strategy", None)
            if not release_id and not release_id_strategy_path:
                # Raise an error if neither release_id nor release_id_strategy is provided.
                raise ValueError(
                    "Either 'release_id' or 'release_id_strategy' must be provided."
                )
            if not release_id:
                release_id_strategy = import_string(release_id_strategy_path)
                release_id = release_id_strategy()

            # Set up the manifest storage to use a subdirectory named after the release ID
            # otherwise using all the same S3 settings as the main storage.
            opts = kwargs.copy()  # copy to avoid modifying original
            opts["location"] = os.path.join(kwargs.get("location", ""), release_id)
            manifest_storage = S3StaticStorage(**opts)
            super().__init__(*args, manifest_storage=manifest_storage, **kwargs)

except ImportError:

    class ReleaseSpecificManifestS3Storage:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "django-storages is required for S3 storage. Please install it to use ReleaseSpecificManifestS3Storage."
            )
