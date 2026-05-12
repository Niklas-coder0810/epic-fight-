import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

/* =========================================================
   RESET + BASE
========================================================= */

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    background:#070b18;
    font-family:Arial;
}

/* =========================================================
   CANVAS (IMPORTANT: SMALLER GAME VIEW, NOT FULL STRETCH)
========================================================= */

canvas{
    display:block;
    margin:auto;

    /* smaller but visible game frame */
    width:95vw;
    height:85vh;

    border:2px solid rgba(255,255,255,0.08);
    border-radius:18px;
}

/* =========================================================
   MENU
========================================================= */

#menu{
    position:absolute;
    width:100%;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    background:rgba(0,0,0,0.75);

    z-index:100;
}

.menu-box{
    width:420px;
    background:#111c33;
    padding:35px;
    border-radius:20px;
    text-align:center;
    color:white;
}

.menu-box h1{
    font-size:48px;
    margin-bottom:10px;
}

.menu-box input{
    width:100%;
    padding:12px;
    margin-top:12px;

    border-radius:10px;
    border:none;

    background:#24324d;
    color:white;
    font-size:16px;
}

.menu-box button{
    width:100%;
    margin-top:20px;
    padding:14px;

    border:none;
    border-radius:12px;

    background:linear-gradient(to right,#2563eb,#38bdf8);

    color:white;
    font-size:18px;
    font-weight:bold;
}

/* =========================================================
   POPUP
========================================================= */

#popup{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    font-size:50px;
    color:white;

    display:none;

    z-index:200;
}

/* =========================================================
   HUD
========================================================= */

#hud{
    position:absolute;
    top:10px;
    width:100%;

    display:flex;
    justify-content:space-between;

    padding:0 40px;

    color:white;
    font-size:20px;
    font-weight:bold;
}

/* =========================================================
   BACKGROUND DECOR (NOT CANVAS, JUST STYLE NOTES)
========================================================= */

</style>

</head>

<body>

<!-- ================= MENU ================= -->

<div id="menu">
    <div class="menu-box">

        <h1>🌙 Jump Battle</h1>

        <input id="p1name" placeholder="Spieler 1 (WASD)">
        <input id="p2name" placeholder="Spieler 2 (Pfeile)">

        <button onclick="startGame()">Start</button>

    </div>
</div>

<div id="popup"></div>

<div id="hud"></div>

<canvas id="game"></canvas>

<script>

/* =========================================================
   CANVAS SETUP
========================================================= */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize(){
    canvas.width = 1200;
    canvas.height = 650;
}
resize();

/* =========================================================
   GAME STATE
========================================================= */

let gameStarted = false;
let winner = null;

/* =========================================================
   PHYSICS
========================================================= */

const gravity = 0.8;

/* =========================================================
   STAR BACKGROUND
========================================================= */

const stars = [];

for(let i=0;i<180;i++){
    stars.push({
        x:Math.random()*1200,
        y:Math.random()*650,
        r:Math.random()*2
    });
}

/* =========================================================
   COINS SYSTEM
========================================================= */

let coins = [];

function spawnCoin(){
    coins.push({
        x:Math.random()*1100+50,
        y:Math.random()*300
    });
}

setInterval(()=>{
    if(gameStarted && !winner){
        if(Math.random()<0.6) spawnCoin();
    }
},3500);

/* =========================================================
   BOOST SYSTEM
========================================================= */

let boost = {
    p1:0,
    p2:0
};

/* =========================================================
   PLATFORM SYSTEM (FIXED + RELIABLE)
========================================================= */

function platforms(){
    return [
        {x:0,y:600,w:1200,h:50},

        {x:150,y:470,w:300,h:20},
        {x:750,y:470,w:300,h:20},

        {x:450,y:340,w:300,h:20},

        {x:200,y:220,w:250,h:20},
        {x:750,y:220,w:250,h:20}
    ];
}

/* =========================================================
   PLAYER CLASS (IMPROVED LOOK)
========================================================= */

class Player{

    constructor(x,y,color,controls){
        this.x=x;
        this.y=y;
        this.w=50;
        this.h=80;

        this.color=color;

        this.dx=0;
        this.dy=0;

        this.score=0;

        this.controls=controls;

        this.onGround=false;

        this.name="";
    }

    draw(){

        // body
        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);

