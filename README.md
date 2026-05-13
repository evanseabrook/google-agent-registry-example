# Agent Agent Registry Example

This project is meant to demonstrate how Gemini Enterprise Agent Platform can offload MCP tool discovery to Agent Registry and external tool authentication to Agent Identity.

## Prerequisites

Before getting started, ensure you have the following set up:
- An auth provider ready to go with a client credential app registration. Auth0 was used for this lab and is referenced heavily in the code.
- Sufficient permissions to interact with all of the services in this lab, including:
  - Gemini Enterprise Agent Platform
  - Cloud Run
  - IAM Connectors
- Application default credentials set up for gcloud with a quota project set. You can do this by running the following two commands in series:
  
  ```bash
  gcloud auth application-default login
  ```
  ```bash
  gcloud auth application-default set-quota-project
  ```

## Setup Instructions

### 1. Create Agent Identity Auth Connector

The agent identity auth connector must be handled using the `gcloud` CLI. Here is an example command to set that up:

```bash
gcloud alpha agent-identity connectors create example_provider \
    --location="<your region>" \
    --two-legged-oauth-client-id="<example client id>" \
    --two-legged-oauth-client-secret="<example client secret>" \
    --two-legged-oauth-token-endpoint="https://dev-yourdomain.us.auth0.com/oauth/token"
```

### 2. Deploy MCP Server

The MCP server can be deployed using the provided deployment script:

```bash
./deploy_mcp.sh
```

**Note:** The environment variables in your setup will need to be adjusted to match your auth provider configuration. Some values, namely the issuer and `MCP_SERVER_URL`, may only be known after the first deployment and will have to be retroactively populated.

### 3. Add MCP Server to Agent Registry

Once the MCP server is deployed to Cloud Run, it can be added to the Agent Registry tool catalog. This must be done via the Google Cloud Console:

1. Use the `tool_description.json` file for the input schema definition.
2. We recommend naming the MCP Server "**Secure Data Server**" and giving it the description "**Fetches secure data**".
3. After the MCP Server registration is complete, grab the `MCP_SERVER_NAME` value from the ADK code snippet produced. You will need this for your local environment configuration.

### 4. Run ADK Agent Locally

The ADK agent located in the `example_agent` directory can be run locally.

1. Navigate to the top-level `example_agent` directory.
2. Run `uv sync` to install dependencies.
3. Create a `.env` file prior to running the agent with the following values:

```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=<your project>
GOOGLE_CLOUD_LOCATION=<your region>
TOOL_NAME=projects/<project>/locations/<region>/mcpServers/<your agent connector>
CONNECTOR_NAME=<name of connector you created earlier>
```

4. Run the agent using the following command:

```bash
uv run adk web
```

You can test the agent using a prompt such as "fetch the latest secure data" to invoke the tool.
