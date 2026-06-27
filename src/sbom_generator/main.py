import json
import logging
from importlib.resources import files
from pathlib import Path
from typing import Annotated, Any, Final

import jsonschema
import yaml
from typer import Argument, Typer

from .execution import execute_targets
from .models import Configuration
from .validation import validate_source, validate_target

__all__ = []

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()],
)
logger: Final = logging.getLogger(__name__)

app: Final = Typer(name='sbom', no_args_is_help=True)


@app.command(name='validate')
def validate(
    config_path: Annotated[
        Path, Argument(help='The path of the generation configuration.')
    ],
) -> Configuration:
    config_path: Final = config_path.resolve()

    configuration: Final[dict[str, Any]] = yaml.safe_load(
        config_path.read_text(encoding='utf-8')
    )
    if 'version' not in configuration:
        raise jsonschema.ValidationError(message="Field 'version' is missing.")

    schema_file: Final = (
        files('sbom_generator')
        / 'schemas'
        / f'generation-{configuration["version"]}.schema.json'
    )

    if not Path(str(schema_file)).exists():
        raise jsonschema.ValidationError(message="Field 'version' is not valid.")

    jsonschema.validate(
        configuration,
        json.load(schema_file.open('r', encoding='utf-8')),
    )

    sbom_configuration = Configuration.model_validate(configuration)

    validate_source(sbom_configuration.sources, config_path.parent)
    validate_target(
        sbom_configuration.targets, sbom_configuration.sources, config_path.parent
    )

    logger.info('Configuration is valid!')

    return sbom_configuration


@app.command(name='generate')
def generate(
    config_path: Annotated[
        Path, Argument(help='The path of the generation configuration.')
    ],
) -> None:
    config_path: Final = config_path.resolve()

    configuration: Final = validate(config_path)

    enabled_targets = [target for target in configuration.targets if target.enabled]
    execute_targets(enabled_targets, configuration.sources, config_path.parent)


if __name__ == '__main__':
    app()
