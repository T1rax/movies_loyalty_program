"""
init
promocodes
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table if not exists promocodes (
            promocode varchar(20) primary key,
            campaign_name varchar not null,
            products jsonb not null,
            type varchar(20) not null,
            value smallint not null,
            duration smallint not null,
            activation_date timestamp with time zone default now(),
            user_ids jsonb not null,
            activations_limit smallint not null,
            deactivated boolean default false,
            creation_dt timestamp with time zone default now(),
            update_dt timestamp with time zone default now()
        );
        
        create table if not exists promocode_uses (
            id bigserial primary key,
            promocode varchar(20) not null,
            user_id uuid not null,
            activation_dt timestamp with time zone default now()
        );
        """,
        """
        drop table if exists promocodes;
        drop table if exists promocode_uses;
        """
    )
]
