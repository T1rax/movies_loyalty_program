"""
init
promo_codes
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table if not exists promos (
            id bigserial primary key,
            promo_code varchar(20) not null,
            campaign_name varchar not null,
            products varchar array not null,
            type varchar(20) not null,
            value smallint not null,
            duration smallint,
            activation_date timestamp with time zone default now(),
            user_ids uuid array not null,
            activations_limit smallint not null,
            deactivated boolean default false,
            created_dt timestamp with time zone default now(),
            updated_dt timestamp with time zone default now()
        );
        
        create unique index if not exists idx_promos_promo_code
        on promos(promo_code);
        
        create table if not exists promos_activations (
            id bigserial primary key,
            promo_id bigserial not null,
            user_id uuid not null,
            activated_dt timestamp with time zone default now()
        );
        """,
        """
        drop index if exists idx_promos_promo_code;
        drop table if exists promos;
        drop table if exists promos_activations;
        """
    )
]
