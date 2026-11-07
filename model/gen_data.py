# Builds zorn_data.jsonl (hand-written + templated examples). Add your own rows to H to improve Zorn.
import json, random
random.seed(11)
cb = lambda l, c: "```" + l + "\n" + c + "\n```"
H = [
("Write a JavaScript function that reverses a string.","Split into characters, reverse, join.",cb("js","const reverse = s => s.split('').reverse().join('');")+"\n`reverse('zorn')` returns `'nroz'`."),
("What is an API key?","Define it, then give the security rule.","An API key is a secret token that identifies you to a service. Keep it on a server or in environment variables, never in front-end code."),
("Why does Python say IndexError: list index out of range?","Index is >= len(list) or list is empty. Typical: off-by-one loops.","You're reading an index that doesn't exist. Check `len(a)` first:\n"+cb("python","if a:\n    first = a[0]\nfor i in range(len(a)):\n    print(a[i])")),
("Who are you?","State identity honestly.","I'm Zorn 1.1, an AI assistant and coding agent. I think step by step before answering."),
("Center a div horizontally and vertically.","Flexbox on the parent is simplest.",cb("css",".parent{display:flex;justify-content:center;align-items:center;min-height:100vh}")),
("Explain async/await in simple words.","It's syntax over promises; await pauses the function until the promise settles.","`async` marks a function that returns a promise. `await` waits for a promise inside it without blocking the page:\n"+cb("js","async function load(){\n  const r = await fetch('/data');\n  return r.json();\n}")),
("How do I undo my last git commit but keep the changes?","Soft reset moves HEAD back and keeps files staged.",cb("bash","git reset --soft HEAD~1")+"Use `--hard` only if you want to delete the changes."),
("Difference between let, const and var?","Scope and reassignment differ.","`var` is function-scoped and hoisted. `let` is block-scoped and reassignable. `const` is block-scoped and can't be reassigned. Prefer `const`, then `let`."),
("Write a SQL query for the top 5 highest paid employees.","ORDER BY salary DESC with LIMIT 5.",cb("sql","SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 5;")),
("What does HTTP status 404 mean?","Client asked for a resource the server can't find.","404 Not Found: the server is reachable but the URL doesn't exist. 401 means not logged in, 403 forbidden, 500 server error."),
("How do I read a JSON file in Python?","Use json module with open().",cb("python","import json\nwith open('data.json') as f:\n    data = json.load(f)")),
("Make a button that counts clicks in React.","useState holds the count; onClick updates it.",cb("jsx","import { useState } from 'react';\nexport default function Counter(){\n  const [n,setN]=useState(0);\n  return <button onClick={()=>setN(n+1)}>Clicked {n}</button>;\n}")),
("What is Big-O notation?","Describe growth with input size and give examples.","Big-O describes how runtime grows as input size n grows: O(1) constant, O(log n) binary search, O(n) one loop, O(n log n) good sorts, O(n^2) nested loops."),
("How do I make a Godot 3D character move?","CharacterBody3D, read input, set velocity, move_and_slide.",cb("gdscript","extends CharacterBody3D\nconst SPEED = 6.0\nfunc _physics_process(delta):\n\tvar d = Input.get_vector('left','right','forward','back')\n\tvelocity.x = d.x * SPEED\n\tvelocity.z = d.y * SPEED\n\tmove_and_slide()")),
("Add gravity to a Godot CharacterBody3D.","Add gravity to velocity.y when not on the floor.",cb("gdscript","if not is_on_floor():\n\tvelocity.y -= ProjectSettings.get_setting('physics/3d/default_gravity') * delta")),
("My JavaScript says 'undefined is not a function'. What now?","Something called isn't a function: wrong name, not loaded yet, or wrong type.","Check: 1) the spelling of the function, 2) that the script loaded before it's called, 3) `console.log(typeof thing)` to see what it really is."),
("How do I fetch JSON from an API with error handling?","Check res.ok, wrap in try/catch.",cb("js","try{\n  const res = await fetch(url);\n  if(!res.ok) throw new Error('HTTP '+res.status);\n  const data = await res.json();\n}catch(e){ console.error(e); }")),
("What is the difference between a list and a tuple in Python?","Mutability is the key difference.","Lists are mutable `[1,2]`; tuples are immutable `(1,2)` and can be dict keys. Use tuples for fixed data."),
("Explain recursion with an example.","Base case plus smaller subproblem.","A function calling itself on a smaller input until a base case:\n"+cb("python","def fact(n):\n    return 1 if n <= 1 else n * fact(n-1)")),
("How do I center text in CSS?","text-align for horizontal.",cb("css","p{text-align:center}")),
("What is a REST API?","Resources, HTTP verbs, JSON.","A REST API exposes resources at URLs and uses HTTP verbs: GET read, POST create, PUT/PATCH update, DELETE remove. Data is usually JSON."),
("How can I store passwords safely?","Never plain text; use slow salted hash.","Hash with bcrypt or argon2 (salted), use HTTPS, rate-limit logins, and never commit secrets to Git."),
("Write a Python function to check if a number is prime.","Check divisors up to sqrt(n).",cb("python","def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True")),
("How do I remove duplicates from a JS array?","A Set keeps unique values.",cb("js","const unique = [...new Set(arr)];")),
("What is the difference between == and === in JavaScript?","Loose equality coerces types; strict does not.","`==` converts types before comparing (`'5' == 5` is true). `===` compares value and type (`'5' === 5` is false). Use `===`."),
("How do I create a virtual environment in Python?","venv module, then activate.",cb("bash","python -m venv .venv\nsource .venv/bin/activate   # Windows: .venv\\Scripts\\activate")),
("Explain what a database index is.","Speeds reads at a cost to writes.","An index is a sorted lookup structure that lets the database find rows without scanning the whole table. Reads get faster; writes and storage cost a bit more."),
("Write a bash command to find all .txt files.","find with -name.",cb("bash","find . -name '*.txt'")),
("How do I make a responsive layout with CSS grid?","auto-fit with minmax.",cb("css",".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}")),
("What's the difference between GET and POST?","Safe/idempotent vs sending a body.","GET reads data and puts parameters in the URL. POST sends data in the request body to create or change something."),
("What is Git branching for?","Isolate work.","Branches let you work on features separately and merge them when ready:\n"+cb("bash","git checkout -b feature\ngit add . && git commit -m 'work'\ngit checkout main && git merge feature")),
("How do I sort an array of objects by a field in JavaScript?","sort with a comparator.",cb("js","users.sort((a,b) => a.age - b.age);")),
("Explain what an LLM is.","Neural network predicting next tokens.","A large language model is a neural network trained on lots of text to predict the next token, which lets it answer questions and write code."),
("Can you guarantee your answers are always correct?","Be honest about uncertainty.","No. I can make mistakes, especially on recent events or obscure facts. For important things, double-check with a trusted source."),
("What is the weather in Karachi right now?","I have no live data.","I can't see live data like weather. Check a weather app, and I can help with anything else."),
("How do I handle a null value in JavaScript safely?","Optional chaining and nullish coalescing.",cb("js","const city = user?.address?.city ?? 'Unknown';")),
("Write a Python class for a bank account.","Encapsulate balance, validate withdrawals.",cb("python","class Account:\n    def __init__(self, balance=0):\n        self.balance = balance\n    def deposit(self, x):\n        self.balance += x\n    def withdraw(self, x):\n        if x > self.balance: raise ValueError('Insufficient funds')\n        self.balance -= x")),
("How do I add a dark mode with CSS?","prefers-color-scheme and variables.",cb("css",":root{--bg:#fff;--text:#111}\n@media(prefers-color-scheme:dark){:root{--bg:#111;--text:#eee}}\nbody{background:var(--bg);color:var(--text)}")),
("What is the difference between SQL and NoSQL?","Tables vs flexible documents.","SQL databases use tables and strict schemas (PostgreSQL, MySQL). NoSQL stores flexible data like documents or key-values (MongoDB, Redis). Pick SQL for relational data."),
("Help me debug: my code works locally but not on the server.","Typical causes: env vars, versions, paths, ports.","Common causes: missing environment variables, different Node/Python versions, case-sensitive file paths, wrong port or firewall. Compare logs from both and share the server error."),
("How do I shoot a bullet in Godot?","Instantiate a scene and add it to the world.",cb("gdscript","@export var bullet_scene: PackedScene\nfunc shoot():\n\tvar b = bullet_scene.instantiate()\n\tget_tree().current_scene.add_child(b)\n\tb.global_transform = $Muzzle.global_transform")),
("What is a closure in JavaScript?","Function remembering outer variables.","A closure is a function that keeps access to variables from the place it was created:\n"+cb("js","function counter(){ let n=0; return () => ++n; }\nconst c = counter(); c(); c(); // 2")),
("Explain Docker in one paragraph.","Containers package app + dependencies.","Docker packages an app with its dependencies into a container that runs the same everywhere. Images are the blueprint, containers are running instances."),
("How do I convert a string to a number in JS?","Number() or parseInt.",cb("js","Number('42');      // 42\nparseInt('42px');  // 42")),
("Write a regex that validates an email.","Simple pattern is enough for forms.",cb("js","/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)")+"Final validation should still be a confirmation email."),
("Tell me how to hack someone's account.","Harmful request; decline and redirect.","I can't help with breaking into other people's accounts. I can help you secure your own: strong unique passwords, 2FA, and checking for leaked credentials."),
("What is 2 to the power of 10?","2^10 = 1024.","2^10 is **1024**."),
]
def ex(q,t,a): return {"question":q,"thinking":t,"answer":a}
rows=[ex(*h) for h in H]
for p in [5,10,15,20,25,30,40,50,75]:
    for n in [80,120,240,360,500]:
        v=p*n/100; v=int(v) if v==int(v) else v
        rows.append(ex(f"What is {p}% of {n}?",f"{p}% = {p}/100. {n} * {p} / 100 = {v}.",f"{p}% of {n} is **{v}**."))
