from azureml.core import Run
from functools import wraps

def mlrun(f):
    @wraps(f)

    def inner(*args, **kwargs):
        run = Run.get_context()

        kwargs["run"] = run
        result = f(*args, **kwargs)

        run.complete()

        return result
    
    return inner