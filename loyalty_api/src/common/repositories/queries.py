CREATE_PROMO = """
    INSERT INTO promos(campaign_name, promo_code, products, "type", "value", duration, activation_date, activations_limit)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    RETURNING *;
"""

GET_PROMO_BY_PROMO_CODE = """
    SELECT id, campaign_name, promo_code, products, "type", "value", duration, activation_date, activations_limit, linked_to_user, deactivated, created_dt, updated_dt
    FROM promos
    WHERE promo_code=$1;
"""

GET_PROMO_ACTIVATION = """
    SELECT id, promo_id, user_id, created_dt, updated_dt
    FROM promos_activations
    WHERE promo_id=$1 and user_id=$2;
"""

CREATE_PROMO_ACTIVATION = """
    INSERT INTO promos_activations (promo_id, user_id)
    VALUES ($1, $2);
"""

GET_ACTIVATIONS_COUNT = """
    SELECT COUNT(promo_id)
    FROM promos_activations
    WHERE promo_id=$1;
"""

SET_FLAG_DEACTIVATED_PROMO = """
    UPDATE promos SET deactivated = $2, updated_dt = now()
    WHERE id=$1;
"""

CREATE_USER_PROMOS = """
    INSERT INTO user_promos (promo_id, user_id)
    VALUES ($1, $2)
    ON CONFLICT (promo_id, user_id)
    DO UPDATE SET promo_id=$1, user_id=$2, updated_dt = now();
"""

GET_USER_PROMO = """
    SELECT id, promo_id, user_id, created_dt, updated_dt
    FROM user_promos
    WHERE promo_id=$1 and user_id=$2;
"""

SET_FLAG_LINKED_TO_USER = """
    UPDATE promos SET linked_to_user = TRUE, updated_dt = now()
    WHERE id=$1;
"""

DELETE_USER_PROMO_ACTIVATION = """
    DELETE
    FROM promos_activations
    WHERE promo_id=$1 and user_id=$2;
"""

GET_PROMO_USAGE_HISTORY_BY_PROMO_IDS = """
    SELECT pa.id, pa.promo_id, p.campaign_name, pa.user_id, pa.created_dt, pa.updated_dt
    FROM promos_activations pa
    LEFT JOIN promos p ON p.id = pa.promo_id
    WHERE pa.promo_id = ANY($1);
"""

GET_PROMO_BY_CAMPAIGN_NAME = """
    SELECT id, campaign_name, promo_code, products, "type", "value", duration, activation_date, activations_limit, linked_to_user, deactivated, created_dt, updated_dt
    FROM promos
    WHERE campaign_name=$1;
"""

GET_PROMO_USAGE_HISTORY_BY_USER_ID = """
    SELECT pa.id, pa.promo_id, p.campaign_name, pa.user_id, pa.created_dt, pa.updated_dt
    FROM promos_activations pa
    LEFT JOIN promos p ON p.id = pa.promo_id
    WHERE pa.user_id = $1;
"""

CREATE_CARD = """
    INSERT INTO loyalty_cards(user_id, loyalty_level)
    VALUES ($1, $2)
    RETURNING *;
"""

GET_LOYALTY_CARD_BY_USER_ID = """
    SELECT id, user_id, loyalty_level, created_dt, updated_dt
    FROM loyalty_cards
    WHERE user_id=$1;
"""

CHANGE_LOYALTY_LEVEL = """
    UPDATE loyalty_cards SET loyalty_level = $2, updated_dt = now()
    WHERE user_id=$1
    RETURNING *;
"""

POINTS_LOYALTY_CARD = """
    INSERT INTO loyalty_transactions (loyalty_id, user_id, points, source)
    VALUES ($1, $2, $3, $4);
"""

GET_LOYALTY_CARD_BALANCE = """
    SELECT loyalty_id, user_id, sum(points) as balance
    FROM loyalty_transactions
    WHERE user_id = $1
    GROUP BY loyalty_id, user_id;
"""

GET_LOYALTY_CARD_BALANCE_HISTORY = """
    SELECT id, points, source, created_dt
    FROM loyalty_transactions
    WHERE user_id = $1
    ORDER BY created_dt DESC;
"""

GET_LOYALTY_CARD_FULL_INFO = """
    WITH card AS (
        SELECT id, user_id, loyalty_level, created_dt, updated_dt
        FROM loyalty_cards
        WHERE user_id=$1;
    ), balance AS (
        SELECT loyalty_id, user_id, sum(points) as
        FROM loyalty_transactions
        WHERE user_id = $1
        GROUP BY loyalty_id, user_id
    )
    SELECT
        c.id
        , c.user_id
        , c.loyalty_level
        , COALESCE(b.balance, 0)
        , c.created_dt
        , c.updated_dt
    FROM card AS c
    LEFT JOIN balance AS b
        ON c.user_id = b.user_id
    ;
"""
