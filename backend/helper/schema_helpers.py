from typing import Any, Dict, Type
from google.genai.types import Schema
from pydantic import BaseModel
from datetime import datetime


def dict_to_schema(d: Dict[str, Any]) -> Schema:
    """
    Convert a flattened dict schema into a google.genai.types.Schema recursively.
    """
    if type(d) is not dict:
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


def flatten_schema(model: Type[BaseModel]) -> Dict[str, Any]:
    """
    Flatten a Pydantic model schema by resolving all $ref entries
    into their actual definitions from $defs.
    Ensures no $ref remains so that google.genai.types.Schema accepts it.
    """
    if not hasattr(model, "model_json_schema") or not callable(getattr(model, "model_json_schema")):
        raise TypeError(f"Expected Pydantic model class, got {type(model)}")

    schema = model.model_json_schema()
    defs = schema.pop("$defs", {})

    def resolve_refs(obj: Any) -> Any:
    # Dict-like: check for .items() and .get() methods
        try:
            if hasattr(obj, "items") and callable(getattr(obj, "items")) and hasattr(obj, "get") and callable(getattr(obj, "get")):
                if "$ref" in obj:
                    ref_path = obj["$ref"]
                    if ref_path.startswith("#/$defs/"):
                        def_name = ref_path.split("/")[-1]
                        resolved = defs.get(def_name, {})
                        return resolve_refs(resolved)
                    return {}
                return {k: resolve_refs(v) for k, v in obj.items()}
        except Exception:
            pass

        # List-like: check for __iter__ and __getitem__ (iterable, not a string)
        try:
            iter(obj)  # check if iterable
            obj["__dummy__"]  # will fail for string
        except Exception:
            # Not list-like
            return obj

        # If it passed both, treat as list
        result = []
        try:
            for v in obj:
                result.append(resolve_refs(v))
            return result
        except Exception:
            return obj  # fallback

    return resolve_refs(schema)
