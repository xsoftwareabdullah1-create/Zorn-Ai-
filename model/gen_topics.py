# Adds Three.js, PHP, SQL, GLSL, Unity C#, Godot, Blender Python, Kotlin/Android and Gradle examples to zorn_data.jsonl.
import json, random
random.seed(9)
cb = lambda l, c: "```" + l + "\n" + c.strip("\n") + "\n```"
R = []
def add(q, t, lang, code, note=""):
    R.append({"question": q, "thinking": t, "answer": cb(lang, code) + ("\n" + note if note else "")})

# ---------- Three.js ----------
add("Create a basic Three.js scene with a rotating cube.","Need scene, camera, renderer, a mesh with a lit material, lights, and an animation loop.","js",r'''
import * as THREE from 'three';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
camera.position.z = 3;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);
const cube = new THREE.Mesh(new THREE.BoxGeometry(), new THREE.MeshStandardMaterial({ color: 0x7c5cff }));
const sun = new THREE.DirectionalLight(0xffffff, 2); sun.position.set(3, 5, 4);
scene.add(cube, sun, new THREE.AmbientLight(0xffffff, 0.5));
renderer.setAnimationLoop(() => { cube.rotation.x += 0.01; cube.rotation.y += 0.01; renderer.render(scene, camera); });
''',"Load it with an import map or a bundler like Vite so `'three'` resolves.")
add("How do I handle window resize in Three.js?","Update camera aspect and projection, then renderer size.","js",r'''
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});''')
add("Add OrbitControls to a Three.js scene.","Import from addons, create with camera and canvas, update every frame if damping is on.","js",r'''
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
// inside the animation loop:
controls.update();''')
add("Load a GLB/GLTF model in Three.js.","Use GLTFLoader and add gltf.scene to the scene.","js",r'''
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
new GLTFLoader().load('model.glb',
  gltf => scene.add(gltf.scene),
  undefined,
  err => console.error('Load failed', err));''')
add("Enable shadows in Three.js.","Renderer flag, light castShadow, and per-mesh cast/receive flags.","js",r'''
renderer.shadowMap.enabled = true;
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
cube.castShadow = true;
floor.receiveShadow = true;''')
add("Detect a mouse click on a 3D object in Three.js.","Convert the pointer to normalized device coordinates, cast a Raycaster from the camera.","js",r'''
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
addEventListener('pointerdown', e => {
  mouse.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObjects(scene.children, true)[0];
  if (hit) console.log('clicked', hit.object.name, hit.point);
});''')
add("Apply a texture to a mesh in Three.js.","TextureLoader, set sRGB color space for color maps, use in material.map.","js",r'''
const tex = new THREE.TextureLoader().load('wood.jpg');
tex.colorSpace = THREE.SRGBColorSpace;
const mesh = new THREE.Mesh(new THREE.PlaneGeometry(4, 4), new THREE.MeshStandardMaterial({ map: tex }));''')
add("Play a GLTF animation in Three.js.","Create an AnimationMixer for the model, play a clip, and update it with the clock delta each frame.","js",r'''
let mixer; const clock = new THREE.Clock();
new GLTFLoader().load('character.glb', g => {
  scene.add(g.scene);
  mixer = new THREE.AnimationMixer(g.scene);
  mixer.clipAction(g.animations[0]).play();
});
// in the loop:
mixer?.update(clock.getDelta());''')
add("Write a custom ShaderMaterial in Three.js.","Provide uniforms, a vertex shader that outputs gl_Position, and a fragment shader using a time uniform.","js",r'''
const mat = new THREE.ShaderMaterial({
  uniforms: { uTime: { value: 0 } },
  vertexShader: `varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `varying vec2 vUv; uniform float uTime;
    void main() { gl_FragColor = vec4(vUv, 0.5 + 0.5 * sin(uTime), 1.0); }`
});
// in the loop:
mat.uniforms.uTime.value = clock.getElapsedTime();''')
add("Render 1000 cubes efficiently in Three.js.","Use InstancedMesh so it is a single draw call; set each instance matrix.","js",r'''
const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(), new THREE.MeshNormalMaterial(), 1000);
const m = new THREE.Matrix4();
for (let i = 0; i < 1000; i++) {
  m.setPosition(Math.random() * 50 - 25, Math.random() * 50 - 25, Math.random() * 50 - 25);
  mesh.setMatrixAt(i, m);
}
scene.add(mesh);''')
add("Make a particle system in Three.js.","Use BufferGeometry with a position attribute and Points material.","js",r'''
const N = 5000, pos = new Float32Array(N * 3).map(() => (Math.random() - 0.5) * 20);
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
scene.add(new THREE.Points(g, new THREE.PointsMaterial({ size: 0.05, color: 0xffffff })));''')
add("Make a first-person camera with WASD in Three.js.","PointerLockControls for mouse look, key state map, moveForward/moveRight scaled by delta time.","js",r'''
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
const controls = new PointerLockControls(camera, document.body);
addEventListener('click', () => controls.lock());
const keys = {};
addEventListener('keydown', e => keys[e.code] = true);
addEventListener('keyup', e => keys[e.code] = false);
function update(dt) {
  const s = 5 * dt;
  if (keys.KeyW) controls.moveForward(s);
  if (keys.KeyS) controls.moveForward(-s);
  if (keys.KeyD) controls.moveRight(s);
  if (keys.KeyA) controls.moveRight(-s);
}''')

