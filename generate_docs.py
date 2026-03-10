import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.get("/openapi.json")
openapi_schema = response.json()

md_content = f"# {openapi_schema['info']['title']} API Documentation\n\n"
md_content += f"**Version**: {openapi_schema['info']['version']}\n"
md_content += f"**Description**: {openapi_schema['info'].get('description', '')}\n\n"

for path, path_data in openapi_schema['paths'].items():
    for method, endpoint in path_data.items():
        md_content += f"## `{method.upper()} {path}`\n\n"
        md_content += f"**Summary**: {endpoint.get('summary', '')}\n\n"
        
        if 'description' in endpoint:
            md_content += f"{endpoint['description']}\n\n"
            
        if 'parameters' in endpoint:
            md_content += "### Parameters\n"
            md_content += "| Name | In | Required | Type |\n"
            md_content += "|---|---|---|---|\n"
            for param in endpoint['parameters']:
                required = "Yes" if param.get('required') else "No"
                param_type = param.get('schema', {}).get('type', 'any') # Simplified
                md_content += f"| {param['name']} | {param['in']} | {required} | {param_type} |\n"
            md_content += "\n"
            
        if 'requestBody' in endpoint:
            md_content += "### Request Body\n"
            content = endpoint['requestBody'].get('content', {})
            if 'application/json' in content:
                schema_ref = content['application/json'].get('schema', {}).get('$ref', '')
                if schema_ref:
                    schema_name = schema_ref.split('/')[-1]
                    md_content += f"Expects a JSON body corresponding to the `{schema_name}` schema.\n\n"
                else:
                    md_content += "Expects a JSON body.\n\n"
                    
        if 'responses' in endpoint:
            md_content += "### Responses\n"
            md_content += "| Status Code | Description |\n"
            md_content += "|---|---|\n"
            for status, resp_data in endpoint['responses'].items():
                md_content += f"| {status} | {resp_data.get('description', '')} |\n"
            md_content += "\n"
            
        md_content += "---\n\n"

# Add Schemas section
md_content += "## Data Schemas\n\n"
if 'components' in openapi_schema and 'schemas' in openapi_schema['components']:
    for schema_name, schema_data in openapi_schema['components']['schemas'].items():
        md_content += f"### {schema_name}\n"
        md_content += "| Property | Type | Required | Default |\n"
        md_content += "|---|---|---|---|\n"
        
        properties = schema_data.get('properties', {})
        required_fields = schema_data.get('required', [])
        
        for prop_name, prop_data in properties.items():
            req_str = "Yes" if prop_name in required_fields else "No"
            prop_type = prop_data.get('type', 'any')
            if 'anyOf' in prop_data:
                types = [t.get('type', 'null') for t in prop_data['anyOf']]
                prop_type = " or ".join(types)
            if 'default' in prop_data:
                default_val = prop_data['default']
            else:
                default_val = "None"
            md_content += f"| {prop_name} | {prop_type} | {req_str} | {default_val} |\n"
        md_content += "\n"

with open("API_Documentation.md", "w") as f:
    f.write(md_content)
    
print("Successfully generated API_Documentation.md")
