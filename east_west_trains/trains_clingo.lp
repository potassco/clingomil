% Replacement: (.*?)&contains\[(.),"(.*?)"\].* by \n#external contains(\2,"\3") : state(\2).\n\1contains(\2,"\3"), state(\2).

#const size=0.
#const skolems=0.
skolem(1..skolems).

binary_bg(remove_car,X,Y) :- Y = @removeFirst(X), state(X).

#external contains(X,",rectangle") : state(X).
unary_bg(shp_rect,X) :- contains(X,",rectangle"), state(X).

#external contains(X,",u_shaped") : state(X).
unary_bg(shp_u,X) :- contains(X,",u_shaped"), state(X).

#external contains(X,",ellipse") : state(X).
unary_bg(shp_ellip,X) :- contains(X,",ellipse"), state(X).

#external contains(X,",hexagon") : state(X).
unary_bg(shp_hex,X) :- contains(X,",hexagon"), state(X).

#external contains(X,",bucket") : state(X).
unary_bg(shp_buck,X) :- contains(X,",bucket"), state(X).


#external contains(X,"short") : state(X).
unary_bg(leng_short,X) :- contains(X,"short"), state(X).

#external contains(X,"long") : state(X).
unary_bg(leng_long,X) :- contains(X,"long"), state(X).


#external contains(X,"double") : state(X).
unary_bg(doub,X) :- contains(X,"double"), state(X).

#external contains(X,"not_double") : state(X).
unary_bg(doub_n,X) :- contains(X,"not_double"), state(X).


#external contains(X,"none") : state(X).
unary_bg(roof_non,X) :- contains(X,"none"), state(X).

#external contains(X,"flat") : state(X).
unary_bg(roof_flat,X) :- contains(X,"flat"), state(X).

#external contains(X,"jagged") : state(X).
unary_bg(roof_jag,X) :- contains(X,"jagged"), state(X).

#external contains(X,"peaked") : state(X).
unary_bg(roof_peak,X) :- contains(X,"peaked"), state(X).

#external contains(X,"arc") : state(X).
unary_bg(roof_arc,X) :- contains(X,"arc"), state(X).


#external contains(X,"flat") : state(X).
unary_bg(roof_clos,X) :- contains(X,"flat"), state(X).

#external contains(X,"jagged") : state(X).
unary_bg(roof_clos,X) :- contains(X,"jagged"), state(X).

#external contains(X,"peaked") : state(X).
unary_bg(roof_clos,X) :- contains(X,"peaked"), state(X).

#external contains(X,"arc") : state(X).
unary_bg(roof_clos,X) :- contains(X,"arc"), state(X).


#external contains(X,"l.circle") : state(X).
unary_bg(load_circ,X) :- contains(X,"l.circle"), state(X).

#external contains(X,"l.diamond") : state(X).
unary_bg(load_dia,X) :- contains(X,"l.diamond"), state(X).

#external contains(X,"l.hexagon") : state(X).
unary_bg(load_hex,X) :- contains(X,"l.hexagon"), state(X).

#external contains(X,"l.rectangle") : state(X).
unary_bg(load_rect,X) :- contains(X,"l.rectangle"), state(X).

#external contains(X,"l.triangle") : state(X).
unary_bg(load_tri,X) :- contains(X,"l.triangle"), state(X).

#external contains(X,"l.utriangle") : state(X).
unary_bg(load_utri,X) :- contains(X,"l.utriangle"), state(X).


#external contains(X,"circle,0") : state(X).
unary_bg(load0_circ,X) :- contains(X,"circle,0"), state(X).

#external contains(X,"diamond,0") : state(X).
unary_bg(load0_dia,X) :- contains(X,"diamond,0"), state(X).

#external contains(X,"hexagon,0") : state(X).
unary_bg(load0_hex,X) :- contains(X,"hexagon,0"), state(X).

#external contains(X,"rectangle,0") : state(X).
unary_bg(load0_rect,X) :- contains(X,"rectangle,0"), state(X).

#external contains(X,"triangle,0") : state(X).
unary_bg(load0_tri,X) :- contains(X,"triangle,0"), state(X).

#external contains(X,"utriangle,0") : state(X).
unary_bg(load0_utri,X) :- contains(X,"utriangle,0"), state(X).


#external contains(X,"circle,1") : state(X).
unary_bg(load1_circ,X) :- contains(X,"circle,1"), state(X).

