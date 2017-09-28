import os
import pytest
import shutil
import logging

from populus.config import (
    Config,
)
from populus.config.defaults import (
    load_default_config,
    load_user_default_config,
    get_default_config_path,
)

from populus.config.helpers import (
    get_legacy_json_config_file_path,
)

from populus.project import (
    Project,
)

from populus.config.versions import (
    V1,
    V2,
    V3,
    V4,
    V5,
    V6,
    V7,
    FIRST_USER_CONFIG_VERSION
)

from populus.api.upgrade import (
    upgrade_configs,
)

from populus.utils.testing import (
    user_config_version,
)


@pytest.mark.parametrize(
    'from_legacy_version',
    (V1, V2, V3, V4, V5, V6)
)
@user_config_version(FIRST_USER_CONFIG_VERSION)
def test_upgrade_to_user_config(project, from_legacy_version):

    shutil.copyfile(
        get_default_config_path(version=from_legacy_version),
        get_legacy_json_config_file_path(project_dir=project.project_dir)
    )

    os.remove(project.config_file_path)

    logger = logging.getLogger("test.test_upgrade_to_user_config")
    upgrade_configs(project.project_dir, logger, FIRST_USER_CONFIG_VERSION)

    upgraded_project = Project(
        project_dir=project.project_dir,
        user_config_file_path=project.user_config_file_path
    )

    expected_user_config = Config(load_user_default_config(V7))
    expected_user_config.unref()

    expected_project_config = Config(load_default_config(V7))
    expected_project_config.unref()

    assert upgraded_project.legacy_config_path is None
    assert upgraded_project.config == expected_user_config
    assert upgraded_project.user_config == expected_user_config
    assert upgraded_project.project_config == expected_project_config
