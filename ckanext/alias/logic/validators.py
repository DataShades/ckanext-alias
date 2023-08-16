from __future__ import annotations

import json
from typing import Any

import ckan.plugins.toolkit as tk
from ckan.logic.converters import convert_to_json_if_string
from ckan.types import Context, FlattenDataDict, FlattenErrorDict, FlattenKey

import ckanext.alias.utils as alias_utils


def alias_unique(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    """Ensures that the alias unique and not occupied by another dataset"""
    aliases: list[str] = convert_to_json_if_string(data[key], context)
    pkg_id = data[("id",)]

    if not aliases:
        return

    if len(aliases) != len(set(aliases)):
        raise tk.Invalid("Alias must be unique. Remove duplicates.")

    for alias in aliases:
        pkg_dict = alias_utils.get_package_by_alias(alias)

        if not pkg_dict:
            continue

        if pkg_dict["id"] == pkg_id:
            continue

        raise tk.Invalid(f"Alias '{alias}' is already occupied.")

    data[key] = json.dumps(aliases)


def name_doesnt_conflict_with_alias(v: str, context) -> Any:
    """Ensures that the name doesn't conflict with existing aliases"""

    if alias_utils.get_package_by_alias(v):
        raise tk.Invalid(f"Name '{v}' is already occupied by an alias.")

    return v
