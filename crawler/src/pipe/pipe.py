import abc
import typing

class Pipe(abc.ABC):

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def pipeline(self) -> typing.Any:
        '''
            Execute all necessary methods 
            to execute a pipeline
        '''
    