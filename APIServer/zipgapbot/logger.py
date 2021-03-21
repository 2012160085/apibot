from datetime import datetime
import time
import inspect
__configure__ = None
def setconfigure(conf):
    global __configure__
    __configure__ = conf
    for key in ["logdir"]:
        if key not in conf.keys():
            raise Exception(key + " key not exist in config")
    return __configure__

def write(msg): 
    ymd = datetime.now().strftime("%Y%m%d")
    with open(ymd+"_"+__configure__["logdir"],'a') as f:
        f.write(msg+"\n")
    print(msg)


def logger_timestamp():
    def decorator(function):
        def wrapper(*args, **kwargs):
            logtxt = "[{_hms}] {_argument} {_args} {_kwargs}"
            logf = logtxt.format(_hms=datetime.now().strftime("%H:%M:%S")
                                ,_args = str(*args)
                                ,_kwargs = str(**kwargs)
                                ,_argument = function.__name__)
            write(logf)
            result = function(*args, **kwargs)
            logtxt = " : {_result}\n"
            logf = logtxt.format(_result=result)
            write(logf)
            return result
        return wrapper
    return decorator

def log_with_trycatch(func):
    def wrapper(*func_args, **func_kwargs):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        args = func_args[:len(arg_names)]
        defaults = func.__defaults__ or ()
        args = args + defaults[len(defaults) - (func.__code__.co_argcount - len(args)):]
        params = list(zip(arg_names, args))
        args = func_args[len(arg_names):]
        if args: params.append(('args', args))
        if func_kwargs: params.append(('kwargs', func_kwargs))
        write(datetime.now().strftime("%H:%M:%S") + " " + func.__name__ + ' (' + ', '.join('%s = %r' % p for p in params) + ' )')
        try:
            result = func(*func_args, **func_kwargs)
            write("-->"+str(result))
            return result
        except Exception as e:
            write("-->[**ERROR**] "+str(e))
    return wrapper