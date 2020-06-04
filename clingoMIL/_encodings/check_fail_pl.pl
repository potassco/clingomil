
% NOTE: we dont need state/1 as prolog does not ground
% foreign functions: import_unary, import_binary
% meta/4, pos_ex/3 and neg_ex/3 are asserted in _check_fail_pl.py

% import_unary and import_binary handle types of X and Y by themselves, but
% the distinction has to be made here such that the unified values are handled
unary_bg(P,X) :-
	var(P),
	nonvar(X),
	import_unary(Ps,X),
	member(P,Ps).

unary_bg(P,X) :-
	nonvar(P),
	nonvar(X),
	import_unary(P,X).

binary_bg(P,X,Y) :-
	var(P),
	nonvar(X),
	var(Y),
	import_binary(Ps,X,Ys),
	nth0(N,Ps,P),
	nth0(N,Ys,Y).

binary_bg(P,X,Y) :-
	nonvar(P),
	nonvar(X),
	var(Y),
	import_binary(P,X,Ys),
	member(Y,Ys).

binary_bg(P,X,Y) :-
	nonvar(P),
	nonvar(X),
	nonvar(Y),
	import_binary(P,X,Y).


% deduced very similar to asp implementation
deduced(P1,X,Y) :-
	meta(precon,P1,P2,P3),
	unary_bg(P2,X),
	deduced(P3,X,Y).

deduced(P1,X,Y) :-
	meta(postcon,P1,P2,P3),
	nonvar(X),
	deduced(P2,X,Y),
	unary_bg(P3,Y).

deduced(P1,X,Y) :-
	meta(chain,P1,P2,P3),
	deduced(P2,X,Z),
	deduced(P3,Z,Y).

deduced(P1,X,Y) :-
	meta(tailrec,P1,P2,n),
	deduced(P2,X,Z),
	deduced(P1,Z,Y).

deduced(P,X,Y) :-
	nonvar(X),
	binary_bg(P,X,Y).


% fail checks. fail_neg/0 for non-functional, fail_functional for funcitonal
% both can be cut as one negative example is enough to prove fail
fail_neg :-
	current_predicate(neg_ex/3),
	neg_ex(P,X,Y),
	deduced(P,X,Y), !.

fail_functional :-
	pos_ex(P,X,Y1),
	deduced(P,X,Y2),
	Y1 \= Y2, !.
