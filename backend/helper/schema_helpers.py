from typing import Any, Dict
from google.genai.types import Schema
from pydantic import BaseModel


def dict_to_schema(d: Dict[str, Any]) -> Schema:
    """
    Convert a flattened dict schema into a google.genai.types.Schema recursively.
    """
    if not isinstance(d, dict):
        raise TypeError(f"dict_to_schema expected dict, got {type(d)}")

    schema_type = d.get("type", "object")

    # Arrays
    if schema_type == "array":
        return Schema(
            type="array",
            items=dict_to_schema(d.get("items", {})),
            description=d.get("description"),
            nullable=d.get("nullable", False),
        )

    # Objects
    if schema_type == "object":
        props = d.get("properties", {})
        return Schema(
            type="object",
            properties={k: dict_to_schema(v) for k, v in props.items()},
            required=d.get("required", []),
            description=d.get("description"),
            additionalProperties=(
                dict_to_schema(d["additionalProperties"])
                if "additionalProperties" in d else None
            ),
            nullable=d.get("nullable", False),
        )

    # Primitive types
    return Schema(
        type=schema_type,
        format=d.get("format"),
        description=d.get("description"),
        nullable=d.get("nullable", False),
    )


def flatten_schema(model: type[BaseModel]) -> Dict[str, Any]:
    """
    Flatten a Pydantic model schema by resolving all $ref entries
    into their actual definitions from $defs.
    Ensures no $ref remains so that google.genai.types.Schema accepts it.
    """
    schema = model.model_json_schema()
    defs = schema.pop("$defs", {})

    def resolve_refs(obj: Any) -> Any:
        if isinstance(obj, dict):
            # Resolve references
            if "$ref" in obj:
                ref_path = obj["$ref"]
                if ref_path.startswith("#/$defs/"):
                    def_name = ref_path.split("/")[-1]
                    resolved = defs.get(def_name, {})
                    return resolve_refs(resolved)  # recurse into resolved schema
                return {}  # drop unknown refs

            # Recurse into dict keys
            return {k: resolve_refs(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            # Recurse into list items
            return [resolve_refs(elem) for elem in obj]

        return obj

    return resolve_refs(schema)
