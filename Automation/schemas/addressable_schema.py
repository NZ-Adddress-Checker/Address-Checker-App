# The Addressable API returns a top-level array of address objects.
ADDRESSABLE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "formatted": {"type": "string"},
            "street_number": {"type": ["string", "null"]},
            "street": {"type": "string"},
            "city": {"type": "string"},
        },
        "required": ["formatted"],
    },
}