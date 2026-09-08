def run_dcf(free_cash_flow, wacc, growth_rate, terminal_growth, net_debt, shares_outstanding, years=5):
    """
    Runs a simple 5-year DCF valuation.

    free_cash_flow: starting year FCF
    wacc: discount rate (as a decimal, e.g. 0.09 for 9%)
    growth_rate: annual FCF growth rate during forecast years (decimal)
    terminal_growth: growth rate assumed forever after year 5 (decimal)
    net_debt: company's total debt minus cash
    shares_outstanding: number of shares
    """
    projected_fcf = []
    fcf = free_cash_flow
    for year in range(1, years + 1):
        fcf = fcf * (1 + growth_rate)
        projected_fcf.append(fcf)

    # Discount each year's FCF back to today's value
    discounted_fcf = [
        fcf / ((1 + wacc) ** year)
        for year, fcf in enumerate(projected_fcf, start=1)
    ]

    # Terminal value: value of all cash flows after year 5, using Gordon Growth
    terminal_value = (projected_fcf[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
    discounted_terminal_value = terminal_value / ((1 + wacc) ** years)

    enterprise_value = sum(discounted_fcf) + discounted_terminal_value
    equity_value = enterprise_value - net_debt
    implied_share_price = equity_value / shares_outstanding if shares_outstanding else 0

    return {
        "projected_fcf": projected_fcf,
        "discounted_fcf": discounted_fcf,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "implied_share_price": implied_share_price,
    }


def sensitivity_table(free_cash_flow, net_debt, shares_outstanding, wacc_range, growth_range):
    """
    Builds a grid of implied share prices across different WACC and
    terminal growth rate assumptions, so you can see how sensitive
    the valuation is to your assumptions.
    """
    table = []
    for wacc in wacc_range:
        row = []
        for growth in growth_range:
            result = run_dcf(free_cash_flow, wacc, 0.05, growth, net_debt, shares_outstanding)
            row.append(round(result["implied_share_price"], 2))
        table.append(row)
    return table
