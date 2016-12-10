function action = defineAction(x,y,xNext,yNext)

if x==xNext && y==yNext
    action=1;
elseif xNext>x && yNext>y
    action=7;
elseif xNext>x && yNext==y
    action=3;
elseif xNext>x && yNext<y
    action=9;
elseif xNext==x && yNext>y
    action=2;
elseif xNext==x && yNext<y
    action=4;
elseif xNext<x && yNext>y
    action=6;
elseif xNext<x && yNext==y
    action=5;
elseif xNext<x && yNext<y
    action=8;
else
    display('Error in action attribution');
end

end