from mcp.server.fastmcp import FastMCP
from genai.report_agent import detect_potholes_tool, policy_lookup_tool, generate_report

mcp = FastMCP("PotholeDetection-MCP")

@mcp.tool()
def detect_potholes(image_path: str) -> str:
    """Run pothole/speed-bump detection on an image and return counts."""
    return detect_potholes_tool(image_path)

@mcp.tool()
def check_maintenance_policy(query: str) -> str:
    """Check road maintenance policy or incident history for a given scenario."""
    return policy_lookup_tool(query)

@mcp.tool()
def generate_maintenance_report(image_path: str) -> str:
    """Generate a full maintenance priority report for a road image."""
    return generate_report(image_path)

if __name__ == "__main__":
    mcp.run()
