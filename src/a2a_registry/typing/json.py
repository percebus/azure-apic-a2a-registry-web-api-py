"""Types."""

SerializedJson = str
JsonValue = None, int, float, list["JsonValue"], dict[str, "JsonValue"]
JsonObject = dict[str, "JsonValue"]
