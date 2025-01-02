def calculate_portfolio_metrics(wallet_address=None, address=None):
    """
    Calculates various portfolio metrics for a given wallet address
    Args:
        wallet_address: str - The wallet address to analyze
        address: str - Alternative parameter name for wallet_address
    """
    # Handle different parameter names
    final_address = wallet_address or address or "default_address"
    
    return {
        "status": "success",
        "data": {
            "wallet_address": final_address,
            "total_value": "123,456.78 USD",
            "diversity_score": "7.5/10",
            "risk_exposure": "medium",
            "top_holdings": ["BTC", "ETH", "SOL"]
        }
    }
