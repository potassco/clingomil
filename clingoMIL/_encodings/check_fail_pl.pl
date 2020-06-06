
% NOTE: we dont need state/1 as prolog does not ground
% foreign functions: import_unary, import_binary
% meta/4, pos_ex/3 and neg_ex/3 are asserted in _check_fail_pl.py

% In _check_fail_pl.py, import_unary and import_binary handle types of X and Y
% by themselves, but the distinction has to be made here such that the unified
% values are handled
unary_bg(P,X) :-
    current_predicate(imported_unary_bg/2),
    imported_unary_bg(P,X), !.
unary_bg(P,X) :-
    var(P),
    nonvar(X),
    import_unary(Ps,X),
    member(P,Ps),
    assertz(imported_unary_bg(P,X)).
unary_bg(P,X) :-
    nonvar(P),
    nonvar(X),
    import_unary(P,X),
    assertz(imported_unary_bg(P,X)).

binary_bg(P,X,Y) :-
    current_predicate(imported_binary_bg/3),
    imported_binary_bg(P,X,Y), !.
binary_bg(P,X,Y) :-
    var(P),
    nonvar(X),
    var(Y),
    import_binary(Ps,X,Ys),
    nth0(N,Ps,P),
    nth0(N,Ys,Y),
    assertz(imported_binary_bg(P,X,Y)).
binary_bg(P,X,Y) :-
    nonvar(P),
    nonvar(X),
    var(Y),
    import_binary(P,X,Ys),
    member(Y,Ys),
    assertz(imported_binary_bg(P,X,Y)).
binary_bg(P,X,Y) :-
    nonvar(P),
    nonvar(X),
    nonvar(Y),
    import_binary(P,X,Y),
    assertz(imported_binary_bg(P,X,Y)).

% deduced represented as actions.
% Successor states are predicates that need to be proved
deduced_by(deduced(P1,X,Y),[unary_bg(P2,X),deduced(P3,X,Y)]) :-
    meta(precon,P1,P2,P3).
deduced_by(deduced(P1,X,Y),[deduced(P2,X,Y),unary_bg(P3,Y)]) :-
    meta(postcon,P1,P2,P3).
deduced_by(deduced(P1,X,Y),[deduced(P2,X,Z),deduced(P3,Z,Y)]) :-
    meta(chain,P1,P2,P3).
deduced_by(deduced(P1,X,Y),[deduced(P2,X,Z),deduced(P1,Z,Y)]) :-
    meta(tailrec,P1,P2,n).

% Base cases
dfs(D) :- dfs([D], []).
dfs([],_).

% Remove preidcates that can be proven by bk
dfs([unary_bg(P,X)|Ds],Seen) :-
    unary_bg(P,X),
    dfs(Ds,Seen).
dfs([deduced(P,X,Y)|Ds],Seen) :-
    binary_bg(P,X,Y),
    dfs(Ds,Seen).

% Skip predicates that are already being proved
dfs([D|Ds],Seen) :-
    member(D,Seen),
    dfs(Ds,Seen).

% Expand predicates that cannot be proven by bk
dfs([D|Ds],Seen) :-
    not(member(D,Seen)),
    deduced_by(D,Succ),
    append(Succ,Ds,Next),
    dfs(Next,[D|Seen]).

% fail checks. fail_neg/0 for non-functional, fail_functional for funcitonal
% both can be cut as one negative example is enough to prove fail
fail_neg :-
    current_predicate(neg_ex/3),
    neg_ex(P,X,Y),
    dfs(deduced(P,X,Y)), !.

fail_functional :-
    pos_ex(P,X,Y1),
    dfs(deduced(P,X,Y2)),
    Y1 \= Y2, !.
