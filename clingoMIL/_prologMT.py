# Taken from https://github.com/yuce/pyswip/issues/3#issuecomment-355458825
# """pyswip doesn't support multithreading at all. IMHO, contemporary API (or
#    at least pyswip.prolog module) needs to be redesigned from the scratch,
#    see: http://www.swi-prolog.org/pldoc/man?section=foreignthread """
#
# """PrologMT is a drop-in replacement for pyswip.Prolog in your code. On each
#    query, native thread's local storage is scanned for the prolog engine
#    (PL_thread_self). If there is no pengine associated with the current
#    thread, new one will be created (PL_thread_attach_engine), without any
#    further resource management.
#    You couldn't use any term_t-related functions of libswipl from the thread
#    with no pengine - that leads to SEGFAULT. By default, the thread which
#    imports pyswip first, will be implicitly associated with the single
#    ("main") pengine, as PL_initialise is called on the pyswip.prolog module
#    top-level. """

import ctypes
from pyswip import Prolog, prolog, core


class PrologMT(Prolog):
    """Multi-threaded (one-to-one) pyswip.Prolog ad-hoc reimpl"""

    _swipl = core._lib

    PL_thread_self = _swipl.PL_thread_self
    PL_thread_self.restype = ctypes.c_int

    PL_thread_attach_engine = _swipl.PL_thread_attach_engine
    PL_thread_attach_engine.argtypes = [ctypes.c_void_p]
    PL_thread_attach_engine.restype = ctypes.c_int

    @classmethod
    def _init_prolog_thread(cls):
        pengine_id = cls.PL_thread_self()
        if pengine_id == -1:
            pengine_id = cls.PL_thread_attach_engine(None)
            # print("{INFO} attach pengine to thread: %d" % pengine_id)
        if pengine_id == -1:
            raise prolog.PrologError(
                "unable to attach new Prolog engine to the thread"
            )
        elif pengine_id == -2:
            # print("{WARN} Single-threaded swipl build, beware!")
            raise prolog.PrologError("single-threaded swipl build")

    class _QueryWrapper(Prolog._QueryWrapper):
        def __call__(self, *args, **kwargs):
            PrologMT._init_prolog_thread()
            return super().__call__(*args, **kwargs)