# ---------- PHP ----------
add("Connect to MySQL in PHP safely with PDO.","Use PDO with exceptions and prepared statements to avoid SQL injection.","php",r'''
<?php
$pdo = new PDO('mysql:host=localhost;dbname=app;charset=utf8mb4', 'user', 'pass', [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');
$stmt->execute([$email]);
$user = $stmt->fetch();''')
add("Build a secure register and login in PHP.","Hash with password_hash, verify with password_verify, regenerate the session id after login.","php",r'''
<?php
// register
$hash = password_hash($password, PASSWORD_DEFAULT);
$pdo->prepare('INSERT INTO users (email, password_hash) VALUES (?, ?)')->execute([$email, $hash]);

// login
session_start();
$stmt = $pdo->prepare('SELECT id, password_hash FROM users WHERE email = ?');
$stmt->execute([$email]);
$u = $stmt->fetch();
if ($u && password_verify($password, $u['password_hash'])) {
    session_regenerate_id(true);
    $_SESSION['uid'] = $u['id'];
} else {
    http_response_code(401);
    echo 'Invalid credentials';
}''')
add("Write a JSON API endpoint in PHP.","Set the JSON header, read php://input, validate, return proper status codes.","php",r'''
<?php
header('Content-Type: application/json');
$in = json_decode(file_get_contents('php://input'), true) ?? [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($in['name'] ?? '');
    if ($name === '') {
        http_response_code(422);
        echo json_encode(['error' => 'name required']);
        exit;
    }
    echo json_encode(['ok' => true, 'name' => $name]);
}''')
add("Handle file uploads safely in PHP.","Check errors and size, detect MIME on the server, use a random name and an allow-list of types.","php",r'''
<?php
$f = $_FILES['file'] ?? null;
if (!$f || $f['error'] !== UPLOAD_ERR_OK) die('Upload failed');
if ($f['size'] > 2 * 1024 * 1024) die('Too large');
$mime = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']);
$ext = ['image/jpeg' => 'jpg', 'image/png' => 'png'][$mime] ?? die('Type not allowed');
move_uploaded_file($f['tmp_name'], __DIR__ . '/uploads/' . bin2hex(random_bytes(8)) . '.' . $ext);''')
add("How do I prevent XSS in PHP?","Escape output with htmlspecialchars in the right context.","php",r'''
<?php echo htmlspecialchars($input, ENT_QUOTES, 'UTF-8'); ?>''',"Escape on output, not on input. Also set a Content-Security-Policy header.")
add("Add CSRF protection to a PHP form.","Store a random token in the session, embed it in the form, compare with hash_equals.","php",r'''
<?php
session_start();
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
// in the form: <input type="hidden" name="csrf" value="<?= $_SESSION['csrf'] ?>">
if ($_SERVER['REQUEST_METHOD'] === 'POST'
    && !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(403);
    exit('Bad token');
}''')
add("Write a tiny router in PHP.","Parse the path, look it up in a route map, 404 otherwise.","php",r'''
<?php
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$routes = ['/' => 'home.php', '/about' => 'about.php'];
if (isset($routes[$path])) {
    require __DIR__ . '/' . $routes[$path];
} else {
    http_response_code(404);
    echo 'Not found';
}
''')
add("Set up Composer autoloading in PHP.","PSR-4 mapping in composer.json, then require vendor/autoload.php.","json",r'''
{
  "require": { "php": ">=8.1" },
  "autoload": { "psr-4": { "App\\": "src/" } }
}''',"Run `composer install`, then `require 'vendor/autoload.php';` and use `App\\Foo` for `src/Foo.php`.")

