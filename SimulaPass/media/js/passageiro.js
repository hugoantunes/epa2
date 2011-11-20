//MOVIMENTOS Q1
var tops = [0, 15, 290]
var rights = [0, 15 , 415, 838]

function movimenta($obj, top, right, tempo){
    if(right==0)
        $obj.animate({top:top}, tempo);
    else if(top==0)
        $obj.animate({right:right}, tempo);
    else
        $obj.animate({top:top,right:right}, tempo);
}

//MOVIMENTOS DE Q1
function q1q3($obj){
    movimenta($obj, tops[1], rights[2], 5000);
    movimenta($obj, tops[2], rights[2]), 2000;
    movimenta($obj, tops[2], rights[3], 4000);
}

function q1q2($obj){
    movimenta($obj, tops[0], rights[3]);
}

function q1q4($obj){
    movimenta($obj, tops[2], rights[0]);
}
//FIM MOVIMENTOS DE Q1

//MOVIMENTOS DE Q2
function q2q4($obj){
    movimenta($obj, tops[0], rights[2]);
    movimenta($obj, tops[2], rights[0]);
    movimenta($obj, tops[0], rights[1]);
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
    movimenta($obj, tops[2], rights[3]);
    movimenta($obj, tops[1], rights[3]);
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
    movimenta($obj, tops[2], rights[2]);
    movimenta($obj, tops[1], rights[2]);
    movimenta($obj, tops[1], rights[3]);
}

function q4q1($obj){
    movimenta($obj, tops[1], rights[0]);
}

function q4q3($obj){
    movimenta($obj, tops[0], rights[3]);
}
//FIM MOVIMENTOS Q4


//OBJETO Transporte
function Transporte() { 
    this.id;
    this.tipo; 
    this.tempo;
    this.capacidade_maxima;
    this.capacidade_atual;
    this.capacidade_confortavel;
    this.conforto;
    this.posicao_inicial;
    this.posicao_final; 
    this.passageiros = new Array(); 
}


//OBJETO Passageiro
function Passageiro() { 
    this.tipo; 
    this.id;
    this.transporte;
    this.conforte;
    
    this.entra_no_transporte = function(transporte){ 
        this.transporte = transporte;
        transporte.passageiros.push(this);
    }

}

