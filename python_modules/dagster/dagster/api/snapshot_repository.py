from dagster import check
from dagster.core.host_representation import (
    ExternalRepository,
    ExternalRepositoryData,
    PythonEnvRepositoryLocationHandle,
    RepositoryHandle,
)
from dagster.core.origin import RepositoryPythonOrigin
from dagster.grpc.client import ephemeral_grpc_api_client

from .utils import execute_unary_api_cli_command


def sync_get_external_repositories(repository_location_handle):
    check.inst_param(
        repository_location_handle, 'repository_location_handle', PythonEnvRepositoryLocationHandle,
    )

    repos = []

    for key, pointer in repository_location_handle.repository_code_pointer_dict.items():

        external_repository_data = check.inst(
            execute_unary_api_cli_command(
                repository_location_handle.executable_path,
                'repository',
                RepositoryPythonOrigin(repository_location_handle.executable_path, pointer),
            ),
            ExternalRepositoryData,
        )
        repos.append(
            ExternalRepository(
                external_repository_data,
                RepositoryHandle(
                    repository_name=external_repository_data.name,
                    repository_key=key,
                    repository_location_handle=repository_location_handle,
                ),
            )
        )

    return repos


def sync_get_external_repositories_grpc(repository_location_handle):
    check.inst_param(
        repository_location_handle, 'repository_location_handle', PythonEnvRepositoryLocationHandle,
    )

    repos = []

    with ephemeral_grpc_api_client(
        python_executable_path=repository_location_handle.executable_path
    ) as api_client:
        for key, pointer in repository_location_handle.repository_code_pointer_dict.items():
            external_repository_data = check.inst(
                api_client.external_repository(
                    repository_python_origin=RepositoryPythonOrigin(
                        repository_location_handle.executable_path, pointer
                    )
                ),
                ExternalRepositoryData,
            )
            repos.append(
                ExternalRepository(
                    external_repository_data,
                    RepositoryHandle(
                        repository_name=external_repository_data.name,
                        repository_key=key,
                        repository_location_handle=repository_location_handle,
                    ),
                )
            )

    return repos
