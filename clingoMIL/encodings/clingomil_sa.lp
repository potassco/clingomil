
% #const size=0.
% #const skolems=0.
skolem(1..skolems).

unary_bg(A,N) :- (A,N) = @unary().
binary_bg(A,N1,N2) :- (A,N1,N2) = @binary().

{ pos(ID,X,Y,Z) } :- (ID,X,Y,Z) = @checkpos().
:- pos_ex(ID,_,_,_), not pos(ID,_,_,_).
:- pos(_,X,Y,Z), not deduced(X,Y,Z).

order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos(_,X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos(_,X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

deduced(P,X,Y) :- binary_bg(P,X,Y).

:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
