import msgspec
from fastapi import FastAPI, Request, Response

from msgspec_openapi_utils import get_json_schema, setup_custom_openapi


class Person(msgspec.Struct):
    name: str
    age: int


class HanderRequest(msgspec.Struct):
    persons: list[Person]


class HanderResponse(msgspec.Struct):
    count: int


decoder = msgspec.json.Decoder(HanderRequest)
encoder = msgspec.json.Encoder()

app = FastAPI()
setup_custom_openapi(app, title="Msgspec Inside.", version="1.0.0")


@app.post(
    "/handler",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": get_json_schema(HanderRequest),
                },
            },
        },
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "schema": get_json_schema(HanderResponse),
                    },
                },
            },
        },
    },
)
async def handler(
    request: Request,
) -> Response:
    parsed_request = decoder.decode(await request.body())
    response = HanderResponse(count=len(parsed_request.persons))
    return Response(
        content=encoder.encode(response),
        media_type="application/json",
    )

