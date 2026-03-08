"""
Demo Script for Recording Video/GIF

This script simulates a realistic AI agent workflow with:
- Multiple LLM calls
- Tool usage
- Cost accumulation
- An error that gets caught

Run with:
    agentdbg run examples/demo_for_video.py

Then record your screen showing the UI at http://localhost:8766
"""

import time
from agentdbg import trace, traced, get_debugger, SpanKind, CostInfo


@traced(name="analyze_user_query", kind=SpanKind.LLM_CALL)
def analyze_query(query: str) -> dict:
    """Simulate analyzing user query with LLM."""
    time.sleep(1.5)  # Simulate API latency

    debugger = get_debugger()
    span = debugger.get_current_span()
    if span:
        span.input_data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        }
        span.cost = CostInfo(
            input_tokens=156,
            output_tokens=89,
            total_tokens=245,
            total_cost=0.0045,
            model="gpt-4o"
        )
        span.output_data = {
            "intent": "search_and_summarize",
            "entities": ["AI agents", "debugging"],
            "confidence": 0.94
        }

    return {"intent": "search", "topic": "AI debugging"}


@traced(name="search_knowledge_base", kind=SpanKind.TOOL_CALL)
def search_knowledge_base(topic: str) -> list:
    """Simulate searching a knowledge base."""
    time.sleep(1.0)

    debugger = get_debugger()
    span = debugger.get_current_span()
    if span:
        span.input_data = {"query": topic, "limit": 5}
        span.output_data = {
            "results": [
                {"title": "AI Agent Best Practices", "score": 0.95},
                {"title": "Debugging LLM Applications", "score": 0.89},
                {"title": "Cost Optimization for AI", "score": 0.82},
            ],
            "total_found": 3
        }

    return ["result1", "result2", "result3"]


@traced(name="generate_response", kind=SpanKind.LLM_CALL)
def generate_response(context: list) -> str:
    """Simulate generating final response."""
    time.sleep(2.0)

    debugger = get_debugger()
    span = debugger.get_current_span()
    if span:
        span.input_data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "Summarize the search results."},
                {"role": "user", "content": f"Context: {context}"}
            ],
            "temperature": 0.7
        }
        span.cost = CostInfo(
            input_tokens=423,
            output_tokens=256,
            total_tokens=679,
            total_cost=0.0156,
            model="gpt-4o"
        )
        span.output_data = {
            "response": "Based on my analysis, here are the key insights about AI agent debugging...",
            "finish_reason": "stop"
        }

    return "AI agents require robust debugging tools for production use."


@traced(name="validate_response", kind=SpanKind.TOOL_CALL)
def validate_response(response: str) -> bool:
    """Simulate validation that might fail."""
    time.sleep(0.8)

    debugger = get_debugger()
    span = debugger.get_current_span()
    if span:
        span.input_data = {"response_length": len(response)}
        span.output_data = {"valid": True, "checks_passed": ["length", "format", "safety"]}

    return True


@traced(name="agent_workflow", kind=SpanKind.CHAIN)
def run_agent(user_query: str) -> str:
    """Main agent workflow."""
    print(f"Processing: {user_query}")
    print()

    # Step 1: Analyze
    print("Step 1: Analyzing query...")
    analysis = analyze_query(user_query)

    # Step 2: Search
    print("Step 2: Searching knowledge base...")
    results = search_knowledge_base(analysis["topic"])

    # Step 3: Generate
    print("Step 3: Generating response...")
    response = generate_response(results)

    # Step 4: Validate
    print("Step 4: Validating response...")
    is_valid = validate_response(response)

    print()
    print(f"Done! Response: {response[:50]}...")

    return response


def main():
    print("=" * 60)
    print("  Agent DevTools - Live Demo")
    print("=" * 60)
    print()
    print("Open http://localhost:8766 to see the debugger UI")
    print()
    print("Starting agent in 3 seconds...")
    time.sleep(3)
    print()

    debugger = get_debugger()
    debugger.start_trace(
        name="customer_support_agent",
        metadata={
            "user_id": "demo_user",
            "session": "video_recording"
        }
    )

    try:
        result = run_agent("How do I debug my AI agents effectively?")
        print()
        print("=" * 60)

        # Show final stats
        traces = debugger.get_all_traces()
        if traces:
            trace = traces[-1]
            print(f"  Total Spans: {len(trace.spans)}")
            print(f"  Total Cost: ${trace.total_cost:.4f}")
            print(f"  Total Tokens: {trace.total_tokens}")
        print("=" * 60)

    finally:
        debugger.end_trace()

    print()
    print("Demo complete! Check the UI for the full trace.")
    print()
    # Keep running so UI stays accessible
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
