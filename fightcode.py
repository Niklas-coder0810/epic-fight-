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

/* ===================== GAME WINDOW (1/4 SCREEN + LANDSCAPE) ===================== */

.game-wrapper{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);

    width:min(1100px,85vw);
    height:min(620px,80vh);

    border-radius:18px;
    overflow:hidden;

    border:2px solid rgba(255,255,255,0.08);
}

canvas{
    display:block;
    width:100%;
    height:100%;
}

/* ===================== MENU ===================== */

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

    border-radius:28px;

    padding:40px;

    text-align:center;

    color:white;

    border:1px solid rgba(255,255,255,0.08);
}

.menu-box input,
.menu-box select{

    width:100%;
    padding:14px;
    margin-top:10px;

    border:none;
    border-radius:12px;

    background:#24324d;
    color:white;
}

.menu-box button{

    width:100%;
    margin-top:20px;
    padding:16px;

    border:none;
    border-radius:14px;

    font-size:18px;

    color:white;
    background:linear-gradient(to right,#2563eb,#38bdf8);

    cursor:pointer;
}

/* ===================== END SCREEN ===================== */

#end{

    position:absolute;
    width:100%;
    height:100%;

    display:none;

    justify-content:center;
    align-items:center;
    flex-direction:column;

    background:rgba(0,0,0,0.85);

    color:white;

    z-index:100;
}

#end h1{
    font-size:60px;
}

#end button{
    margin-top:20px;
    padding:12px;
    border:none;
    border-radius:10px;
    background:#2563eb;
    color:white;
    cursor:pointer;
}

/* ===================== HUD ===================== */

#hud{

    position:absolute;
    top:10px;
    width:100%;

    display:flex;
    justify-content:space-between;

    padding:0 20px;

    color:white;

    font-weight:bold;

    z-index:5;
}

</style>
</head>

<body>

<!-- ================= MENU ================= -->

<div id="menu">

    <div class="menu-box">

        <h2>⚔ Jump Battle</h2>

        <input id="p1name" placeholder="Spieler 1">

        <select id="p1color">
            <option value="red">Rot</option>
            <option value="blue">Blau</option>
            <option value="green">Grün</option>
            <option value="yellow">Gelb</option>
            <option value="hotpink">Pink</option>
        </select>

        <input id="p2name" placeholder="Spieler 2">

        <select id="p2color">
            <option value="blue">Blau</option>
            <option value="red">Rot</option>
            <option value="green">Grün</option>
            <option value="yellow">Gelb</option>
            <option value="hotpink">Pink</option>
        </select>

        <button onclick="start()">START</button>

    </div>

</div>

<!-- ================= END ================= -->

<div id="end">
    <h1 id="winnerText"></h1>
    <div>🏆 CHAMPION CEREMONY 🏆</div>
    <button onclick="location.reload()">Zurück zum Menü</button>
</div>

<!-- ================= HUD ================= -->

<div id="hud"></div>

<!-- ================= GAME ================= -->

<div class="game-wrapper">
<canvas id="game"></canvas>
</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = 1100;
canvas.height = 620;

let game = false;
let winner = null;

/* ================= PHYSICS ================= */

const gravity = 0.8;

/* ================= FIREWORK ================= */

let particles = [];

function firework(x,y){

    for(let i=0;i<60;i++){

        particles.push({
            x:x,
            y:y,
            dx:(Math.random()-0.5)*8,
            dy:(Math.random()-0.5)*8,
            life:70
        });
    }
}

/* ================= PLATFORMS ================= */

function platforms(){

    return[
        {x:0,y:580,w:1100,h:40},
        {x:150,y:450,w:300,h:25},
        {x:700,y:450,w:300,h:25},
        {x:420,y:320,w:260,h:25}
    ];
}

/* ================= PLAYER ================= */

class Player{

    constructor(x,y,color){

        this.x=x;
        this.y=y;
        this.w=50;
        this.h=80;

        this.dx=0;
        this.dy=0;

        this.color=color;

        this.score=0;

        this.onGround=false;
    }

    draw(){

        ctx.fillStyle=this.color;
        ctx.fillRect(this.x,this.y,this.w,this.h);

        // face
        ctx.fillStyle="white";
        ctx.fillRect(this.x+10,this.y+20,6,6);
        ctx.fillRect(this.x+30,this.y+20,6,6);
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

                if(this.dy > 0 && this.y+this.h-this.dy <= p.y){

                    this.y = p.y - this.h;
                    this.dy = 0;
                    this.onGround = true;
                }
            }
        }

        if(this.x < 0) this.x = 0;
        if(this.x > 1050) this.x = 1050;
    }
}

/* ================= PLAYERS ================= */

const p1 = new Player(200,100,"red");
const p2 = new Player(800,100,"blue");

/* ================= INPUT ================= */

const keys = {};

window.addEventListener("keydown",e=>keys[e.code]=true);
window.addEventListener("keyup",e=>keys[e.code]=false);

/* ================= CONTROLS ================= */

function control(p,l,r,j){

    p.dx = 0;

    if(keys[l]) p.dx = -6;
    if(keys[r]) p.dx = 6;

    if(keys[j] && p.onGround) p.dy = -15;
}

/* ================= START ================= */

function start(){

    p1.color = document.getElementById("p1color").value;
    p2.color = document.getElementById("p2color").value;

    document.getElementById("menu").style.display="none";

    game = true;
}

/* ================= RESET ================= */

function reset(){

    p1.x=200; p1.y=100; p1.dy=0;
    p2.x=800; p2.y=100; p2.dy=0;
}

/* ================= COLLISION ================= */

function collide(a,b){

    return a.x<b.x+b.w &&
           a.x+a.w>b.x &&
           a.y<b.y+b.h &&
           a.y+a.h>b.y;
}

/* ================= LOOP ================= */

function loop(){

    ctx.fillStyle="#0b1020";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    for(let p of platforms()){

        ctx.fillStyle="#334155";
        ctx.fillRect(p.x,p.y,p.w,p.h);
    }

    if(game && !winner){

        control(p1,"KeyA","KeyD","KeyW");
        control(p2,"ArrowLeft","ArrowRight","ArrowUp");

        p1.update();
        p2.update();

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

        if(p1.score>=3 && !winner){

            winner = p1;
            firework(canvas.width/2,canvas.height/2);
        }

        if(p2.score>=3 && !winner){

            winner = p2;
            firework(canvas.width/2,canvas.height/2);
        }
    }

    // firework particles
    for(let i=particles.length-1;i>=0;i--){

        let p = particles[i];

        p.x += p.dx;
        p.y += p.dy;
        p.life--;

        ctx.fillStyle="white";
        ctx.fillRect(p.x,p.y,3,3);

        if(p.life<=0) particles.splice(i,1);
    }

    p1.draw();
    p2.draw();

    document.getElementById("hud").innerHTML =
        "P1: "+p1.score+" | P2: "+p2.score;

    if(winner){

        document.getElementById("end").style.display="flex";
        document.getElementById("winnerText").innerText =
            winner.color.toUpperCase() + " WINS!";
    }

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=1000)
