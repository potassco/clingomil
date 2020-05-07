
% #const size=X.
% #const skolems=Y. (does not make sense to be greater or equal to X)
skolem(1..skolems).

unary_bg(P,X) :- P = @unary(X), state(X).
binary_bg(P,X,Y) :- (P,Y) = @binary(X), state(X).

state(X) :- pos_ex(_,X,_).
state(X) :- neg_ex(_,X,_).
state(Y) :- deduced(_,_,Y).
deduced(P,X,Y) :- binary_bg(P,X,Y).

order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

#external functional.
:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- not functional, neg_ex(P,X,Y),  deduced(P,X,Y).
:-     functional, pos_ex(P,X,Y1), deduced(P,X,Y2), Y1 != Y2.
:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
