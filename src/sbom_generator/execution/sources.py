import shutil
from pathlib import Path
from typing import Final

from git import Repo

from sbom_generator.models import SourceGit, SourceType

__all__ = ['execute_sources']


def execute_sources(sources: list[SourceType], config_dir: Path) -> None:
    for source in sources:
        if isinstance(source, SourceGit):
            path: Final = (
                config_dir / source.clone_dir
            )  # ).resolve() # Resolve, because Repo.clone_from cannot handle relative paths
            if path.is_dir():
                shutil.rmtree(path)

            Repo.clone_from(source.url, to_path=path)
