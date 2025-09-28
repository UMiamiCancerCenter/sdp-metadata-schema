# sdp-metadata-schema

Repository describing metadata schemas for Sylvester Data Portal

## JSON schema standard

https://json-schema.org/

## JSON schema validators

### JSON schema validator

https://www.jsonschemavalidator.net/

### ELIXIR Biovalidator

https://www.ebi.ac.uk/ait/biovalidator/

### 🔄 Updating JSON Schema Versions

To increment the version of the JSON schema files:

1. Open the `update_versions.py` file.
2. Set the values for:
   - `CURRENT_VERSION`: the version you want to replace.
   - `NEW_VERSION`: the new version you want to apply.
3. Run the script using one of the following commands, depending on your local setup:

```bash
python3 update_versions.py
# or
python update_versions.py
# or
poetry run update-json-versions
```