#external contains(X,"diamond,1") : state(X).
unary_bg(load1_dia,X) :- contains(X,"diamond,1"), state(X).

#external contains(X,"hexagon,1") : state(X).
unary_bg(load1_hex,X) :- contains(X,"hexagon,1"), state(X).

#external contains(X,"rectangle,1") : state(X).
unary_bg(load1_rect,X) :- contains(X,"rectangle,1"), state(X).

#external contains(X,"triangle,1") : state(X).
unary_bg(load1_tri,X) :- contains(X,"triangle,1"), state(X).

#external contains(X,"utriangle,1") : state(X).
unary_bg(load1_utri,X) :- contains(X,"utriangle,1"), state(X).


#external contains(X,"circle,2") : state(X).
unary_bg(load2_circ,X) :- contains(X,"circle,2"), state(X).

#external contains(X,"diamond,2") : state(X).
unary_bg(load2_dia,X) :- contains(X,"diamond,2"), state(X).

#external contains(X,"hexagon,2") : state(X).
unary_bg(load2_hex,X) :- contains(X,"hexagon,2"), state(X).

#external contains(X,"rectangle,2") : state(X).
unary_bg(load2_rect,X) :- contains(X,"rectangle,2"), state(X).

#external contains(X,"triangle,2") : state(X).
unary_bg(load2_tri,X) :- contains(X,"triangle,2"), state(X).

#external contains(X,"utriangle,2") : state(X).
unary_bg(load2_utri,X) :- contains(X,"utriangle,2"), state(X).


#external contains(X,"circle,3") : state(X).
unary_bg(load3_circ,X) :- contains(X,"circle,3"), state(X).

#external contains(X,"diamond,3") : state(X).
unary_bg(load3_dia,X) :- contains(X,"diamond,3"), state(X).

#external contains(X,"hexagon,3") : state(X).
unary_bg(load3_hex,X) :- contains(X,"hexagon,3"), state(X).

#external contains(X,"rectangle,3") : state(X).
unary_bg(load3_rect,X) :- contains(X,"rectangle,3"), state(X).

#external contains(X,"triangle,3") : state(X).
unary_bg(load3_tri,X) :- contains(X,"triangle,3"), state(X).

#external contains(X,"utriangle,3") : state(X).
unary_bg(load3_utri,X) :- contains(X,"utriangle,3"), state(X).


#external contains(X,",2,") : state(X).
unary_bg(wheel_2,X) :- contains(X,",2,"), state(X).

#external contains(X,",3,") : state(X).
unary_bg(wheel_3,X) :- contains(X,",3,"), state(X).

order(X,Y) :- skolem(X), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), binary_bg(Y,_,_).
order(X,Y) :- pos_ex(X,_,_), skolem(Y).
order(X,Y) :- skolem(X), skolem(Y), X < Y.

{meta(precon,P1,P2,P3)} :- order(P1,P3), unary_bg(P2,X), deduced(P3,X,Y).
{meta(postcon,P1,P2,P3)} :- order(P1,P2), deduced(P2,X,Y), unary_bg(P3,Y).
{meta(chain,P1,P2,P3)} :- order(P1,P2), order(P1,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
{meta(tailrec,P1,P2,n)} :- order(P1,P2), deduced(P2,X,Z), deduced(P1,Z,Y).

deduced(P1,X,Y) :- meta(precon,P1,P2,P3), unary_bg(P2,X), deduced(P3,X,Y).
deduced(P1,X,Y) :- meta(postcon,P1,P2,P3), deduced(P2,X,Y), unary_bg(P3,Y).
deduced(P1,X,Y) :- meta(chain,P1,P2,P3), deduced(P2,X,Z), deduced(P3,Z,Y).
deduced(P1,X,Y) :- meta(tailrec,P1,P2,n), deduced(P2,X,Z), deduced(P1,Z,Y).

state(X) :- pos_ex(_,X,_).
state(X) :- neg_ex(_,X,_).

state(Y) :- deduced(_,_,Y).
deduced(P,X,Y) :- binary_bg(P,X,Y).

:- pos_ex(P,X,Y), not deduced(P,X,Y).
:- neg_ex(P,X,Y), deduced(P,X,Y).


:- #count{ M,P1,P2,P3 : meta(M,P1,P2,P3) } != size.


