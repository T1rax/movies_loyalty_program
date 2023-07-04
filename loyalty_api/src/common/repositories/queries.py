CREATE_PROMO = """
    INSERT INTO promos(campaign_name, promo_code, products, "type", "value", duration, activation_date, user_ids, activations_limit)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    RETURNING *;
"""
