from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from genai.rag_chain import build_rag_chain
from api.inference import run_inference

rag_chain = build_rag_chain()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def detect_potholes_tool(image_path: str) -> str:
    """Runs YOLO detection on an image file path and returns a summary string."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    detections = run_inference(image_bytes)
    pothole_count = sum(1 for d in detections if d["class"].lower() == "pothole")
    speedbump_count = sum(1 for d in detections if "speed" in d["class"].lower())
    return f"Detected {pothole_count} potholes and {speedbump_count} speed bumps. Raw: {detections}"

def policy_lookup_tool(query: str) -> str:
    """Answers questions about maintenance policy or past incidents using RAG."""
    result = rag_chain.invoke({"query": query})
    return result["result"]

tools = [
    Tool(name="DetectPotholes", func=detect_potholes_tool,
         description="Use this to run pothole/speed-bump detection on an image file path. Input: file path string."),
    Tool(name="PolicyLookup", func=policy_lookup_tool,
         description="Use this to check maintenance policy or past incident history for a given pothole count/severity.")
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def generate_report(image_path: str) -> str:
    prompt = (
        f"Analyze the road image at {image_path}. First detect potholes/speed bumps, "
        f"then look up the maintenance policy to determine priority level, "
        f"then write a 3-sentence maintenance report with a clear priority recommendation."
    )
    response = agent.invoke({"input": prompt})
    return response["output"]

if __name__ == "__main__":
    report = generate_report("sample_road.jpg")
    print(report)
