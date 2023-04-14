#################
# Free API URLs #
#################
random_user_api_url = "https://randomuser.me/api/"

#########
# CACHE #
#########
default_cache_dir = ".cache"
allowed_cache_backends = ["sqlite"]
allowed_serializers = ["json", "bson", "yaml"]

default_cache_settings = {
    "cache_name": "default_cache",
    "cache_dir": ".cache",
    "backend": "sqlite",
}


#################################
# REQUEST CLIENT SETTINGS DICTS #
#################################
default_req_client_settings = {
    "url": None,
    "expire_after": 900,
    "allowable_methods": ("GET", "POST"),
    "stale_if_error": True,
}

##########
# CONFIG #
##########
allowed_conf_filetypes = [".yaml", ".yml", ".env"]
