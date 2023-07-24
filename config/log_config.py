import logging
import uvicorn

FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

def init_loggers():
    
# create logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = uvicorn.logging.DefaultFormatter(FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)