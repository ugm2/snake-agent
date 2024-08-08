def state_to_key(state):
    """
    Convert a state to a string key for use in the Q-table.
    Example: (head_x, head_y, food_dx, food_dy, direction)
    """
    return tuple(round(x, 4) if isinstance(x, float) else x for x in state)