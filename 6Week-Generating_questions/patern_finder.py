import inspect 

def OR_F(f1,f2):
    sig1=inspect.signature(f1)
    sig2=inspect.signature(f2)
    if(sig1!=sig2):
        raise Exception('functions must have the same signature')
    S=str(sig1)[1:-1]
    rfunct="lambda %s: f1(%s) or f2(%s)"%(S,S,S)
    return eval(rfunct,{'f1':f1,'f2':f2},None)

def AND_F(f1,f2):
    sig1=inspect.signature(f1)
    sig2=inspect.signature(f2)
    if(sig1!=sig2):
        raise Exception('functions must have the same signature')
    S=str(sig1)[1:-1]
    rfunct="lambda %s: f1(%s) and f2(%s)"%(S,S,S)
    return eval(rfunct,{'f1':f1,'f2':f2},None)
