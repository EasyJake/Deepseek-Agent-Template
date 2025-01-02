def generate_trading_strategy(risk_level=None, budget=None, risk=None, amount=None):
    """
    Generates a basic trading strategy based on risk level and budget
    Args:
        risk_level: str - Risk level (low/medium/high)
        budget: float - Available budget
        risk: str - Alternative parameter name for risk_level
        amount: float - Alternative parameter name for budget
    """
    # Handle different parameter names
    final_risk = risk_level or risk or "medium"
    final_budget = budget or amount or 1000
    
    strategies = {
        "low": "Dollar-cost averaging with 70% stable coins",
        "medium": "Balanced portfolio with 50% major coins, 30% mid-caps",
        "high": "Leveraged trading with focus on emerging tokens"
    }
    
    return {
        "status": "success",
        "data": {
            "risk_level": final_risk,
            "budget": final_budget,
            "strategy": strategies.get(final_risk, "Invalid risk level"),
            "recommended_allocation": "Generated based on market conditions"
        }
    }
