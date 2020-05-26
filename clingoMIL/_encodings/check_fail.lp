
unary_bg(P,X) :- P = @unary(X), state(X).
binary_bg(P,X,Y) :- (P,Y) = @binary(X), state(X).

deduced(P,X,Y) :- binary_bg(P,X,Y).
deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

state(X) :- pos_ex(_,X,_).
state(X) :- neg_ex(_,X,_).
state(Y) :- deduced(_,_,Y).

#external functional.
fail :- not functional, neg_ex(P,X,Y), deduced(P,X,Y).
fail :-     functional, pos_ex(P,X,Y1), deduced(P,X,Y2), Y1 != Y2.

#show.
#show fail/0.
