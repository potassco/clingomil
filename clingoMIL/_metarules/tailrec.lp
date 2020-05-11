#program substitution.
{meta(tailrec,P1,P2,n)} :- order(P1,P2), deduced(P2,X,Z), deduced(P1,Z,Y).

#program deduction.
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

#program string_substitution.
substitution_string(tailrec,"{P1}(X,Y) :- {P2}(X,Z), {P1}(Z,Y).").
