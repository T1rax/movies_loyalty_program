CREATE_PROMO = """
    INSERT INTO promos(campaign_name, promo_code, products, "type", "value", duration, activation_date, user_ids, activations_limit)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    RETURNING *;
"""

GET_PROMO_BY_PROMO_CODE = """
    SELECT id, campaign_name, promo_code, products, "type", "value", duration, activation_date, user_ids, activations_limit, created_dt, updated_dt
    FROM promos
    WHERE promo_code=$1 and not deactivated;
"""

GET_PROMO_ACTIVATION = """
    SELECT id, promo_id, user_id, activations_cnt
    FROM promos_activations
    WHERE promo_id=$1 and user_id=$2;
"""

CREATE_PROMO_ACTIVATION = """
    INSERT INTO promos_activations (promo_id, user_id)
    VALUES ($1, $2)
    ON CONFLICT (promo_id, user_id) 
    DO UPDATE SET promo_id=$1, user_id=$2, updated_dt = now();
"""

GET_ACTIVATIONS_COUNT = """
    SELECT COUNT(promo_id)
    FROM promos_activations
    WHERE promo_id=$1;
"""

SET_DEACTIVATED_PROMO = """
    UPDATE promos SET deactivated = TRUE, updated_dt = now()
    WHERE id=$1;
"""
