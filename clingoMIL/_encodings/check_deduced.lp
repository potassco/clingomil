
unary_bg(P,X) :- (P,X) = @unary().
binary_bg(P,X,Y) :- (P,X,Y) = @binary().
deduced(P,X,Y) :- binary_bg(P,X,Y).

meta(N,P1,P2,P3) :- (N,P1,P2,P3) = @meta().

deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

#show deduced/3.
