# app.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    font-family:Arial;
    background:#0f172a;
}

#menu{
    position:absolute;
    width:100%;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    background:rgba(0,0,0,0.8);

    z-index:10;
}

.menu-box{

    width:420px;

    background:#1e293b;

    padding:40px;

    border-radius:25px;

    text-align:center;

    box-shadow:0 0 40px rgba(0,0,0,0.5);
}

.menu-box h1{

    color:white;

    font-size:48px;

    margin-bottom:25px;
}

.menu-box input{

    width:100%;

    padding:15px;

    margin-top:15px;

    border:none;

    border-radius:12px;

    background:#334155;

    color:white;

    font-size:18px;
}

.menu-box button{

    width:100%;

    margin-top:25px;

    padding:15px;

    border:none;

    border-radius:12px;

    font-size:22px;

    color:white;

    cursor:pointer;

    background:linear-gradient(to right,#3b82f6,#06b6d4);

    transition:0.2s;
}

.menu-box button:hover{
    transform:scale(1.03);
}

.controls{

    margin-top:20px;

    color:#cbd5e1;

    line-height:1.8;
}

canvas{
    display:block;
}

</style>
</head>

<body>

<div id="menu">

    <div class="menu-box">

        <h1>Jump Battle</h1>

        <input id="p1name" placeholder="Name Spieler 1" value="Rot">
        <input id="p2name" placeholder="Name Spieler 2" value="Blau">

        <div class="controls">

            <p><b>Spieler 1:</b> WASD</p>
            <p><b>Spieler 2:</b> Pfeiltasten</p>
            <p>Springe auf den Kopf des Gegners!</p>
            <p>Erster bis 3 Punkte gewinnt.</p>

        </div>

        <button onclick="startGame()">Spiel starten</button>

    </div>

</div>

<canvas id="game"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener("resize",()=>{

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

});

const gravity = 0.7;

let gameStarted = false;
let winner = null;

const platforms = [

    {
        x:0,
        y:canvas.height-40,
        w:canvas.width,
        h:40
    },

    {
        x:150,
        y:canvas.height-180,
        w:320,
        h:20
    },

    {
        x:canvas.width-470,
        y:canvas.height-180,
        w:320,
        h:20
    },

    {
        x:canvas.width/2-170,
        y:canvas.height-330,
        w:340,
        h:20
    },

    {
        x:100,
        y:canvas.height-480,
        w:280,
        h:20
    },

    {
        x:canvas.width-380,
        y:canvas.height-480,
        w:280,
        h:20
    }

];

class Player{

    constructor(x,y,color,controls){

        this.x=x;
        this.y=y;

        this.w=70;
        this.h=90;

        this.color=color;

        this.dx=0;
        this.dy=0;

        this.score=0;

        this.controls=controls;

        this.onGround=false;

        this.name="Spieler";
    }

    draw(){

        ctx.fillStyle=this.color;

        ctx.shadowColor=this.color;
        ctx.shadowBlur=20;

        ctx.fillRect(this.x,this.y,this.w,this.h);

        ctx.shadowBlur=0;
    }

    update(){

        this.dy += gravity;

        this.x += this.dx;
        this.y += this.dy;

        this.onGround=false;

        for(let p of platforms){

            if(

                this.x < p.x+p.w &&
                this.x+this.w > p.x &&
                this.y < p.y+p.h &&
                this.y+this.h > p.y

            ){

                if(this.dy > 0){

                    this.y = p.y - this.h;

                    this.dy = 0;

                    this.onGround=true;
                }
            }
        }

        if(this.x < 0){
            this.x = 0;
        }

        if(this.x + this.w > canvas.width){

            this.x = canvas.width - this.w;
        }
    }
}

const keys = {};

window.addEventListener("keydown",(e)=>{

    keys[e.code]=true;

});

window.addEventListener("keyup",(e)=>{

    keys[e.code]=false;

});

const p1 = new Player(

    200,
    canvas.height-300,

    "#ef4444",

    {
        left:"KeyA",
        right:"KeyD",
        jump:"KeyW"
    }
);

const p2 = new Player(

    canvas.width-300,
    canvas.height-300,

    "#3b82f6",

    {
        left:"ArrowLeft",
        right:"ArrowRight",
        jump:"ArrowUp"
    }
);

function startGame(){

    const name1 =
        document.getElementById("p1name").value;

    const name2 =
        document.getElementById("p2name").value;

    p1.name = name1 || "Rot";
    p2.name = name2 || "Blau";

    document.getElementById("menu").style.display="none";

    gameStarted=true;
}

function controls(player){

    player.dx=0;

    if(keys[player.controls.left]){

        player.dx=-8;
    }

    if(keys[player.controls.right]){

        player.dx=8;
    }

    if(keys[player.controls.jump] && player.onGround){

        player.dy=-16;
    }
}

function collision(a,b){

    return(

        a.x < b.x+b.w &&
        a.x+a.w > b.x &&
        a.y < b.y+b.h &&
        a.y+a.h > b.y

    );
}

function reset(){

    p1.x=200;
    p1.y=canvas.height-300;
    p1.dy=0;

    p2.x=canvas.width-300;
    p2.y=canvas.height-300;
    p2.dy=0;
}

function drawBackground(){

    const grad =
        ctx.createLinearGradient(0,0,0,canvas.height);

    grad.addColorStop(0,"#0f172a");
    grad.addColorStop(1,"#1e293b");

    ctx.fillStyle=grad;

    ctx.fillRect(0,0,canvas.width,canvas.height);
}

function drawPlatforms(){

    for(let p of platforms){

        ctx.fillStyle="#22c55e";

        ctx.shadowColor="#22c55e";
        ctx.shadowBlur=20;

        ctx.fillRect(p.x,p.y,p.w,p.h);

        ctx.shadowBlur=0;
    }
}

function drawScores(){

    ctx.fillStyle="white";

    ctx.font="bold 32px Arial";

    ctx.fillText(

        p1.name + ": " + p1.score,

        50,

        50
    );

    ctx.fillText(

        p2.name + ": " + p2.score,

        canvas.width-250,

        50
    );
}

function drawWinner(){

    ctx.fillStyle="white";

    ctx.font="bold 72px Arial";

    const text = winner + " gewinnt!";

    const textWidth =
        ctx.measureText(text).width;

    ctx.fillText(

        text,

        canvas.width/2 - textWidth/2,

        canvas.height/2
    );
}

function gameLoop(){

    drawBackground();

    if(gameStarted && !winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        if(collision(p1,p2)){

            if(p1.dy > 0 && p1.y < p2.y){

                p1.score++;

                reset();
            }

            else if(p2.dy > 0 && p2.y < p1.y){

                p2.score++;

                reset();
            }
        }

        if(p1.score >= 3){

            winner = p1.name;
        }

        if(p2.score >= 3){

            winner = p2.name;
        }
    }

    drawPlatforms();

    p1.draw();
    p2.draw();

    drawScores();

    if(winner){

        drawWinner();
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=1080)
