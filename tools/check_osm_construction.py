from check_osm_life_cycle import get_by_life_cycle

if __name__ == "__main__":
    env_file = "env_conf/.check_osm_construction_env"
    get_by_life_cycle(env_file, "construction")
