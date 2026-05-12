import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    overflow: hidden;
    background: #222;
}

canvas {
    background: #333;
    display: block;
    margin: auto;
    border: 3px solid white;
}
</style>
</head>
<body>

<canvas id="game" width="1000" height="700"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const gravity = 0.7;

const platforms = [
    {x:0,y:650,w:1000,h:50},

    {x:150,y:520,w:250,h:20},
    {x:600,y:520,w:250,h:20},

    {x:350,y:390,w:300,h:20},

    {x:150,y:250,w:250,h:20},
    {x:600,y:250,w:250,h:20},
];

class Player {

    constructor(x,y,color,controls){
        this.x=x;
        this.y=y;
        this.w=50;
        this.h=60;
        this.color=color;

        this.dx=0;
        this.dy=0;

        this.score=0;

        this.controls=controls;

        this.onGround=false;
    }

    draw(){
        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);
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

        if(this.x < 0) this.x = 0;
        if(this.x + this.w > canvas.width)
            this.x = canvas.width - this.w;
    }
}

const keys = {};

document.addEventListener("keydown",(e)=>{
    keys[e.code]=true;
});

document.addEventListener("keyup",(e)=>{
    keys[e.code]=false;
});

const p1 = new Player(
    200,
    100,
    "red",
    {
        left:"KeyA",
        right:"KeyD",
        jump:"KeyW"
    }
);

const p2 = new Player(
    700,
    100,
    "blue",
    {
        left:"ArrowLeft",
        right:"ArrowRight",
        jump:"ArrowUp"
    }
);

function controls(player){

    player.dx = 0;

    if(keys[player.controls.left]){
        player.dx = -6;
    }

    if(keys[player.controls.right]){
        player.dx = 6;
    }

    if(keys[player.controls.jump] && player.onGround){
        player.dy = -14;
    }
}

function reset(){

    p1.x=200;
    p1.y=100;
    p1.dy=0;

    p2.x=700;
    p2.y=100;
    p2.dy=0;
}

let winner = null;

function collision(a,b){

    return (
        a.x < b.x+b.w &&
        a.x+a.w > b.x &&
        a.y < b.y+b.h &&
        a.y+a.h > b.y
    );
}

function gameLoop(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    controls(p1);
    controls(p2);

    p1.update();
    p2.update();

    // Plattformen
    ctx.fillStyle="lime";

    for(let p of platforms){
        ctx.fillRect(p.x,p.y,p.w,p.h);
    }

    // Kopf Treffer
    if(collision(p1,p2) && !winner){

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
        winner = "Spieler 1";
    }

    if(p2.score >= 3){
        winner = "Spieler 2";
    }

    p1.draw();
    p2.draw();

    // Score
    ctx.fillStyle="white";
    ctx.font="30px Arial";

    ctx.fillText(
        "Spieler 1: " + p1.score +
        "    Spieler 2: " + p2.score,
        280,
        40
    );

    if(winner){

        ctx.font="60px Arial";

        ctx.fillText(
            winner + " gewinnt!",
            250,
            300
        );
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=720)
