from typing import Callable, Any, Tuple, Type, Optional
import functools

import time

FUNC_t = Callable[..., Any]

def retry(max_trails:int=5, delay:Optional[float]=None,
        exceptions:Tuple[Type[Exception], ...] = (Exception, ),
        default: Any = None) -> Callable[[FUNC_t], FUNC_t]:
    def decorator(fn:FUNC_t) -> FUNC_t:
        @functools.wraps(fn)
        def warper(*args:Any, **kwargs:Any) -> Any:
            err: Optional[Exception] = None
            for _ in range(max_trails):
                try:
                    return  fn(*args, **kwargs)
                except exceptions as e:
                    err = e
                    if delay is not None:
                        time.sleep(delay)
            if default is not None:
                return default
            raise err # type: ignore
        return warper
    
    return decorator