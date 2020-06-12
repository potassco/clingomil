
% #const size=X.
% #const skolems=Y. (does not make sense to be greater or equal to X)
skolem(1..skolems).

% BACKGROUND IMPORT
unary_bg(P,X) :- P = @unary(X), state(X).
binary_bg(P,X,Y) :- (P,Y) = @binary(X), state(X).

state(X) :- pos_ex(_,X,_).
state(X) :- neg_ex(_,X,_).
state(Y) :- deduced(_,_,Y).
deduced(P,X,Y) :- binary_bg(P,X,Y).

% PREDICATE ORDER
order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

% METARULES
% precon
{meta(precon,P1,P2,P3)} :- order(P1,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).

% postcon
{meta(postcon,P1,P2,P3)} :- order(P1,P2), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).

% chain
{meta(chain,P1,P2,P3)} :- order(P1,P2), order(P1,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
% deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
meta(chain,P2,P3,X,Y,Z) :- deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3),  meta(chain,P2,P3,X,Y,Z).

% tailrec
{meta(tailrec,P1,P2,n)} :- order(P1,P2), deduced(P2,X,Z), deduced(P1,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

% CONSTRAINTS
#external functional.
:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- not functional, neg_ex(P,X,Y),  deduced(P,X,Y).
:-     functional, pos_ex(P,X,Y1), deduced(P,X,Y2), Y1 != Y2.
:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
