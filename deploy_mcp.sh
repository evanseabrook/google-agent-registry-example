#!/bin/bash

echo "Deploying the FastMCP server to Cloud Run..."
gcloud run deploy auth0-mcp-server \
    --source example_mcp \
    --allow-unauthenticated \
    --set-env-vars="MCP_SERVER_AUTH0_ISSUER=https://dev-ra4bqr1pghpwdkde.us.auth0.com/,MCP_SERVER_AUTH0_CONFIG_URL=https://dev-ra4bqr1pghpwdkde.us.auth0.com/.well-known/jwks.json,MCP_SERVER_URL=https://auth0-mcp-server-1075043300078.us-central1.run.app" \
    --region us-central1 \
    --clear-base-image

echo ""
echo "Deployment initiated!"
echo "NOTE: Once deployed, copy the Cloud Run URL."
echo "You will use this URL as the Audience in Auth0, and update the Cloud Run service's environment variable MCP_SERVER_URL to match it."
