import time
from functools import wraps
import logging

logging.basicConfig(filename='property_table.log', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        LOGGER.info("Total time running {}: {} seconds".format(function.func_name,
                                                               str(t1-t0)))
        return result
    return function_timer
