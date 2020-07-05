
% #const size=X.
% #const skolems=Y. (does not make sense to be greater or equal to X)
skolem(1..skolems).

% BACKGROUND IMPORT
unary_bg(P,X) :- P = @unary(X), state(_,X).

binary_bg(P,X,Y) :- pos_ex(_,X,_), (P,Y) = @binary(X).
binary_bg(P,X,Y) :- neg_ex(_,X,_), (P,Y) = @binary(X).
binary_bg(P,X,Y) :- binary_bg(_,_,X), (P,Y) = @binary(X).

lstate(pos_ex,X) :- pos_ex(_,X,_).
rstate(pos_ex,Y) :- pos_ex(_,_,Y).
lstate(neg_ex,X) :- neg_ex(_,X,_).
rstate(neg_ex,Y) :- neg_ex(_,_,Y).

lstate(T,Y) :- lstate(T,X), binary_bg(_,X,Y).
rstate(T,X) :- rstate(T,Y), binary_bg(_,X,Y).

state(T,X) :- lstate(T,X), rstate(T,X).
state(T,X) :- lstate(T,X), functional.


% PREDICATE ORDER
order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

% METARULES
may_deduced(P,X,Y) :- state(pos_ex,X), state(pos_ex,Y), binary_bg(P,X,Y).
may_deduced(P1,X,Y) :- may_meta(precon,P1,P2,P3), unary_bg(P2,X), may_deduced(P3,X,Y).
may_deduced(P1,X,Y) :- may_meta(postcon,P1,P2,P3), may_deduced(P2,X,Y), unary_bg(P3,Y).
may_deduced(P1,X,Y) :- may_meta(chain,P1,P2,P3), may_deduced(P2,X,Z), may_deduced(P3,Z,Y).
may_deduced(P1,X,Y) :- may_meta(tailrec,P1,P2,n), may_deduced(P2,X,Z), may_deduced(P1,Z,Y).

% precon, postcon, chain, tailrec
may_meta(precon,P1,P2,P3) :- order(P1,P3), unary_bg(P2,X), may_deduced(P3,X,Y).
may_meta(postcon,P1,P2,P3) :- order(P1,P2), may_deduced(P2,X,Y), unary_bg(P3,Y).
may_meta(chain,P1,P2,P3) :- order(P1,P2), order(P1,P3), may_deduced(P2,X,Z), may_deduced(P3,Z,Y).
may_meta(tailrec,P1,P2,n) :- order(P1,P2), may_deduced(P2,X,Z), may_deduced(P1,Z,Y).

{ meta(ID,P1,P2,P3) } :- may_meta(ID,P1,P2,P3).
deduced(P,X,Y) :- state(_,X), state(_,Y), binary_bg(P,X,Y).
deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

% CONSTRAINTS
#external functional.
:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- not functional, neg_ex(P,X,Y), deduced(P,X,Y).
:-     functional, pos_ex(P,X,Y1), deduced(P,X,Y2), Y1 != Y2.
:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
