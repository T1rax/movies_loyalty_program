CREATE_PROMO = """
    INSERT INTO loyalty(campaign_name, promo_code, products, "type", "value", duration, activation_date, user_id, activations_limit)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    RETURNING *;
"""
