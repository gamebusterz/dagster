from dagster.cli.workspace.load import load_workspace_from_yaml_paths
from dagster.utils import file_relative_path


def test_workspace():
    workspace = load_workspace_from_yaml_paths([file_relative_path(__file__, '../workspace.yaml')])
    assert len(workspace.repository_location_handles) == 2
