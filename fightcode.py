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
    font-family:Arial, sans-serif;
    background:#0b1020;
}

canvas{
    display:block;
    width:100vw;
    height:100vh;
}

/* ---------------- MENU ---------------- */

#menu{

    position:absolute;

    width:100%;
    height:100vh;

    display:flex;

    justify-content:center;
    align-items:center;

    background:rgba(5,10,25,0.85);

    z-index:10;
}

.menu-box{

    width:min(90vw,550px);

    background:rgba(20,30,55,0.95);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:28px;

    padding:40px;

    text-align:center;

    box-shadow:0 0 50px rgba(0,0,0,0.5);

    backdrop-filter:blur(10px);
}

.menu-box h1{

    color:#f8fafc;

    font-size:56px;

    margin-bottom:12px;
}

.subtitle{

    color:#94a3b8;

    margin-bottom:28px;

    font-size:18px;
}

.input-label{

    color:#cbd5e1;

    text-align:left;

    margin-top:16px;

    margin-bottom:8px;

    font-size:16px;

    font-weight:bold;
}

.menu-box input{

    width:100%;

    padding:16px;

    border:none;

    border-radius:14px;

    background:#24324d;

    color:white;

    font-size:18px;

    outline:none;

    border:2px solid transparent;
}

.menu-box input:focus{

    border:2px solid #60a5fa;
}