# ---------- SQL ----------
add("Create users and orders tables with a foreign key in SQL.","Primary keys, unique email, foreign key with cascade.","sql",r'''
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);''')
add("Write a SQL query for customers who spent more than 100 in total.","LEFT JOIN, GROUP BY user, HAVING on the aggregate.","sql",r'''
SELECT u.email, COUNT(o.id) AS orders, SUM(o.total) AS spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.email
HAVING SUM(o.total) > 100
ORDER BY spent DESC;''')
add("Get the top earner per department in SQL.","Rank within each department using a window function inside a CTE.","sql",r'''
WITH ranked AS (
  SELECT name, dept, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT name, dept, salary FROM ranked WHERE rnk = 1;''')
add("When should I add an index in SQL?","Indexes speed up filters, joins and sorts on a column but slow writes slightly.","sql",r'''
CREATE INDEX idx_orders_user ON orders(user_id);
EXPLAIN SELECT * FROM orders WHERE user_id = 42;''',"Index columns used in WHERE, JOIN and ORDER BY on big tables. Check with EXPLAIN.")
add("Transfer money between two accounts safely in SQL.","Both updates must succeed or neither, so use a transaction.","sql",r'''
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;''',"Check affected rows from the first update and `ROLLBACK` if it is 0.")
add("How do I do an upsert in SQL?","Syntax differs: MySQL uses ON DUPLICATE KEY, PostgreSQL uses ON CONFLICT.","sql",r'''
-- MySQL
INSERT INTO stats (user_id, hits) VALUES (1, 1)
ON DUPLICATE KEY UPDATE hits = hits + 1;

-- PostgreSQL
INSERT INTO stats (user_id, hits) VALUES (1, 1)
ON CONFLICT (user_id) DO UPDATE SET hits = stats.hits + 1;''')
add("Find the second highest salary in SQL.","Max of salaries below the overall max.","sql",r'''
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);''')
add("Paginate results in SQL.","LIMIT/OFFSET is simple; keyset pagination is faster on large tables.","sql",r'''
SELECT * FROM posts ORDER BY id DESC LIMIT 20 OFFSET 40;
-- keyset (faster): pass the last id you saw
SELECT * FROM posts WHERE id < 1234 ORDER BY id DESC LIMIT 20;''')

# ---------- GLSL ----------
add("Write a GLSL fragment shader with animated colors.","Use a time uniform and cosine palette over UV coordinates.","glsl",r'''
precision mediump float;
uniform float uTime;
varying vec2 vUv;
void main() {
  vec3 c = 0.5 + 0.5 * cos(uTime + vUv.xyx + vec3(0.0, 2.0, 4.0));
  gl_FragColor = vec4(c, 1.0);
}''')
add("Write GLSL for simple diffuse lighting.","Pass the normal from the vertex shader, dot it with the light direction, clamp at 0.","glsl",r'''
// vertex
varying vec3 vNormal;
void main() {
  vNormal = normalize(normalMatrix * normal);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
// fragment
precision mediump float;
varying vec3 vNormal;
uniform vec3 uLightDir;
void main() {
  float d = max(dot(normalize(vNormal), normalize(uLightDir)), 0.0);
  gl_FragColor = vec4(vec3(0.2) + vec3(0.8, 0.5, 0.3) * d, 1.0);
}''')
add("Write a GLSL vertex shader that makes a wave.","Offset position.y with a sine of x and time.","glsl",r'''
uniform float uTime;
void main() {
  vec3 p = position;
  p.y += sin(p.x * 3.0 + uTime) * 0.2;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}''')

