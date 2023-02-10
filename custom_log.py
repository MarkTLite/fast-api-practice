def log(tag: str = '', msg: str = ''):
    """Custom logging"""
    with open('log.txt', 'w+') as log:
        log.write(f'{tag} : {msg} \n')