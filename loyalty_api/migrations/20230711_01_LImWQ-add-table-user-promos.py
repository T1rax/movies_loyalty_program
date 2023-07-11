"""
add table user_promos
"""

from yoyo import step

__depends__ = {'20230709_02_ERJiu-add-column-updated-dt', '__init__'}

steps = [
    step(
        """
        create table if not exists user_promos (
            id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
            promo_id bigint not null,
            user_id uuid not null,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now()
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_user_promos_promo_id_user_id ON user_promos (promo_id, user_id);
        """,
        """
        drop table if exists user_promos;
        drop index if exists idx_user_promos_promo_id_user_id;
        """
    )
]
