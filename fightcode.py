import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    overflow:hidden;
    font-family:Arial;
    background:#070b18;
}

canvas{
    width:100vw;
    height:100vh;
    display:block;
}

/* ---------------- MENU ---------------- */

#menu{
    position:absolute;
    width:100%;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:rgba(0,0,0,0.75);
    z-index:20;
}

.menu-box{
    width:min(520px,92vw);
    background:#111c33;
    padding:40px;
    border-radius:25px;
    text-align:center;
    color:white;
    box-shadow:0 0 50px rgba(0,0,0,0.6);
}

.menu-box h1{
    font-size:54px;
    margin-bottom:10px;
}

.menu-box p{
    color:#94a3b8;
    margin-bottom:20px;
}

.input-label{
    text-align:left;
    margin-top:15px;
    margin-bottom:5px;
    color:#cbd5e1;
    font-weight:bold;
}

.menu-box input{
    width:100%;
    padding:14px;
    border-radius:12px;
    border:none;
    background:#24324d;
    color:white;
    font-size:18px;
    outline:none;
}

.menu-box button{
    width:100%;
    margin-top:25px;
    padding:16px;
    border:none;
    border-radius:14px;
    font-size:20px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(to right,#2563eb,#38bdf8);
}

/* ---------------- POPUP ---------------- */

#popup{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:60px;
    color:white;
    display:none;
    z-index:30;
    font-weight:bold;
}

/* ---------------- HUD ---------------- */

#hud{
    position:absolute;
    top:15px;
    width:100%;
    display:flex;
    justify-content:space-between;
    padding:0 30px;
    color:white;
    font-size:22px;
    font-weight:bold;
    z-index:5;
}

</style>
</head>

<body>

<div id="menu">
    <div class="menu-box">
        <h1>🌙 Jump Battle</h1>
        <p>Gib eure Namen ein und starte das Spiel</p>

        <div class="input-label">Spieler 1 (WASD)</div>
        <input id="p1name" placeholder="Name Spieler 1">

        <div class="input-label">Spieler 2 (Pfeiltasten)</div>
        <input id="p2name" placeholder="Name Spieler 2">

        <button onclick="startGame()">Start</button>
    </div>
</div>

<div id="popup"></div>

<div id="hud"></div>

<canvas id="game"></canvas>

<script>

/* ---------------- CANVAS ---------------- */

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

/* ---------------- GAME STATE ---------------- */

let gameStarted = false;
let winner = null;

const gravity = 0.8;

/* ---------------- BACKGROUND ---------------- */

const stars = [];

for(let i=0;i<200;i++){
    stars.push({
        x:Math.random()*window.innerWidth,
        y:Math.random()*window.innerHeight,
        r:Math.random()*2
    });
}

/* ---------------- POPUP ---------------- */

function popup(text){
    const p=document.getElementById("popup");
    p.innerText=text;
    p.style.display="block";

    setTimeout(()=>{
        p.style.display="none";
    },2000);
}

/* ---------------- BOOST ---------------- */

let boost = {
    p1:0,
    p2:0
};

/* ---------------- COINS ---------------- */

let coins = [];

function spawnCoin(){
    coins.push({
        x:Math.random()*canvas.width,
        y:Math.random()*canvas.height/2
    });
}

setInterval(()=>{
    if(gameStarted && !winner){
        if(Math.random() < 0.6){
            spawnCoin();
        }
    }
},3000);

/* ---------------- PLATFORMS ---------------- */

function platforms(){
    return [
        {x:0,y:canvas.height-50,w:canvas.width,h:50},

        {x:150,y:canvas.height-220,w:320,h:20},
        {x:canvas.width-470,y:canvas.height-220,w:320,h:20},

        {x:canvas.width/2-170,y:canvas.height-380,w:340,h:20},

        {x:120,y:canvas.height-540,w:280,h:20},
        {x:canvas.width-400,y:canvas.height-540,w:280,h:20}
    ];
}

/* ---------------- PLAYER ---------------- */

class Player{

    constructor(x,y,color,controls){
        this.x=x;
        this.y=y;
        this.w=60;
        this.h=90;
        this.color=color;
        this.dx=0;
        this.dy=0;
        this.score=0;
        this.controls=controls;
        this.onGround=false;
        this.name="";
    }

    speed(){
        return (boost[this.id] > 0) ? 12 : 7;
    }

