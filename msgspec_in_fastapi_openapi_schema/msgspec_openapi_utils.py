from functools import partial
from typing import Any

import msgspec
from fastapi import FastAPI
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import get_openapi

REF_TEMPLATE = f"{REF_PREFIX}{{name}}"


def get_json_schema(model: Any) -> dict[str, Any]:
    (out,), components = msgspec.json.schema_components(
        (model,),
        ref_template=REF_TEMPLATE,
    )
    if components:
        out["$defs"] = components
    return out


def custom_openapi(app: FastAPI, **kwargs) -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        **kwargs,
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    components = openapi_schema["components"]
    if "schemas" not in components:
        components["schemas"] = {}

    def move_content_defs_to_schemas(content: dict[str, Any]) -> None:
        for content_type_description in content.values():
            if "schema" not in content_type_description:
                continue
            defs = content_type_description["schema"].pop("$defs", {})
            components["schemas"].update(defs)

    app.openapi_schema = openapi_schema

    for path in openapi_schema["paths"].values():
        for method_data in path.values():
            responses = method_data.get("responses", {})
            for response in responses.values():
                move_content_defs_to_schemas(response.get("content", {}))

            requests_body = method_data.get("requestBody", {})
            move_content_defs_to_schemas(requests_body.get("content", {}))

    return app.openapi_schema


def setup_custom_openapi(app: FastAPI, **kwargs) -> None:
    openapi = partial(custom_openapi, app, **kwargs)
    app.openapi = openapi
