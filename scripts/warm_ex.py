
import warnings

def get_user_warning(data):
    class HERE(UserWarning):
        pass
    setattr( HERE, 'data', data )
    return HERE

class Message(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b

def fxn():
    ##warnings.warn(Message('sample text','b'), UserWarning )
    warnings.warn(Message('sample text','b'), get_user_warning('other sample text',45) )
    ##warnings.warn(('sample text','b'), UserWarning )


with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")
    # Trigger a warning.
    fxn()
    # Verify some things
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    ##assert "deprecated" in str(w[-1].message)
    print (w[-1].filename, w[-1].lineno )
    print (w[-1].message)
