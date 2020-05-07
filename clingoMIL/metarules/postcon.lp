#program substitution.
{meta(postcon,P1,P2,P3)} :- order(P1,P2), deduced(P2,X,Y), unary_bg(P3,Y).

#program deduction.
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).

#program string_substitution.
substitution_string(postcon,"{P1}(X,Y) :- {P2}(X,Y), {P3}(Y).").
