import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agentapp.agentsingle import setup_and_run, run_agent, main_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

@pytest.fixture
def mock_session_service():
    svc = InMemorySessionService()
    svc.create_session = AsyncMock(return_value=MagicMock())
    return svc

@pytest.fixture
def mock_runner(mock_session_service):
    runner = MagicMock(spec=Runner)
    runner.run_async = AsyncMock()
    return runner

@patch("agentapp.agentsingle.InMemorySessionService", return_value=MagicMock(create_session=AsyncMock()))
@patch("agentapp.agentsingle.Runner")
def test_setup_and_run_creates_session_and_runner(mock_runner_cls, mock_svc_cls):
    # Ensure no exceptions when setting up
    async def dummy():
        # Patch input to break immediately
        with patch("builtins.input", side_effect=["quit"]):
            await setup_and_run()
    asyncio.run(dummy())
    mock_svc_cls.assert_called_once()
    mock_runner_cls.assert_called_once()

@patch("agentapp.agentsingle.Runner")
@pytest.mark.asyncio
async def test_run_agent_returns_text(mock_runner_cls):
    fake_event1 = MagicMock(
        is_final_response=MagicMock(return_value=True),
        content=types.Content(role="assistant", parts=[types.Part(text=""), types.Part(text=None)])
    )
    fake_event2 = MagicMock(
        is_final_response=MagicMock(return_value=True),
        content=types.Content(role="assistant", parts=[types.Part(text="Hello user!")])
    )
    runner = mock_runner_cls.return_value

    async def async_iterable(seq):
        for item in seq:
            yield item

    runner.run_async.return_value = async_iterable([fake_event1, fake_event2])

    result = await run_agent(runner, "test query")
    assert result == "Hello user!"

@patch("agentapp.agentsingle.Runner")
@pytest.mark.asyncio
async def test_run_agent_handles_no_text(mock_runner_cls):
    fake_event = MagicMock(
        is_final_response=MagicMock(return_value=True),
        content=types.Content(role="assistant", parts=[types.Part(text="")])
    )
    runner = mock_runner_cls.return_value

    async def async_iterable(seq):
        for item in seq:
            yield item

    runner.run_async.return_value = async_iterable([fake_event])

    result = await run_agent(runner, "test query")
    assert result == "No response generated from the agent."
