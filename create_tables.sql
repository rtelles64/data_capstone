CREATE TABLE public.cities (
	city_id int NOT NULL AUTO_INCREMENT,
	city varchar(256),
	state varchar(256),
	st_code varchar(10),
	race varchar(256),
	CONSTRAINT cities_pkey PRIMARY KEY (city_id)
);

CREATE TABLE public.imm_dem (
	imm_dem_id int NOT NULL AUTO_INCREMENT,
	city_id int NOT NULL,
	city varchar(256),
	state_id int NOT NULL,
	state varchar(256),
	state_code varchar(10),
	entry_port_id int NOT NULL,
	travel_mode int,
	gender varchar(3),
	foreign_born numeric,
	race varchar(256),
	visa_type varchar(5),
	CONSTRAINT immdem_pkey PRIMARY KEY (imm_dem_id)
);

CREATE TABLE public.entry_ports (
	entry_port_id int NOT NULL AUTO_INCREMENT,
	entry_port varchar(256),
	travel_mode int,
	dest_state varchar(5),
	visa_type varchar(5),
	CONSTRAINT entryport_pkey PRIMARY KEY (entry_port_id)
);

CREATE TABLE public.staging_dem (
	dem_id int NOT NULL AUTO_INCREMENT,
	city varchar(256),
	state varchar(256),
	median_age numeric,
	male_pop numeric,
	female_pop numeric,
	foreign_born numeric,
	state_code varchar(10),
	race varchar(256)
);

CREATE TABLE public.staging_imm (
	imm_id int NOT NULL AUTO_INCREMENT,
	entry_port varchar(256),
	travel_mode numeric,
	dest_state varchar(256),
	birth_year int,
	gender varchar(5),
	visa_type varchar(256)
);

CREATE TABLE public.states (
	state_id int NOT NULL AUTO_INCREMENT,
	state varchar(256),
	male_pop_total bigint,
	fem_pop_total bigint,
	foreign_born_tot bigint,
	CONSTRAINT states_pkey PRIMARY KEY (state_id)
);
