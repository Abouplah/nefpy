<!--//Michel DEBOOM 06/2005
gk=window.Event?1:0; // navigateurs Gecko ou IE
D=document;popup=popn=encours=wpop=hpop=x=0
dy=10;dx=5

function ctrl(e)
{
if(!x){de=!D.documentElement.clientWidth?D.body:D.documentElement;x=1} // IE6
el=gk?e.target:event.srcElement; //objet sous la souris
if(!el.tagName)el=el.parentNode; // noeud #text
if(el.className == 'pop')
  {
  popup = D.getElementById(el.href.substring(el.href.lastIndexOf('#') + 1)); 
  with(popup){wpop=offsetWidth;hpop=offsetHeight}
  if(popup.style!=encours) // seulement si changement de bulle
    {
    encours.left=-999+'px';
    encours=popup.style;
    fx=gk?innerWidth-15:de.clientWidth   //l fenêtre
    fy=gk?innerHeight-15:de.clientHeight //h fenêtre
    sx=gk?pageXOffset:de.scrollLeft      //scroll h
    sy=gk?pageYOffset:de.scrollTop       //scroll v
    x=gk?e.pageX:event.clientX+sx;       //curseur x
    y=gk?e.pageY:event.clientY+sy;       //curseur y
    posx=535;//posx=x>=(fx-wpop-dx)?(x-wpop-2*dx):x+dx;
    posy=170;//posy=y>=(fy-hpop-dy)?(y-hpop-2*dy):y+dy;
    with(popup.style){left=posx+dx+'px';top=posy+dy+'px';}
    el.onclick=function(){return false}//désactive le lien
    }
  } else {encours.left=-999+'px';encours=0}//else {encours.left=-999+'px';encours=0}
}

D.onclick=ctrl //D.onmousemove=ctrl
// charge la feuille de style des popups.
//D.write('<style type="text/css">@import url(bull.css);</style>')
//-->
