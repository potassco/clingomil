
#const size=0.
#const skolems=0.
skolem(1..skolems).

binary_bg(pour_tea,X,Y) :- Y = @pour_tea(X), state(X).
binary_bg(pour_coffee,X,Y) :- Y = @pour_coffee(X), state(X).
binary_bg(move_right,X,Y) :- Y = @move_right(X), state(X).

#external wants_tea(X) : state(X).
unary_bg(wants_tea,X) :- wants_tea(X), state(X).

#external wants_coffee(X) : state(X).
unary_bg(wants_coffee,X) :- wants_coffee(X), state(X).

#external at_end(X) : state(X).
unary_bg(at_end,X) :- at_end(X), state(X).

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
state(Y) :- deduced(_,_,Y).

deduced(P,X,Y) :- binary_bg(P,X,Y).

:- pos_ex(P,X,Y1), deduced(P,X,Y2), Y1 != Y2.
:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
