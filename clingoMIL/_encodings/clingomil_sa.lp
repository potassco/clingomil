
% #const size=0.
% #const skolems=0.
skolem(1..skolems).

% BACKGROUND IMPORT
unary_bg(A,N) :- (A,N) = @unary().
binary_bg(A,N1,N2) :- (A,N1,N2) = @binary().
deduced(P,X,Y) :- binary_bg(P,X,Y).

% PREDICATE ORDER
order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos(_,X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos(_,X,_,_), skolem(Y).
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
% note that the check for negative examples is done externally (by adding nogoods
% consisting of the assigned metas if they entail negative examples)

% selection of bk to use for deducing positive examples
{ pos(ID,X,Y,Z) } :- (ID,X,Y,Z) = @checkpos().
:- pos_ex(ID,_,_,_), not pos(ID,_,_,_).
:- pos(_,X,Y,Z), not deduced(X,Y,Z).

:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.