        // head
        ctx.fillStyle="#f1c27d";
        ctx.beginPath();
        ctx.arc(this.x+25,this.y-10,12,0,Math.PI*2);
        ctx.fill();
    }

    update(){

        this.dy += gravity;

        this.x += this.dx;
        this.y += this.dy;

        this.onGround=false;

        for(let p of platforms()){

            const hit =
                this.x < p.x+p.w &&
                this.x+this.w > p.x &&
                this.y < p.y+p.h &&
                this.y+this.h > p.y;

            if(hit){

                // landing fix (IMPORTANT)
                if(this.dy > 0 && this.y+this.h-this.dy <= p.y){
                    this.y = p.y - this.h;
                    this.dy = 0;
                    this.onGround = true;
                }
            }
        }

        if(this.x<0) this.x=0;
        if(this.x+this.w>1200) this.x=1200-this.w;
    }
}

/* =========================================================
   INPUT
========================================================= */

const keys={};

window.addEventListener("keydown",e=>keys[e.code]=true);
window.addEventListener("keyup",e=>keys[e.code]=false);

/* =========================================================
   PLAYERS
========================================================= */

const p1 = new Player(200,100,"#ef4444",{l:"KeyA",r:"KeyD",j:"KeyW"});
const p2 = new Player(800,100,"#3b82f6",{l:"ArrowLeft",r:"ArrowRight",j:"ArrowUp"});

p1.id="p1";
p2.id="p2";

/* =========================================================
   CONTROLS
========================================================= */

function controls(p){

    p.dx=0;

    let sp = (boost[p.id]>0)?11:7;

    if(keys[p.controls.l]) p.dx=-sp;
    if(keys[p.controls.r]) p.dx=sp;

    if(keys[p.controls.j] && p.onGround){
        p.dy=-15;
    }
}

/* =========================================================
   START GAME
========================================================= */

function startGame(){

    p1.name=document.getElementById("p1name").value||"P1";
    p2.name=document.getElementById("p2name").value||"P2";

    document.getElementById("menu").style.display="none";

    gameStarted=true;
}

/* =========================================================
   RESET POS
========================================================= */

function reset(){
    p1.x=200;p1.y=100;p1.dy=0;
    p2.x=800;p2.y=100;p2.dy=0;
}

/* =========================================================
   COLLISION
========================================================= */

function collide(a,b){
    return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
}

/* =========================================================
   COINS
========================================================= */

function drawCoins(){

    ctx.fillStyle="gold";

    for(let c of coins){

        ctx.beginPath();
        ctx.arc(c.x,c.y,8,0,Math.PI*2);
        ctx.fill();
    }
}

function checkCoins(p){

    coins=coins.filter(c=>{

        let hit =
            p.x < c.x+10 &&
            p.x+p.w > c.x &&
            p.y < c.y+10 &&
            p.y+p.h > c.y;

        if(hit){

            boost[p.id]=8*60;

            return false;
        }

        return true;
    });
}

/* =========================================================
   DRAW WORLD
========================================================= */

function draw(){

    // background
    ctx.fillStyle="#070b18";
    ctx.fillRect(0,0,1200,650);

    // stars
    ctx.fillStyle="white";
    for(let s of stars){
        ctx.beginPath();
        ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fill();
    }

    // moon
    ctx.fillStyle="#f8fafc";
    ctx.beginPath();
    ctx.arc(1000,100,50,0,Math.PI*2);
    ctx.fill();

    // platforms
    for(let p of platforms()){
        ctx.fillStyle="#334155";
        ctx.fillRect(p.x,p.y,p.w,p.h);
    }
}

/* =========================================================
   LOOP
========================================================= */

function loop(){

    draw();

    if(gameStarted && !winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        checkCoins(p1);
        checkCoins(p2);

        if(collide(p1,p2)){

            if(p1.dy>0 && p1.y<p2.y){
                p1.score++;
                reset();
            }

            if(p2.dy>0 && p2.y<p1.y){
                p2.score++;
                reset();
            }
        }

        if(p1.score>=3) winner=p1.name;
        if(p2.score>=3) winner=p2.name;
    }

    drawCoins();

    p1.draw();
    p2.draw();

    ctx.fillStyle="white";
    ctx.font="20px Arial";
    ctx.fillText(p1.name+": "+p1.score,30,30);
    ctx.fillText(p2.name+": "+p2.score,1000,30);

    if(winner){
        ctx.font="50px Arial";
        ctx.fillText(winner+" gewinnt!",400,300);
    }

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
