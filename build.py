#!/usr/bin/env python3
"""Builds index.html for pittner/fitness-vision-board.

A single-purpose page for the "fitness vision board" / "gym vision board 2027" search intent:
36 fitness goals in 6 groups (strength and gym, running and cardio, flexibility and recovery,
outdoor and adventure, sports and teams, fitness habits and mindset), each with why it matters
and a first step; one click opens the free maker prefilled as a phone lock screen. Plus 12
questions, a 45-minute plan, a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/fitness-vision-board/"
SRC = "ghpages_fitness"
CAMPAIGN = "fitness_2027"

GROUPS = [
    ("Strength and gym", [
        ("Do my first unassisted pull-up", "A pull-up proves you can move your own body weight, and that changes how you see yourself.", "Hang from a bar for 20 seconds today and note how it feels"),
        ("Squat my own body weight", "Leg strength protects your knees, your back and your independence as you age.", "Find your current max and write it down so you have a starting number"),
        ("Train consistently three times a week", "Three sessions a week is enough to change your body and your energy in 90 days.", "Block three 45-minute slots in your calendar for the next two weeks"),
        ("Build a simple home gym", "Removing the commute to the gym removes the biggest excuse.", "Buy one pair of adjustable dumbbells and a mat this week"),
        ("Deadlift double my body weight", "The deadlift builds full-body strength that carries into everything you do outside the gym.", "Test your current one-rep max or estimate it from your working sets"),
        ("Feel strong, not just look strong", "Strength you can use every day matters more than a mirror number.", "Pick one real-world task that is hard for you now and train for it"),
    ]),
    ("Running and cardio", [
        ("Run my first 5K without stopping", "Five kilometres proves your heart and lungs can handle more than you thought.", "Run or walk for 20 minutes today and note how far you get"),
        ("Finish a half marathon", "21 kilometres is the distance where discipline matters more than talent.", "Find a half marathon in the next 6 months and write the date on your wall"),
        ("Run faster, not just farther", "Speed work improves efficiency and makes every easy run feel easier.", "Add one short interval session per week to your current routine"),
        ("Cycle to work at least twice a week", "Bike commuting adds cardio without taking extra time.", "Map the route, check travel time and try it once this Saturday"),
        ("Swim regularly again", "Swimming is the easiest way to move every muscle without joint stress.", "Find a pool nearby, check opening hours and pack a bag tonight"),
        ("Get my resting heart rate below 60", "A lower resting heart rate means a more efficient heart and better recovery.", "Measure your resting heart rate three mornings in a row and write the average"),
    ]),
    ("Flexibility and recovery", [
        ("Touch my toes comfortably", "Basic flexibility prevents the back pain and stiffness that slow people down in their 30s and 40s.", "Stretch for 5 minutes after your next workout, hamstrings first"),
        ("Start a morning stretch routine", "Ten minutes of stretching before coffee sets the body and the mood for the day.", "Do a 10-minute YouTube stretch video tomorrow before breakfast"),
        ("Try yoga once a week", "Yoga builds flexibility, balance and calm at the same time.", "Find one beginner class near you or online and book the first session"),
        ("Sleep 7 to 8 hours every night", "Sleep is when your muscles actually grow and your willpower refills.", "Set a phone alarm for bedtime, not just wake-up, starting tonight"),
        ("Foam roll after every session", "Five minutes of rolling reduces soreness and keeps you training without forced rest days.", "Buy a foam roller and use it after your next workout"),
        ("Take one full rest day every week", "Rest days are when adaptation happens, not a sign of laziness.", "Pick a fixed rest day and write it into your training plan"),
    ]),
    ("Outdoor and adventure", [
        ("Hike a mountain I have never climbed", "A summit gives you a goal that is about the journey, not the mirror.", "Pick one mountain within driving distance and check the trail on a map"),
        ("Train for a mud run or obstacle race", "Obstacle races test strength, cardio and problem-solving in one event.", "Find an event in the next 4 months and sign up this week"),
        ("Kayak, paddle or surf regularly", "Water sports build core strength and clear the head faster than any gym.", "Rent or borrow equipment once and try it on the nearest water"),
        ("Walk 10 000 steps every day for a month", "Daily steps are the lowest-friction fitness habit that compounds quietly.", "Check your step count today and note how far you are from 10 000"),
        ("Spend more time training outside", "Fresh air and sunlight improve mood, vitamin D and training enjoyment.", "Move one indoor workout outside this week, even if it is just a walk"),
        ("Climb a via ferrata or try rock climbing", "Climbing forces you to solve a physical puzzle one move at a time.", "Find the nearest climbing wall, check prices and book a taster session"),
    ]),
    ("Sports and teams", [
        ("Join a sports team or group", "Playing with others makes fitness feel like fun instead of a chore.", "Search for local groups in the sport you liked as a kid and message one"),
        ("Learn a martial art", "Martial arts build discipline, reflexes and confidence in equal measure.", "Visit one martial arts gym this week and watch a class"),
        ("Play a sport I loved as a teenager", "The sport you dropped at 18 probably still makes you happy.", "Find where that sport is played near you and go once"),
        ("Get better at one sport, not five", "Focus beats variety when you want real improvement.", "Pick the one sport you enjoy most and commit to it for 3 months"),
        ("Compete in something, anything", "A race date or match day gives training a purpose that the gym alone does not.", "Enter one event in the next 90 days, even a small local one"),
        ("Coach or mentor someone in fitness", "Teaching locks in your own knowledge and keeps you accountable.", "Offer to train with one friend who is just starting out"),
    ]),
    ("Fitness habits and mindset", [
        ("Track my workouts every session", "What you measure improves, and a log shows progress your body hides.", "Start a simple note on your phone with today's workout"),
        ("Eat enough protein every day", "Muscle needs protein, and most people eat half of what they need.", "Calculate 1.6 grams per kilo of your body weight and check today's intake"),
        ("Drink enough water without reminders", "Hydration affects strength, focus and recovery more than any supplement.", "Fill a bottle in the morning and finish it by lunch"),
        ("Stop comparing my body to strangers online", "Social media bodies are selected, edited and often unhealthy to maintain.", "Unfollow three accounts that make you feel worse after scrolling"),
        ("Warm up properly before every session", "Five minutes of warming up prevents the injury that costs you six weeks.", "Do 5 minutes of light movement before your next workout"),
        ("Make fitness part of my identity, not a phase", "When you see yourself as someone who trains, skipping feels wrong instead of normal.", "Write one sentence about who you are as a person who moves and read it tonight"),
    ]),
]

QUESTIONS = [
    "What kind of movement makes me feel most alive?",
    "When was the last time I felt truly strong, and what was I doing?",
    "What stopped my last fitness streak, and what would prevent it this time?",
    "Am I training for how I look, how I feel or what I can do?",
    "If I could only do one type of exercise for a year, which would it be?",
    "What fitness goal have I been putting off because it feels too hard?",
    "Do I train better alone or with other people?",
    "What does my body need more of right now: strength, flexibility or rest?",
    "How many hours a week can I realistically give to training?",
    "What injury or pain am I ignoring that I should address first?",
    "If I reach my fitness goal by December 2027, how will my daily life be different?",
    "Who in my life would notice the change, and what would they say?",
]

PLAN = [
    ("10 minutes: honest audit.", "Write down what you did last week, how your body feels now, and what you have been avoiding."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers; nobody else reads them."),
    ("10 minutes: pick three fitness goals.", "One you can do this month, one for this quarter and one for the year."),
    ("10 minutes: make it visible.", "Turn your main fitness goal and its first step into a phone lock screen, so you see it every time you pick up your phone."),
]

FAQ = [
    ("What should go on a fitness vision board?",
     "Your goal in your own words, a first step for this week, and the reason it matters to you. "
     "This page has 36 fitness goals in 6 groups (strength and gym, running and cardio, flexibility and recovery, outdoor and adventure, sports and teams, fitness habits and mindset), each with a first step and a free lock screen maker."),
    ("Does a fitness vision board actually work?",
     "A board does not lift the weight for you, but seeing your goal every day keeps it present when you decide how to spend your evening or what to eat. "
     "The habit that works best is putting it on your phone lock screen so you cannot ignore it."),
    ("How many fitness goals should I set for 2027?",
     "Three is enough: one strength or cardio goal, one habit goal and one recovery goal. Fewer goals get done more often than long lists."),
    ("Is this different from a weight loss vision board?",
     "Yes. Weight loss focuses on a number on the scale. A fitness vision board focuses on what your body can do: run further, lift more, move better, recover faster. The mindset shift matters."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full fitness vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fitness Vision Board 2027: %%COUNT%% Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% fitness goals for 2027 (strength and gym, running, flexibility, outdoor adventure, sports, fitness habits), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Fitness vision board 2027 - %%COUNT%% goals with a first step and a free lock screen">
<meta property="og:description" content="Strength, running, flexibility, outdoor and sports goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Fitness vision board 2027: %%COUNT%% goals with a first step for this week</h1>
  <p class="lede">Most fitness plans die in February because there is no clear goal, no first step and no daily reminder. Below are %%COUNT%% fitness goals for 2027, from your first pull-up to a half marathon and a morning stretch routine, each with why it matters and one thing you can do this week, plus %%NQ%% questions to find out what your body actually needs. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every day until it is done.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your fitness goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My fitness goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Run a half marathon by June" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Run 3K this Saturday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose your fitness goals</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads them. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your fitness year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full fitness vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/self-care-vision-board/">self care vision board</a>,
  <a href="https://pittner.github.io/travel-vision-board/">travel vision board</a>,
  <a href="https://pittner.github.io/dream-home-vision-board/">dream home vision board</a>,
  <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-for-relationships/">vision board for relationships</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/fitness-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