# ---------- Unity / Godot / Blender ----------
add("Write a Unity C# first-person movement script.","CharacterController with input axes, gravity and isGrounded.","csharp",r'''
using UnityEngine;
[RequireComponent(typeof(CharacterController))]
public class Player : MonoBehaviour {
    public float speed = 6f, gravity = -20f;
    CharacterController cc; float vy;
    void Awake() => cc = GetComponent<CharacterController>();
    void Update() {
        var move = transform.right * Input.GetAxis("Horizontal") + transform.forward * Input.GetAxis("Vertical");
        vy = cc.isGrounded ? -1f : vy + gravity * Time.deltaTime;
        cc.Move((move * speed + Vector3.up * vy) * Time.deltaTime);
    }
}''')
add("Make a Unity hitscan shooting method.","Raycast forward from the camera and damage whatever has a Health component.","csharp",r'''
void Shoot() {
    if (Physics.Raycast(cam.transform.position, cam.transform.forward, out RaycastHit hit, 100f)) {
        if (hit.collider.TryGetComponent<Health>(out var h)) h.Damage(10);
    }
}''')
add("Spawn and destroy a prefab in Unity.","Instantiate with position and rotation; Destroy with a delay.","csharp",r'''
public GameObject prefab;
void Spawn(Vector3 pos) {
    var obj = Instantiate(prefab, pos, Quaternion.identity);
    Destroy(obj, 5f);
}''')
add("Add mouse look to a Godot 4 FPS camera.","Capture the mouse, rotate the body on Y and the camera on X, clamp pitch.","gdscript",r'''
extends Camera3D
@export var sens := 0.003
func _ready():
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
func _unhandled_input(e):
	if e is InputEventMouseMotion:
		get_parent().rotate_y(-e.relative.x * sens)
		rotate_x(-e.relative.y * sens)
		rotation.x = clamp(rotation.x, -1.5, 1.5)''')
add("Make a Godot 4 enemy chase the player.","Use NavigationAgent3D: set target, read next path point, move toward it.","gdscript",r'''
extends CharacterBody3D
@onready var agent: NavigationAgent3D = $NavigationAgent3D
@export var target: Node3D
const SPEED = 3.0
func _physics_process(_delta):
	agent.target_position = target.global_position
	var next = agent.get_next_path_position()
	velocity = (next - global_position).normalized() * SPEED
	move_and_slide()''')
add("Write a hitscan gun in Godot 4.","Cast a ray with the physics space state and call take_damage on the collider.","gdscript",r'''
func shoot():
	var space = get_world_3d().direct_space_state
	var to = global_position - global_transform.basis.z * 100.0
	var q = PhysicsRayQueryParameters3D.create(global_position, to)
	var hit = space.intersect_ray(q)
	if hit and hit.collider.has_method("take_damage"):
		hit.collider.take_damage(10)''')
add("Create a cube with a red material in Blender Python.","bpy: add primitive, create a node material, set Principled BSDF base color, assign it.","python",r'''
import bpy
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
obj = bpy.context.active_object
mat = bpy.data.materials.new("Red")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 0, 0, 1)
obj.data.materials.append(mat)
bpy.ops.export_scene.gltf(filepath="/tmp/cube.glb", export_format="GLB")''',"The last line exports a GLB that Three.js can load.")

# ---------- Kotlin / Android ----------
add("Model UI states in Kotlin with a sealed interface.","Sealed types make `when` exhaustive.","kotlin",r'''
sealed interface UiState<out T> {
    data object Loading : UiState<Nothing>
    data class Success<T>(val data: T) : UiState<T>
    data class Error(val message: String) : UiState<Nothing>
}
fun render(s: UiState<String>) = when (s) {
    is UiState.Loading -> "Loading"
    is UiState.Success -> s.data
    is UiState.Error -> s.message
}''')
add("Run two tasks in parallel with Kotlin coroutines.","Use async inside a coroutine scope and await both.","kotlin",r'''
import kotlinx.coroutines.*
suspend fun load(): String = withContext(Dispatchers.IO) { delay(500); "data" }
fun main() = runBlocking {
    val a = async { load() }
    val b = async { load() }
    println(a.await() + b.await())
}''')
add("Write an Android ViewModel with StateFlow.","Private mutable flow, public read-only StateFlow, update atomically.","kotlin",r'''
class MainViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    fun inc() { _count.update { it + 1 } }
}''')
add("Show a counter in Jetpack Compose using a ViewModel.","Collect the flow as state and call the ViewModel function from the button.","kotlin",r'''
@Composable
fun Counter(vm: MainViewModel = viewModel()) {
    val n by vm.count.collectAsState()
    Column(Modifier.padding(16.dp)) {
        Text("Count: $n")
        Button(onClick = vm::inc) { Text("Add") }
    }
}''')
add("Call a REST API with Retrofit in Kotlin.","Define a suspend interface, build Retrofit with a converter, create the service.","kotlin",r'''
data class User(val id: Int, val name: String)
interface Api { @GET("users/{id}") suspend fun user(@Path("id") id: Int): User }
val api: Api = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()
    .create(Api::class.java)''')
