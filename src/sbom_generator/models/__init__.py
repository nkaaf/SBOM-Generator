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
)

SourceType: TypeAlias = SourceGit | SourceLocal | SourceDocker
TargetType: TypeAlias = TargetDocker | TargetNPM

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
]
