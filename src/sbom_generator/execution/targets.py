import shutil
import subprocess
from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final

from sbom_generator.models import (
    SourceGit,
    SourceLocal,
    SourceType,
    TargetNPM,
    TargetType,
)

__all__ = ['execute_targets']


def _execute_target_npm(
    target: TargetNPM, source: SourceType, config_dir: Path
) -> None:
    assert isinstance(source, (SourceGit, SourceLocal))

    if isinstance(source, SourceGit):
        source_path: Final = config_dir / source.clone_dir
    else:
        source_path: Final = config_dir / source.path
    manifest_path = source_path / target.options.path

    if not manifest_path.is_file():
        msg: Final = f"Configured manifest '{manifest_path!s}' in target '{target.id}' with source '{source.id}' is not an existing file!"
        raise ValueError(msg)

    if target.options.lock_only and not (
        (manifest_path.parent / 'npm-shrinkwrap.json').is_file()
        or (manifest_path.parent / 'package-lock.json').is_file()
    ):
        msg: Final = f"Lock Only mode is configured, but neither a 'npm-shrinkwrap.json' nor a 'package-lock.json' for target '{target.id}' in source '{source.id}' file exists!"
        raise ValueError(msg)

    if not target.options.lock_only:
        node_modules_dir: Final = manifest_path.parent / 'node_modules'
        if node_modules_dir.is_dir():
            shutil.rmtree(node_modules_dir)

        subprocess.check_call(
            [
                'npm',
                'install',
                '.',
                *(['--omit=dev'] if not target.options.include_dev else []),
                *(['--omit=peer'] if not target.options.include_peer else []),
                *(['--omit=optional'] if not target.options.include_optional else []),
            ],
            cwd=manifest_path.parent,
            stdout=subprocess.DEVNULL,
        )

    with TemporaryDirectory() as tmpdir:
        shutil.copy(
            (Path(str(files('sbom_generator') / 'deps' / 'npm' / 'package.json'))),
            tmpdir,
        )

        subprocess.check_call(
            ['npm', 'install'],
            cwd=tmpdir,
            stdout=subprocess.DEVNULL,
        )

        subprocess.check_call(
            [
                'npx',
                '--',
                '@cyclonedx/cyclonedx-npm',
                *(['--package-lock-only'] if target.options.lock_only else []),
                *(['--omit', 'dev'] if not target.options.include_dev else []),
                *(['--omit', 'peer'] if not target.options.include_peer else []),
                *(
                    ['--omit', 'optional']
                    if not target.options.include_optional
                    else []
                ),
                *(['--flatten-components'] if target.options.flatten else []),
                *(['--spec-version', target.generation.spec_version]),
                '--output-reproducible',
                *(['--output-format', target.generation.format]),
                *(
                    [
                        '--output-file',
                        (config_dir / target.generation.output_path)
                        .absolute()
                        .resolve(),
                    ]
                ),  # Resolve, for understandable output logging
                '--validate',
                *(['--mc-type', target.options.main_type.value]),
                '--verbose',
                '--',
                manifest_path,
            ],
            cwd=tmpdir,
            stdout=subprocess.DEVNULL,
        )


def execute_targets(
    targets: list[TargetType], sources: list[SourceType], config_path: Path
) -> None:
    for target in targets:
        source: Final = next(
            source for source in sources if source.id == target.source_id
        )
        if isinstance(target, TargetNPM):
            _execute_target_npm(target, source, config_path)
