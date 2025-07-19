from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Literal

from schemachange.config.param_namespace import SNOWFLAKE_PARAMS, SCHEMACHANGE_PARAMS
from schemachange.config.BaseConfig import BaseConfig
from schemachange.config.utils import validate_file_path


@dataclasses.dataclass(frozen=True)
class RenderConfig(BaseConfig):
    script_path: Path | None = None
    subcommand: Literal["render"] = "render"

    @classmethod
    def factory(
        cls,
        script_path: Path | str,
        **kwargs,
    ):
        # 1. Gather all possible defaults
        merged_kwargs = {}
        merged_kwargs.update(SCHEMACHANGE_PARAMS.get_defaults())
        merged_kwargs.update(SNOWFLAKE_PARAMS.get_defaults())
        
        # 2. Overlay with provided kwargs limited to RenderConfig fields
        field_names = [field.name for field in dataclasses.fields(RenderConfig)]
        merged_kwargs.update({k: v for k, v in kwargs.items() if k in field_names})

        # 3. Handle script_path precedence and validation
        if script_path is not None:
            merged_kwargs["script_path"] = validate_file_path(file_path=script_path)
        elif merged_kwargs.get("script_path") is not None:
            merged_kwargs["script_path"] = validate_file_path(file_path=merged_kwargs["script_path"])
        else:
            raise TypeError("RenderConfig is missing 1 required argument: 'script_path'")
        
        # 4. Always set subcommand
        merged_kwargs["subcommand"] = "render"

        # 5. Remove any keys not in RenderConfig fields (defensive)
        merged_kwargs = {k: v for k, v in merged_kwargs.items() if k in field_names}

        # 6. Call parent factory
        return super().factory(**merged_kwargs)

    def __post_init__(self):
        if self.script_path is None:
            raise TypeError(
                "RenderConfig is missing 1 required argument: 'script_path'"
            )
