from typing import TypeAlias

from .configuration import (
    SBOMGenerationConfig as Configuration,
)
from .configuration import (
    SourceBase,
    SourceDocker,
    SourceGit,
    SourceLocal,
    TargetDocker,
    TargetNPM,
    TargetYarn,
)

SourceType: TypeAlias = SourceGit | SourceLocal | SourceDocker
TargetType: TypeAlias = TargetDocker | TargetNPM | TargetYarn

__all__ = [
    'Configuration',
    'SourceBase',
    'SourceDocker',
    'SourceGit',
    'SourceLocal',
    'SourceType',
    'TargetDocker',
    'TargetNPM',
    'TargetType',
    'TargetYarn',
]
