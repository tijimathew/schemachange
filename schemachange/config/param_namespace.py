"""
Maintain a centralized location for configuration parameters used across the application.
Separate parameters into different categories for better organization.
"""
from os import environ
from dataclasses import dataclass, field
from typing import Any, Dict, Set, Literal
from packaging import version
import logging

# Minimum supported connector version
SNOWFLAKE_CONNECTOR_MIN_VERSION = "2.8.0"

@dataclass(frozen=True)
class ParamNamespace:
    """
    Represents a namespace for a group of configuration parameters.
    Stores the set of valid parameter names, their default values, and minimum supported versions.
    """
    prefix: Literal["SNOWFLAKE", "SCHEMACHANGE"] = "SNOWFLAKE"
    params: Set[str]
    defaults: Dict[str, Any] = field(default_factory=dict)
    min_versions: Dict[str, str] = field(default_factory=dict)
    max_versions: Dict[str, str] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=lambda: {k: f"{ParamNamespace.prefix}_{k.upper()}" for k in ParamNamespace.params})

    def is_supported_param(self, param: str, connector_version: str) -> bool:
        """
        Check if a parameter is supported for the given connector version.

        Args:
            param (str): The parameter name.
            connector_version (str): The connector version string.

        Returns:
            bool: True if supported, False otherwise.
        """
        min_version = self.min_versions.get(param)
        max_version = self.max_versions.get(param)
        
        if min_version is None:
            min_version = SNOWFLAKE_CONNECTOR_MIN_VERSION
        
        if min_version is not None and max_version is None:
            return version.parse(connector_version) >= version.parse(min_version)
        else:
            return version.parse(connector_version) >= version.parse(min_version) and version.parse(connector_version) < version.parse(max_version)

    def is_supported_environment_variable(self, env_var: str) -> bool:
        """
        Check if an environment variable is supported.

        Args:
            env_var (str): The environment variable name.

        Returns:
            bool: True if supported, False otherwise.
        """
        return env_var in self.environment_variables.keys()

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
    prefix="SNOWFLAKE",
    params={
        "account",
        "user",
        "password",
        "application",
        "region",
        "port",
        "database",
        "schema",
        "role",
        "warehouse",
        "passcode_in_password",
        "passcode",
        "private_key",
        "private_key_file",
        "private_key_file_pwd",
        "autocommit",
        "client_fetch_use_mp",
        "client_prefetch_threads",
        "client_session_keep_alive",
        "connection_name",
        "connections_file_path",
        "login_timeout",
        "network_timeout",
        "ocsp_response_cache_filename",
        "authenticator",
        "validate_default_parameters",
        "paramstyle",
        "timezone",
        "arrow_number_to_decimal",
        "socket_timeout",
        "backoff_policy",
        "enable_connection_diag",
        "connection_diag_log_path",
        "connection_diag_allowlist_path",
        "iobound_tpe_limit",
        "unsafe_file_write",
        "disable_ocsp_checks",
        "insecure_mode",
        "debug_arrow_chunk",
        "disable_saml_url_check",
        "oauth_client_id",
        "oauth_client_secret",
        "oauth_authorization_url",
        "oauth_token_request_url",
        "oauth_scope",
        "oauth_redirect_uri",
        "oauth_disable_pkce",
        "oauth_enable_refresh_token",
        "oauth_enable_single_use_refresh_tokens",
        "client_store_temporary_credential",
        "client_fetch_use_mp",
        "session_parameters"
    },
    # minimum version after which the parameter is supported
    # minimum version number is expected to be greater than supported minimum connector version.
    min_versions={
        "connection_name": "3.1.0",
        "connections_file_path": "3.1.0",
        "client_session_keep_alive": "3.1.0",
        "backoff_policy": "3.4.0",
        "private_key_file": "3.6.0",
        "private_key_file_pwd": "3.6.0",
        "token_file_path": "3.11.0",
        "debug_arrow_chunk": "3.11.0",
        "disable_saml_url_check": "3.11.0",
        "iobound_tpe_limit": "3.13.0",
        "unsafe_file_write": "3.14.0",
        "disable_ocsp_checks": "3.14.1",
        "oauth_client_id": "3.15.0",
        "oauth_client_secret": "3.15.0",
        "oauth_authorization_url": "3.15.0",
        "oauth_token_request_url": "3.15.0",
        "oauth_redirect_uri": "3.15.0",
        "oauth_scope": "3.15.0",
        "oauth_disable_pkce": "3.15.0",
        "oauth_enable_refresh_tokens": "3.15.0",
        "oauth_enable_single_use_refresh_tokens": "3.15.0",
        "client_store_temporary_credential": "3.15.0",
        "client_fetch_use_mp": "3.16.0"
        # ...add more as needed
    },
    # max version after which the parameter is deprecated
    max_versions={
        "insecure_mode": "3.14.1"
    }
)

# Instantiate for schemachange-specific params
SCHEMACHANGE_PARAMS = ParamNamespace(
    prefix="SCHEMACHANGE",
    params={
        "root_folder",
        "config_folder",
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
        "config_folder": ".",
        "config_file": "schemachange-config.yml",
        "create_change_history_table": False,
        "change_history_table": "METADATA.SCHEMACHANGE.CHANGE_HISTORY",
        "vars": {},
        "dry_run": False,
        "verbose": False,
        "log_level": logging.INFO,
        "modules_folder": None,
    }
)

