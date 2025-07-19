"""
Maintain a centralized location for configuration parameters used across the application.
Separate parameters into different categories for better organization.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Set
from packaging import version
import logging

@dataclass(frozen=True)
class ParamNamespace:
    """
    Represents a namespace for a group of configuration parameters.
    Stores the set of valid parameter names, their default values, and minimum supported versions.
    """
    params: Set[str]
    defaults: Dict[str, Any] = field(default_factory=dict)
    min_versions: Dict[str, str] = field(default_factory=dict)

    def is_supported(self, param: str, connector_version: str) -> bool:
        """
        Check if a parameter is supported for the given connector version.

        Args:
            param (str): The parameter name.
            connector_version (str): The connector version string.

        Returns:
            bool: True if supported, False otherwise.
        """
        min_version = self.min_versions.get(param)
        if min_version is None:
            return True
        return version.parse(connector_version) >= version.parse(min_version)

    def get_defaults(self) -> Dict[str, Any]:
        """
        Get a copy of the default values for this namespace.

        Returns:
            Dict[str, Any]: A copy of the defaults dictionary.
        """
        return self.defaults.copy()

    def filter(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return only parameters in this namespace from a given config dictionary.

        Args:
            config_dict (Dict[str, Any]): The configuration dictionary.

        Returns:
            Dict[str, Any]: Filtered dictionary containing only valid parameters.
        """
        return {k: v for k, v in config_dict.items() if k in self.params}

# Instantiate for Snowflake
SNOWFLAKE_PARAMS = ParamNamespace(
    params={
        "account",
        "user",
        "password",
        "private_key",
        "private_key_file",
        "private_key_file_pwd",
        "authenticator",
        "database",
        "schema",
        "warehouse",
        "role",
        "session_parameters",
        "application",
        "token",
        "token_file_path",
        "client_session_keep_alive",
        "client_prefetch_threads",
        "insecure_mode",
        "ocsp_response_cache_filename",
        "login_timeout",
        "network_timeout",
        "validate_default_parameters",
        "connection_name",
        "connections_file_path"
    },
    defaults={
        "warehouse": "COMPUTE_WH",
        "role": "SYSADMIN",
        # ...add more as needed
    },
    min_versions={
        "token_file_path": "3.0.0",
        "connection_name": "3.0.0",
        "connections_file_path": "3.0.0",
        # ...add more as needed
    }
)

# Instantiate for schemachange-specific params
SCHEMACHANGE_PARAMS = ParamNamespace(
    params={
        "root_folder",
        "config_file",
        "create_change_history_table",
        "change_history_table",
        "vars",
        "dry_run",
        "verbose",
        "log_level",
        "modules_folder",
        # ...add more as needed
    },
    defaults={
        "root_folder": ".",
        "create_change_history_table": False,
        "change_history_table": "METADATA.SCHEMACHANGE.CHANGE_HISTORY",
        "vars": {},
        "dry_run": False,
        "verbose": False,
        "log_level": logging.INFO,
        "modules_folder": None,
    }
)

# Minimum supported connector version
SNOWFLAKE_CONNECTOR_MIN_VERSION = "2.8.0"