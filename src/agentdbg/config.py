"""
Configuration for AgentDBG.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# Cost per 1K tokens for different models (as of 2024)
MODEL_COSTS: dict[str, dict[str, float]] = {
    # OpenAI
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "o1": {"input": 0.015, "output": 0.06},
    "o1-mini": {"input": 0.003, "output": 0.012},
    "o3-mini": {"input": 0.0011, "output": 0.0044},

    # Anthropic
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-5-haiku": {"input": 0.0008, "output": 0.004},
    "claude-3-7-sonnet": {"input": 0.003, "output": 0.015},
    "claude-opus-4": {"input": 0.015, "output": 0.075},
    "claude-sonnet-4": {"input": 0.003, "output": 0.015},
}


def get_model_cost(model: str, input_tokens: int, output_tokens: int) -> tuple[float, float]:
    """Calculate cost for a model based on token counts."""
    # Normalize model name
    model_lower = model.lower()

    # Find matching cost entry
    costs = None
    for key in MODEL_COSTS:
        if key in model_lower:
            costs = MODEL_COSTS[key]
            break

    if costs is None:
        # Default to GPT-4o pricing if unknown
        costs = MODEL_COSTS["gpt-4o"]

    input_cost = (input_tokens / 1000) * costs["input"]
    output_cost = (output_tokens / 1000) * costs["output"]

    return input_cost, output_cost


@dataclass
class DebugConfig:
    """Configuration for the debugger."""

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8765
    ui_port: int = 8766

    # Storage settings
    db_path: str = ".agentdbg/traces.db"
    max_traces: int = 1000  # Max traces to keep in DB

    # Debugging settings
    auto_pause_on_error: bool = True
    auto_pause_on_cost: float | None = None  # Pause when cost exceeds this
    auto_pause_on_tokens: int | None = None  # Pause when tokens exceed this

    # Instrumentation settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    max_input_size: int = 10000  # Truncate inputs larger than this
    max_output_size: int = 10000  # Truncate outputs larger than this

    # Which providers to auto-instrument
    instrument_openai: bool = True
    instrument_anthropic: bool = True
    instrument_langchain: bool = True

    # Logging
    log_level: Literal["debug", "info", "warning", "error"] = "info"

    # UI settings
    theme: Literal["dark", "light"] = "dark"

    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "ui_port": self.ui_port,
            "db_path": self.db_path,
            "max_traces": self.max_traces,
            "auto_pause_on_error": self.auto_pause_on_error,
            "auto_pause_on_cost": self.auto_pause_on_cost,
            "auto_pause_on_tokens": self.auto_pause_on_tokens,
            "capture_inputs": self.capture_inputs,
            "capture_outputs": self.capture_outputs,
            "max_input_size": self.max_input_size,
            "max_output_size": self.max_output_size,
            "instrument_openai": self.instrument_openai,
            "instrument_anthropic": self.instrument_anthropic,
            "instrument_langchain": self.instrument_langchain,
            "log_level": self.log_level,
            "theme": self.theme,
        }
