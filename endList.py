####NEED TO TEST!!!!####
##To Do: Make index request faster (avoid front processing if possible)##
class ProcessingDone(StandardError):
    pass

class endList():
    """A fucntional lazy list that allows for end concatination.

    To use: (endList is eL)
    eL[i]           -- Returns the i'th element of the endList (i>=0)
    eL(function)    -- Applies a function to elements of the endList
    eL[i:j]         -- Takes a slice of the endList
    eL_1 + eL_2     -- concatinates two endLists
    n * eL          -- Takes n copies of an endList and concatinates them together
    eL.copy()       -- Returns a copy of eL
    eL also acts like an iterable. """

    def __init__(self, inIterable):
        self._processedfront = []
        self._toGo = iter(inIterable)
        self._thenAfter = []
        self._compsFunc = []

    def _thisFunc(self, value):
        for f in self._compsFunc:
            value = f(value)
        return value

    def copy(self):
        ret = endList(self)
        return ret
    
    def pop(self):
        """pops the front element of the endList"""
        if len(self._processedfront)!=0:
            return self._processedfront.pop()
        else:
            processed = True
            try:
                self._processNext()
            except ProcessingDone:
                processed = False
            if not processed:
                raise IndexError
            else:
                return self._processedfront.pop()


    def push(self, item):
        """pushes a new element to the front of the endList"""
        self._processedfront.push(item)


    def _processNext(self):
        failure = True
        while(failure):
            failure = False
            try:
                self._processedfront.append(self._thisFunc(self._toGo.next()))
            except StopIteration:
                failure = True
            if failure:
                if len(self._thenAfter) != 0:
                    self._toGo = iter(self._thenAfter.pop())
                else:
                    raise ProcessingDone
        
        
    def _endCat(self, inIterable):
        if isinstance(inIterable, endList):
            self._thenAfter.append(inIterable.copy())
        else:
            self._thenAfter.append(endList(inIterable))

    def __call__(self, function):
        """Applies a function to the elements of endList. (map)"""
        
        if len(self._processedfront) != 0:
            self._thenAfter = [endList(self._toGo)] + self._thenAfter
            self._toGo = self._processedfront.__iter__() ##watch this later
            self._processedFront = []
        self._compsFunc.append(function)
        
    def  _sliceHelperFunct(self, sta, ste, sto):
            i = sta
            if sto == None:
                while(True):
                    yield self[i]
                    i+=ste
            else:
                while(abs(i-sto)>=abs(ste)):
                    yield self[i]
                    i+=ste

        
    def __getitem__ (self, index):
        if type(index) == slice:
            start = index.start
            step = index.step
            stop = index.stop
            if start == None:
                start = 0
            if step == None:
                step = 1
            return endList(self._sliceHelperFunct(start, step, stop))
                
        elif type(index) == int:
            if index<0:
                raise IndexError
            valuesToGet = index - len(self._processedfront)
            nothingLeft = False
            while(valuesToGet>=0):
                cantProcessNext = False
                try:
                    self._processNext()
                except ProcessingDone:
                    cantProcessNext = True
                if cantProcessNext:
                    raise IndexError
                valuesToGet -= 1
            return self._processedfront[index]
        elif type(index) == long:
            raise IndexError("index too far to process")
        else:
            raise TypeError
            

    def __iter__(self):
        curIndex = 0
        while True:
            IndexTooFar = False
            try:
                yield self[curIndex]
            except IndexError:
                IndexTooFar = True
            if IndexTooFar:
                break
            curIndex+=1
                

    def __add__(self, other):
        if not isinstance(other, endList):
            raise TypeError
        ret = self.copy()
        ret._endCat(other.copy())
        return ret

    def __rmul__(self, n):
        return self*n

    def __mul__(self, n):
        if n<0:
            raise ValueError
        ret = endList([])
        while(n>0):
            ret.endCat(self)
            n-= 1
        return ret

class endListRange(endList):
    def __init__(self, start, step = 1, stop = None):
        def makeGen(sta, ste, sto):
            i = sta
            if sto == None:
                while(True):
                    yield i
                    i+=ste
            else:
                while(abs(i-sto)>=abs(ste)):
                    yield i
                    i+=ste
        endList.__init__(self, makeGen(start, step, stop))



    
    

    
