#program substitution.
{meta(precon,P1,P2,P3)} :- order(P1,P3), unary_bg(P2,X), deduced(P3,X,Y).

#program deduction.
deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).

#program string_substitution.
substitution_string(precon,"{P1}(X,Y) :- {P2}(X), {P3}(X,Y).").
