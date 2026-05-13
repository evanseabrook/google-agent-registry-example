import os
import logging
import asyncio
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

verifier = JWTVerifier(
    jwks_uri=os.environ.get("MCP_SERVER_AUTH0_CONFIG_URL"),
    issuer=os.environ.get("MCP_SERVER_AUTH0_ISSUER"),
    audience=os.environ.get("MCP_SERVER_URL")
)

# 1. Define the FastMCP Server
mcp = FastMCP("Auth0SecuredServer", auth=verifier)

@mcp.tool()
def get_secure_data(query: str) -> str:
    """A tool that returns highly secure data, protected by Auth0."""
    logger.info(f"Accessing secure data for query: {query}")
    return f"SECURE_DATA: You successfully accessed the secured MCP tool with query '{query}'!"

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