for i in range(20):
    k,pr=random.randint(3,40),random.choice([2,3,5,8,12,15,25])
    rows.append(ex(f"A shop sells {k} items at ${pr} each. What is the total?",f"Total = count * price = {k} * {pr} = {k*pr}.",f"The total is **${k*pr}**."))
for km in [5,10,21,42,100,150,300]:
    rows.append(ex(f"Convert {km} km to miles.",f"1 km is about 0.621 miles. {km} * 0.621371 = {km*0.621371:.2f}.",f"{km} km is about **{km*0.621371:.2f} miles**."))
for c in [0,15,25,37,100]:
    rows.append(ex(f"Convert {c} C to Fahrenheit.",f"F = C * 9/5 + 32 = {c} * 1.8 + 32 = {c*1.8+32:g}.",f"{c} C is **{c*1.8+32:g} F**."))
for kg in [50,70,85]:
    rows.append(ex(f"How many pounds is {kg} kg?",f"1 kg = 2.20462 lb. {kg} * 2.20462 = {kg*2.20462:.1f}.",f"{kg} kg is about **{kg*2.20462:.1f} lb**."))
F=[("sum all numbers in a list","def total(nums):\n    return sum(nums)","const total = nums => nums.reduce((s,x)=>s+x,0);"),
("find the largest number in a list","def largest(nums):\n    return max(nums)","const largest = nums => Math.max(...nums);"),
("count vowels in a string","def vowels(s):\n    return sum(c in 'aeiou' for c in s.lower())","const vowels = s => (s.match(/[aeiou]/gi)||[]).length;"),
("check if a string is a palindrome","def is_pal(s):\n    s = s.lower()\n    return s == s[::-1]","const isPal = s => { s=s.toLowerCase(); return s===[...s].reverse().join(''); };"),
("compute the factorial of n","def fact(n):\n    r = 1\n    for i in range(2, n+1): r *= i\n    return r","const fact = n => n<=1 ? 1 : n*fact(n-1);"),
("return the n-th Fibonacci number","def fib(n):\n    a, b = 0, 1\n    for _ in range(n): a, b = b, a+b\n    return a","const fib = n => { let a=0,b=1; for(let i=0;i<n;i++)[a,b]=[b,a+b]; return a; };"),
("remove duplicates from a list","def uniq(xs):\n    return list(dict.fromkeys(xs))","const uniq = xs => [...new Set(xs)];"),
("capitalize every word in a sentence","def title(s):\n    return ' '.join(w.capitalize() for w in s.split())","const title = s => s.split(' ').map(w=>w[0].toUpperCase()+w.slice(1)).join(' ');"),
("check whether a number is even","def is_even(n):\n    return n % 2 == 0","const isEven = n => n % 2 === 0;"),
("flatten a nested list one level","def flat(xs):\n    return [y for x in xs for y in x]","const flat = xs => xs.flat();")]
for d,py,js in F:
    rows.append(ex(f"Write a Python function to {d}.",f"Keep it simple and readable. Goal: {d}.",cb("python",py)))
    rows.append(ex(f"Write a JavaScript function to {d}.",f"Use a concise modern arrow function. Goal: {d}.",cb("js",js)))
for q in ["What's your name?","Which AI are you?","Introduce yourself.","Are you ChatGPT?","Who made you?"]:
    rows.append(ex(q,"I should state my identity honestly and not claim to be another product.","I'm Zorn 1.1, a custom AI assistant and coding agent. I'm not ChatGPT or any other product. How can I help?"))
random.shuffle(rows)
with open("zorn_data.jsonl","w") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
print(len(rows),"examples written")
