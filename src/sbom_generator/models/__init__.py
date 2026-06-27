from typing import TypeAlias

from .configuration import (
    SBOMGenerationConfig as Configuration, TargetEsbuild,
)
from .configuration import (
    SourceBase,
    SourceGit,
    SourceLocal,
    TargetNPM,
    TargetRuby,
    TargetYarn,
)

SourceType: TypeAlias = SourceGit | SourceLocal
TargetType: TypeAlias = TargetNPM | TargetYarn | TargetRuby | TargetEsbuild

__all__ = [
    'Configuration',
    'SourceBase',
    'SourceGit',
    'SourceLocal',
    'SourceType',
    'TargetEsbuild',
    'TargetNPM',
    'TargetRuby',
    'TargetType',
    'TargetYarn',
]
