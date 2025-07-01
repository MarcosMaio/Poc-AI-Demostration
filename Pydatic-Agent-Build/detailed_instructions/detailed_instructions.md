## Instructions for Information Extraction

Instructions for Information Extraction

Use the guidelines below to extract and structure every field from the document into a single JSON object that exactly matches the schema. Do not include any extra text—only return the JSON.

### Fields and Descriptions:

1. **emissorId**:

   * UUID of the issuer.
   * Type: `string`

2. **codigoExterno**:

   * External reference code for the issuance.
   * Type: `string`

3. **numeroEmissao**:

   * Sequential issuance number.
   * Type: `integer`



### Schema of Expected Output:


```json
{
  "type": "object",
  "properties": {
      "emissorId": { "type": "string" },
      "codigoExterno": { "type": "string" },
      "numeroEmissao": { "type": "integer" },
      "numeroSerie": { "type": "string" },
  }
}
```