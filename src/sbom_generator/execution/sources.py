import shutil
from pathlib import Path
from typing import Final

from git import Repo

from sbom_generator.models import SourceGit, SourceType

__all__ = ['execute_source']

EXECUTED_SOURCES: Final[dict[str, SourceType]] = {}


def execute_source(source: SourceType, config_dir: Path) -> None:
    if source.id in EXECUTED_SOURCES:
        return

    if isinstance(source, SourceGit):
        path: Final = (
            config_dir / source.clone_dir
        )  # ).resolve() # Resolve, because Repo.clone_from cannot handle relative paths
        if path.is_dir():
            shutil.rmtree(path)

        Repo.clone_from(source.url, to_path=path)

    EXECUTED_SOURCES[source.id] = source
