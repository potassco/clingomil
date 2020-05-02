
#const size=0.
#const skolems=0.
skolem(1..skolems).

binary_bg(remove,X,Y) :- Y = @remove(X), state(X).
binary_bg(switch,X,Y) :- Y = @switch(X), state(X).

#external isA(X) : state(X).
unary_bg(isA,X) :- isA(X), state(X).

#external isB(X) : state(X).
unary_bg(isB,X) :- isB(X), state(X).

#external isC(X) : state(X).
unary_bg(isC,X) :- isC(X), state(X).

order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

{meta(precon,P1,P2,P3)} :- order(P1,P3), unary_bg(P2,X), deduced(P3,X,Y).
{meta(postcon,P1,P2,P3)} :- order(P1,P2), deduced(P2,X,Y), unary_bg(P3,Y).
{meta(chain,P1,P2,P3)} :- order(P1,P2), order(P1,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
{meta(tailrec,P1,P2,n)} :- order(P1,P2), deduced(P2,X,Z), deduced(P1,Z,Y).

deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

state(X) :- pos_ex(_,X,_).
state(X) :- neg_ex(_,X,_).
state(Y) :- deduced(_,_,Y).

deduced(P,X,Y) :- binary_bg(P,X,Y).

:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- neg_ex(P,X,Y), deduced(P,X,Y).


:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
