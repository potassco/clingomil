#program substitution.
{meta(chain,P1,P2,P3)} :- order(P1,P2), order(P1,P3), deduced(P2,X,Z), deduced(P3,Z,Y).

#program deduction.
% deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
meta(chain,P2,P3,X,Y,Z) :- deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3),  meta(chain,P2,P3,X,Y,Z).

#program string_substitution.
substitution_string(chain,"{P1}(X,Y) :- {P2}(X,Z), {P3}(Z,Y).").
