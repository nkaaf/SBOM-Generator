from pathlib import Path
from typing import Final

from sbom_generator.models import (
    SourceType,
    TargetType,
)

__all__ = ['validate_target']


def validate_target(
    targets: list[TargetType], sources: list[SourceType], config_dir: Path
) -> None:
    ids = [target.id for target in targets]
    if len(ids) != len(set(ids)):
        msg: Final = f"Multiple equal ids in targets found: '{[target_id for target_id in ids if target_id not in set(ids)]}'"
        raise ValueError(msg)

    source_ids: Final = [source.id for source in sources]

    linked_sources: Final[list[str]] = []
    for target in targets:
        if target.source_id not in source_ids:
            msg = f"Source with ID '{target.source_id}' in target '{target.id}' is not found!"
            raise ValueError(msg)

        target_path: Final = config_dir / target.generation.output_path
        if target_path.parent.exists() and not target_path.parent.is_dir():
            msg: Final = f"Configured output directory '{target_path.parent!s}' exists, but is not a directory!"
            raise ValueError(msg)

        linked_sources.append(target.source_id)

    if len(sources) != len(set(linked_sources)):
        msg: Final = f"Following sources are configured, but are not linked by enabled nor disabled targets: '{[source.id for source in sources if source.id not in set(linked_sources)]}'"
        raise ValueError(msg)
