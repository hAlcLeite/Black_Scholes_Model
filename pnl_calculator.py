def calculate_pnl(option_type: str, purchase_price: float, current_price: float):
    """
    Calculates the PnL for an option.

    Args:
        option_type (str): Type of the option ('call' or 'put')
        purchase_price (float): The price at which the option was purchased
        current_price (float): The current price of the option

    Returns:
        float: The profit or loss value
    """
    if option_type not in ['call', 'put']:
        raise ValueError("Option type must be either 'call' or 'put'.")

    pnl = current_price - purchase_price
    return pnl
