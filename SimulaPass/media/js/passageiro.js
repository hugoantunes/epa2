//MOVIMENTOS Q1
var tops = [0, 15, 290]
var rights = [0, 415, 838]

function movimenta($obj, top, right){
    if(right==0)
        $obj.animate({top:top});
    else if(top==0)
        $obj.animate({right:right});
    else
        $obj.animate({top:top,right:right});
}
//MOVIMENTOS DE Q1
function q1q3($obj){
    movimenta($obj, tops[1], rights[1]);
    movimenta($obj, tops[2], rights[1]);
    movimenta($obj, tops[2], rights[2]);
}

function q1q2($obj){
    movimenta($obj, tops[0], rights[2]);
}

function q1q4($obj){
    movimenta($obj, tops[2], rights[0]);
}
//FIM MOVIMENTOS DE Q1

//MOVIMENTOS DE Q2
function q2q4($obj){
    movimenta($obj, tops[1], rights[2]);
    movimenta($obj, tops[2], rights[2]);
    movimenta($obj, tops[1], rights[2]);
}

function q2q1($obj){
    movimenta($obj, tops[0], rights[1]);
}

function q2q3($obj){
    movimenta($obj, tops[2], rights[0]);
}
//FIM MOVIMENTOS Q2

//MOVIMENTOS Q3
function q3q1($obj){
    movimenta($obj, tops[2], rights[2]);
    movimenta($obj, tops[1], rights[2]);
    movimenta($obj, tops[1], rights[1]);
}

function q3q2($obj){
    movimenta($obj, tops[1], rights[0]);
}

function q3q4($obj){
    movimenta($obj, tops[0], rights[1]);
}
//FIM MOVIMENTOS Q3
//MOVIMENTOS Q4
function q4q2($obj){
    movimenta($obj, tops[2], rights[1]);
    movimenta($obj, tops[1], rights[1]);
    movimenta($obj, tops[1], rights[2]);
}

function q4q1($obj){
    movimenta($obj, tops[1], rights[0]);
}

function q4q3($obj){
    movimenta($obj, tops[0], rights[2]);
}
//FIM MOVIMENTOS Q4

