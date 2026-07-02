from google.adk.events.event import Event

from app.agent import guardrail_node


def test_guardrail_node_safe():
    # Pass None for Context as it is not actively used in the guardrail logic.
    res = guardrail_node(None, "I am feeling stressed about work.")
    assert isinstance(res, Event)
    assert res.actions.route == "safe"
    assert res.actions.state_delta["safety_flagged"] == "False"
    assert res.actions.state_delta["user_input"] == "I am feeling stressed about work."


def test_guardrail_node_crisis():
    res = guardrail_node(None, "I feel like I want to self-harm.")
    assert isinstance(res, Event)
    assert res.actions.route == "escalated"
    assert res.actions.state_delta["safety_flagged"] == "True"
    assert "988 Suicide & Crisis Lifeline" in res.actions.state_delta["crisis_response"]
