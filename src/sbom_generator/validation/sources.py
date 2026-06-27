from pathlib import Path
from typing import Final

from sbom_generator.models import SourceGit, SourceLocal, SourceType

__all__ = ['validate_source']


def validate_source(sources: list[SourceType], config_dir: Path) -> None:
    ids: Final = [source.id for source in sources]
    if len(ids) != len(set(ids)):
        msg: Final = f"Multiple equal ids in sources found: '{[source_id for source_id in ids if source_id not in set(ids)]}'."
        raise ValueError(msg)

    paths: Final[list[Path]] = []

    for source in sources:
        if isinstance(source, SourceLocal):
            path: Final = config_dir / source.path
        elif isinstance(source, SourceGit):
            path: Final = config_dir / source.clone_dir
        else:
            path: Final = None

        if path is not None:
            if path.exists() and not path.is_dir():
                msg: Final = f"Path '{path.absolute()!s}' is not a valid directory."
                raise ValueError(msg)
            paths.append(path.resolve())

    if len(paths) != len(set(paths)):
        msg: Final = f"Multiple equal source paths found: '{[path for path in paths if path not in set(paths)]}'"
        raise ValueError(msg)
