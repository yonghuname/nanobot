"""Test parameter validation for agent tools."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from nanobot.agent.subagent import SubagentManager
from nanobot.agent.tools.spawn import SpawnTool
from nanobot.agent.tools.web import WebFetchTool, WebSearchTool
from nanobot.config.schema import WebSearchConfig


@pytest.mark.asyncio
async def test_web_search_validates_empty_query():
    """Test that WebSearchTool rejects empty queries."""
    tool = WebSearchTool(config=WebSearchConfig(provider="duckduckgo"))

    # None query
    result = await tool.execute(query=None)
    assert "Error" in result
    assert "empty" in result.lower()

    # Empty string query
    result = await tool.execute(query="")
    assert "Error" in result
    assert "empty" in result.lower()

    # Whitespace-only query
    result = await tool.execute(query="   ")
    assert "Error" in result
    assert "empty" in result.lower()


@pytest.mark.asyncio
async def test_web_fetch_validates_missing_url():
    """Test that WebFetchTool rejects missing URL."""
    tool = WebFetchTool()

    # None URL
    result = await tool.execute(url=None)
    assert "error" in result.lower()
    assert "required" in result.lower()


@pytest.mark.asyncio
async def test_spawn_tool_validates_empty_task():
    """Test that SpawnTool rejects empty task descriptions."""
    # Create a mock SubagentManager
    mock_manager = MagicMock(spec=SubagentManager)
    mock_manager.spawn = AsyncMock(return_value="spawned")

    tool = SpawnTool(manager=mock_manager)
    tool.set_context("cli", "test")

    # None task
    result = await tool.execute(task=None)
    assert "Error" in result
    assert "empty" in result.lower()
    mock_manager.spawn.assert_not_called()

    # Empty string task
    result = await tool.execute(task="")
    assert "Error" in result
    assert "empty" in result.lower()

    # Whitespace-only task
    result = await tool.execute(task="   ")
    assert "Error" in result
    assert "empty" in result.lower()


@pytest.mark.asyncio
async def test_valid_parameters_still_work():
    """Test that valid parameters pass validation."""
    mock_manager = MagicMock(spec=SubagentManager)
    mock_manager.spawn = AsyncMock(return_value="Task spawned")

    spawn_tool = SpawnTool(manager=mock_manager)
    spawn_tool.set_context("cli", "test")

    # Valid task should work
    result = await spawn_tool.execute(task="Do something useful")
    assert "Error" not in result
    mock_manager.spawn.assert_called_once()
