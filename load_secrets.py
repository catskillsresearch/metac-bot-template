def load_secrets():
    ## Secrets
    from omegaconf import OmegaConf
    config = OmegaConf.load("../tokens.yaml")
    
    import os
    for key in config:
        os.environ[key] = config[key]