add("Define a Room entity and DAO in Kotlin.","Entity with primary key, DAO with suspend insert and Flow query, database class.","kotlin",r'''
@Entity data class Note(@PrimaryKey(autoGenerate = true) val id: Int = 0, val text: String)
@Dao interface NoteDao {
    @Insert suspend fun insert(n: Note)
    @Query("SELECT * FROM Note ORDER BY id DESC") fun all(): Flow<List<Note>>
}
@Database(entities = [Note::class], version = 1)
abstract class AppDb : RoomDatabase() { abstract fun notes(): NoteDao }''')
add("Explain Kotlin null safety with examples.","Nullable types need ?, safe call ?., elvis ?:, avoid !!.","kotlin",r'''
var name: String? = null
val len = name?.length ?: 0      // safe call + default
name?.let { println(it) }        // runs only if not null
fun String.shout() = uppercase() + "!"   // extension function''',"Avoid `!!` because it throws a NullPointerException.")

# ---------- Gradle ----------
add("Write an Android app/build.gradle.kts with Kotlin and Compose.","Plugins, android block with SDK versions, Java 17, compose options, dependencies.","kotlin",r'''
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.example.app"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.8" }
}
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}''',"The Compose compiler version must match your Kotlin version (1.5.8 pairs with Kotlin 1.9.22). With Kotlin 2.0+, use the Compose compiler Gradle plugin instead.")
add("Write settings.gradle.kts for an Android project.","Plugin and dependency repositories, project name, included modules.","kotlin",r'''
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "MyApp"
include(":app")''')
add("Use a Gradle version catalog (libs.versions.toml).","Central place for versions; reference with libs.* in build files.","toml",r'''
[versions]
kotlin = "1.9.22"
coroutines = "1.8.0"

[libraries]
coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }''',"Put it in `gradle/libs.versions.toml`, then use `implementation(libs.coroutines.core)` and `alias(libs.plugins.kotlin.jvm)`.")
add("Write a build.gradle.kts for a Kotlin JVM command-line app.","Kotlin JVM plugin, application plugin with main class, JVM toolchain.","kotlin",r'''
plugins {
    kotlin("jvm") version "1.9.22"
    application
}
repositories { mavenCentral() }
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
    testImplementation(kotlin("test"))
}
kotlin { jvmToolchain(17) }
application { mainClass.set("MainKt") }''',"Run with `./gradlew run`.")
add("What are the most useful Gradle commands?","List the common wrapper tasks and when to use them.","bash",r'''
./gradlew assembleDebug            # build debug APK
./gradlew assembleRelease          # build release APK
./gradlew bundleRelease            # build AAB for Play Store
./gradlew test                     # run unit tests
./gradlew clean                    # delete build outputs
./gradlew dependencies             # print dependency tree
./gradlew build --refresh-dependencies --stacktrace''')
add("Set up release signing in Gradle without committing secrets.","Read the keystore data from gradle.properties or environment variables, never hardcode.","kotlin",r'''
android {
    signingConfigs {
        create("release") {
            storeFile = file(providers.gradleProperty("KEYSTORE_FILE").get())
            storePassword = providers.gradleProperty("KEYSTORE_PASSWORD").get()
            keyAlias = providers.gradleProperty("KEY_ALIAS").get()
            keyPassword = providers.gradleProperty("KEY_PASSWORD").get()
        }
    }
    buildTypes { release { signingConfig = signingConfigs.getByName("release") } }
}''',"Keep the values in `~/.gradle/gradle.properties`, not in the repo.")
add("Gradle error: 'Could not resolve' a dependency. How do I fix it?","Usual causes: missing repository, wrong coordinates or version, no internet, offline mode.","text",r'''
1. Check repositories: google() and mavenCentral() in settings.gradle.kts
2. Check the group:artifact:version spelling and that the version exists
3. Turn off Offline Mode (Android Studio: Settings > Build > Gradle)
4. Retry: ./gradlew build --refresh-dependencies
5. Behind a proxy? Set it in gradle.properties''')
add("Gradle error: 'Unsupported class file major version'. What does it mean?","Gradle or a plugin is running on a different Java version than it supports.","text",r'''
Cause: the JDK running Gradle is newer/older than your Gradle version supports.
Fix:
- Android Studio: Settings > Build > Gradle > Gradle JDK = 17
- Or set org.gradle.java.home in gradle.properties
- Or upgrade the Gradle wrapper: ./gradlew wrapper --gradle-version 8.5''')

old = [json.loads(x) for x in open("zorn_data.jsonl")]
seen = {r["question"] for r in old}
R = [r for r in R if r["question"] not in seen]
allr = old + R
random.shuffle(allr)
with open("zorn_data.jsonl", "w") as f:
    for r in allr: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(R), "added; total", len(allr))
