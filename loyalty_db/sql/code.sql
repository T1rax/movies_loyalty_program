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

drop table if exists promocodes;
drop table if exists promocode_uses;



create table if not exists loyalty_account (
    id bigserial primary key,
    user_id uuid not null,
    loyalty_level varchar(10) not null,
    creation_dt timestamp with time zone default now(),
    update_dt timestamp with time zone default now()
);

create table if not exists loyalty_transactions (
    id bigserial primary key,
    loyalty_id bigserial not null,
    user_id uuid not null,
    points smallint not null,
    source varchar,
    transaction_dt timestamp with time zone default now()
);

drop table if exists loyalty_account;
drop table if exists loyalty_transactions;