.menu-box button{

    width:100%;

    margin-top:28px;

    padding:18px;

    border:none;

    border-radius:16px;

    font-size:22px;

    font-weight:bold;

    color:white;

    cursor:pointer;

    background:linear-gradient(to right,#2563eb,#38bdf8);

    transition:0.2s;
}

.menu-box button:hover{

    transform:scale(1.03);
}

.controls{

    margin-top:22px;

    color:#cbd5e1;

    line-height:2;

    font-size:17px;
}

</style>
</head>

<body>

<div id="menu">

    <div class="menu-box">

        <h1>🌙 Jump Battle</h1>

        <div class="subtitle">
            Gib eure Namen ein und startet das Duell
        </div>

        <div class="input-label">
            Spieler 1 Name
        </div>

        <input
            id="p1name"
            type="text"
            placeholder="z.B. Max"
            value=""
        >

        <div class="input-label">
            Spieler 2 Name
        </div>

        <input
            id="p2name"
            type="text"
            placeholder="z.B. Leon"
            value=""
        >

        <div class="controls">

            <div>🔴 Spieler 1 → WASD</div>
            <div>🔵 Spieler 2 → Pfeiltasten</div>
            <div>👑 Auf den Kopf springen = Punkt</div>
            <div>🏆 Erster bis 3 gewinnt</div>

        </div>

        <button onclick="startGame()">
            Spiel starten
        </button>

    </div>

</div>

<canvas id="game"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resizeCanvas(){

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();

window.addEventListener("resize", resizeCanvas);

const gravity = 0.8;

let gameStarted = false;
let winner = null;

/* ---------------- STARS ---------------- */

const stars = [];

for(let i=0;i<150;i++){

    stars.push({

        x:Math.random()*window.innerWidth,
        y:Math.random()*window.innerHeight,
        r:Math.random()*2
    });
}

/* ---------------- PLATFORMS ---------------- */

function getPlatforms(){

    return [

        {
            x:0,
            y:canvas.height-45,
            w:canvas.width,
            h:45
        },

        {
            x:150,
            y:canvas.height-220,
            w:340,
            h:24
        },

        {
            x:canvas.width-490,
            y:canvas.height-220,
            w:340,
            h:24
        },

        {
            x:canvas.width/2-170,
            y:canvas.height-380,
            w:340,
            h:24
        },

        {
            x:120,
            y:canvas.height-540,
            w:280,
            h:24
        },

        {
            x:canvas.width-400,
            y:canvas.height-540,
            w:280,
            h:24
        }
    ];
}

/* ---------------- PLAYER ---------------- */

class Player{

    constructor(x,y,color,controls){

        this.x=x;
        this.y=y;

        this.w=70;
        this.h=100;

        this.color=color;

        this.dx=0;
        this.dy=0;

        this.score=0;

        this.controls=controls;

        this.onGround=false;

        this.name="Spieler";
    }

    draw(){

        // Kopf
        ctx.fillStyle="#f1c27d";

        ctx.beginPath();

        ctx.arc(
            this.x + this.w/2,
            this.y + 20,
            18,
            0,
            Math.PI*2
        );

        ctx.fill();

        // Körper
        ctx.fillStyle=this.color;

        ctx.fillRect(
            this.x + 15,
            this.y + 40,
            40,
            40
        );

        // Beine
        ctx.fillRect(
            this.x + 18,
            this.y + 80,
            12,
            20
        );

        ctx.fillRect(
            this.x + 40,
            this.y + 80,
            12,
            20
        );

        // Arme
        ctx.fillRect(
            this.x + 2,
            this.y + 45,
            12,
            10
        );

        ctx.fillRect(
            this.x + 56,
            this.y + 45,
            12,
            10
        );
    }

    update(){

        this.dy += gravity;

        this.x += this.dx;
        this.y += this.dy;

        this.onGround = false;

        const platforms = getPlatforms();

        for(let p of platforms){

            const touching =

                this.x < p.x+p.w &&
                this.x+this.w > p.x &&
                this.y < p.y+p.h &&
                this.y+this.h > p.y;

            if(touching){

                // OBEN landen
                if(
                    this.dy > 0 &&
                    this.y + this.h - this.dy <= p.y
                ){

                    this.y = p.y - this.h;

                    this.dy = 0;

                    this.onGround = true;
                }

                // UNTEN blockieren
                else if(
                    this.dy < 0 &&
                    this.y >= p.y + p.h - 5
                ){

                    this.y = p.y + p.h;

                    this.dy = 0;
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

/* ---------------- CONTROLS ---------------- */

const keys = {};

window.addEventListener("keydown",(e)=>{

    keys[e.code] = true;
});

window.addEventListener("keyup",(e)=>{

    keys[e.code] = false;
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

function controls(player){

    player.dx = 0;

    if(keys[player.controls.left]){

        player.dx = -8;
    }

    if(keys[player.controls.right]){

        player.dx = 8;
    }

    if(keys[player.controls.jump] && player.onGround){

        player.dy = -17;
    }
}

/* ---------------- GAME ---------------- */

function startGame(){

    p1.name =
        document.getElementById("p1name").value
        || "Rot";

    p2.name =
        document.getElementById("p2name").value
        || "Blau";

    document.getElementById("menu").style.display =
        "none";

    gameStarted = true;
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

    p1.x = 200;
    p1.y = canvas.height-300;
    p1.dy = 0;

    p2.x = canvas.width-300;
    p2.y = canvas.height-300;
    p2.dy = 0;
}

/* ---------------- DRAW ---------------- */

function drawBackground(){

    const grad =
        ctx.createLinearGradient(0,0,0,canvas.height);

    grad.addColorStop(0,"#0b1020");
    grad.addColorStop(1,"#111827");

    ctx.fillStyle = grad;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Sterne

    ctx.fillStyle = "white";

    for(let s of stars){

        ctx.beginPath();

        ctx.arc(s.x,s.y,s.r,0,Math.PI*2);

        ctx.fill();
    }

    // Mond

    ctx.fillStyle = "#f8fafc";

    ctx.beginPath();

    ctx.arc(
        canvas.width-180,
        120,
        60,
        0,
        Math.PI*2
    );

    ctx.fill();
}

function drawPlatforms(){

    const platforms = getPlatforms();

    for(let p of platforms){

        ctx.fillStyle = "#334155";

        ctx.fillRect(
            p.x,
            p.y,
            p.w,
            p.h
        );

        ctx.fillStyle = "#64748b";

        ctx.fillRect(
            p.x,
            p.y,
            p.w,
            5
        );
    }
}

function drawScores(){

    ctx.fillStyle = "white";

    ctx.font = "bold 30px Arial";

    ctx.fillText(

        p1.name + ": " + p1.score,

        40,

        50
    );

    const rightText =
        p2.name + ": " + p2.score;

    const width =
        ctx.measureText(rightText).width;

    ctx.fillText(

        rightText,

        canvas.width - width - 40,

        50
    );
}

function drawWinner(){

    ctx.fillStyle = "white";

    ctx.font = "bold 70px Arial";

    const text =
        winner + " gewinnt!";

    const width =
        ctx.measureText(text).width;

    ctx.fillText(

        text,

        canvas.width/2 - width/2,

        canvas.height/2
    );
}

/* ---------------- LOOP ---------------- */

function gameLoop(){

    drawBackground();

    if(gameStarted && !winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        if(collision(p1,p2)){

            if(
                p1.dy > 0 &&
                p1.y < p2.y
            ){

                p1.score++;

                reset();
            }

            else if(
                p2.dy > 0 &&
                p2.y < p1.y
            ){

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

components.html(html_code, height=1200)
