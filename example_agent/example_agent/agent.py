from google.adk.agents import Agent
from google.adk.auth.credential_manager import CredentialManager
from google.adk.integrations.agent_identity import GcpAuthProvider
from google.adk.integrations.agent_identity import GcpAuthProviderScheme
from google.adk.integrations.agent_registry import AgentRegistry
import os


# The name of the tool as registered in the Vertex AI Agent Registry
mcp_server_name = os.environ.get("TOOL_NAME")
connector_name = os.environ.get("CONNECTOR_NAME")
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION")

# This is necessary to access the agent identity data connector
CredentialManager.register_auth_provider(GcpAuthProvider())

auth_scheme = GcpAuthProviderScheme(
    name=f"projects/{project_id}/locations/{location}/connectors/{connector_name}"
)

registry = AgentRegistry(
    project_id=project_id,
    location=location,
)
# 1. Initialize the toolset simply by referencing the registered tool name.
# The Agent Engine dynamically resolves the URL, looks up the Auth Provider, 
# fetches the Auth0 token, and injects the Authorization headers transparently.
mcp_toolset = registry.get_mcp_toolset(mcp_server_name=mcp_server_name, auth_scheme=auth_scheme)

# 2. Initialize the agent with the toolset
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    instruction="""You are a helpful assistant with access to a highly secure MCP tool.
    Whenever a user asks for secure data, use your registered tool to fetch it for them.""",
    tools=[mcp_toolset]
)