    draw(){
        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);
    }

    update(){

        this.dy += gravity;
        this.x += this.dx;
        this.y += this.dy;

        this.onGround = false;

        for(let p of platforms()){

            const hit =
                this.x < p.x+p.w &&
                this.x+this.w > p.x &&
                this.y < p.y+p.h &&
                this.y+this.h > p.y;

            if(hit){

                // LANDEN
                if(this.dy > 0 && this.y+this.h-this.dy <= p.y){
                    this.y = p.y - this.h;
                    this.dy = 0;
                    this.onGround = true;
                }

                // DECKEL BLOCK
                else if(this.dy < 0 && this.y >= p.y+p.h-5){
                    this.y = p.y+p.h;
                    this.dy = 0;
                }
            }
        }

        if(this.x < 0) this.x = 0;
        if(this.x + this.w > canvas.width) this.x = canvas.width - this.w;
    }
}

/* ---------------- INPUT ---------------- */

const keys = {};

window.addEventListener("keydown",e=>keys[e.code]=true);
window.addEventListener("keyup",e=>keys[e.code]=false);

/* ---------------- PLAYERS ---------------- */

const p1 = new Player(200,100,"#ef4444",{l:"KeyA",r:"KeyD",j:"KeyW"});
const p2 = new Player(700,100,"#3b82f6",{l:"ArrowLeft",r:"ArrowRight",j:"ArrowUp"});

p1.id="p1";
p2.id="p2";

/* ---------------- CONTROLS ---------------- */

function controls(p){

    p.dx = 0;

    let sp = (boost[p.id] > 0) ? 11 : 7;

    if(keys[p.controls.l]) p.dx = -sp;
    if(keys[p.controls.r]) p.dx = sp;

    if(keys[p.controls.j] && p.onGround){
        p.dy = -16;
    }
}

/* ---------------- START ---------------- */

function startGame(){

    p1.name = document.getElementById("p1name").value || "P1";
    p2.name = document.getElementById("p2name").value || "P2";

    document.getElementById("menu").style.display="none";

    gameStarted = true;
}

/* ---------------- RESET ---------------- */

function reset(){

    p1.x=200;p1.y=100;p1.dy=0;
    p2.x=700;p2.y=100;p2.dy=0;
}

/* ---------------- COLLISION ---------------- */

function collide(a,b){
    return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
}

/* ---------------- COINS ---------------- */

function drawCoins(){

    ctx.fillStyle="gold";

    for(let c of coins){

        ctx.beginPath();
        ctx.arc(c.x,c.y,8,0,Math.PI*2);
        ctx.fill();
    }
}

function checkCoins(p){

    coins = coins.filter(c=>{

        let hit =
            p.x < c.x+10 &&
            p.x+p.w > c.x &&
            p.y < c.y+10 &&
            p.y+p.h > c.y;

        if(hit){

            boost[p.id] = 8*60;

            popup(p.name + " SPEED BOOST!");

            return false;
        }

        return true;
    });
}

/* ---------------- DRAW ---------------- */

function drawBackground(){

    const g = ctx.createLinearGradient(0,0,0,canvas.height);

    g.addColorStop(0,"#070b18");
    g.addColorStop(1,"#111827");

    ctx.fillStyle=g;
    ctx.fillRect(0,0,canvas.width,canvas.height);

    // Sterne
    ctx.fillStyle="white";
    for(let s of stars){
        ctx.beginPath();
        ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
        ctx.fill();
    }

    // Mond
    ctx.fillStyle="#f8fafc";
    ctx.beginPath();
    ctx.arc(canvas.width-150,120,60,0,Math.PI*2);
    ctx.fill();
}

function drawPlatforms(){

    for(let p of platforms()){

        ctx.fillStyle="#334155";
        ctx.fillRect(p.x,p.y,p.w,p.h);

        ctx.fillStyle="#64748b";
        ctx.fillRect(p.x,p.y,p.w,4);
    }
}

/* ---------------- LOOP ---------------- */

function loop(){

    drawBackground();

    if(gameStarted && !winner){

        controls(p1);
        controls(p2);

        p1.update();
        p2.update();

        checkCoins(p1);
        checkCoins(p2);

        if(boost.p1>0)boost.p1--;
        if(boost.p2>0)boost.p2--;

        if(collide(p1,p2)){

            if(p1.dy>0 && p1.y<p2.y){
                p1.score++;
                popup(p1.name+" +1");
                reset();
            }

            if(p2.dy>0 && p2.y<p1.y){
                p2.score++;
                popup(p2.name+" +1");
                reset();
            }
        }

        if(p1.score>=3)winner=p1.name;
        if(p2.score>=3)winner=p2.name;
    }

    drawPlatforms();

    drawCoins();

    p1.draw();
    p2.draw();

    document.getElementById("hud").innerHTML =
        p1.name+" : "+p1.score+" | "+p2.name+" : "+p2.score;

    if(winner){

        ctx.fillStyle="white";
        ctx.font="60px Arial";
        ctx.fillText(winner+" gewinnt!",canvas.width/2-200,canvas.height/2);
    }

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=1200)
