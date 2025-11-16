"""Tests for Enterprise Agent."""

import pytest
from src.agents.enterprise_agent import EnterpriseAgent


def test_agent_initialization():
    """Test agent initialization with default config."""
    agent = EnterpriseAgent(config_dict={
        "agent": {
            "name": "Test Agent",
            "version": "1.0.0"
        }
    })
    
    assert agent.name == "Test Agent"
    assert agent.version == "1.0.0"


def test_agent_capabilities():
    """Test getting agent capabilities."""
    agent = EnterpriseAgent(config_dict={
        "agent": {
            "name": "Test Agent",
            "capabilities": ["test_capability"]
        }
    })
    
    capabilities = agent.get_capabilities()
    assert "test_capability" in capabilities


def test_task_execution():
    """Test task execution."""
    agent = EnterpriseAgent(config_dict={
        "agent": {
            "name": "Test Agent",
            "version": "1.0.0"
        }
    })
    
    result = agent.execute_task("Test task")
    assert result["status"] in ["success", "error"]
    assert "timestamp" in result
    assert result["agent"] == "Test Agent"


def test_agent_status():
    """Test getting agent status."""
    agent = EnterpriseAgent(config_dict={
        "agent": {
            "name": "Test Agent",
            "version": "1.0.0"
        }
    })
    
    status = agent.get_status()
    assert status["name"] == "Test Agent"
    assert status["status"] == "active"
    assert "timestamp" in status

