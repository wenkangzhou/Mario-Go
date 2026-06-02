extends Node2D

const CELL_SIZE = 40.0

var score = 0
var points = 0
var lives = 3
var time_left = 400.0
var score_label: Label
var points_label: Label
var lives_label: Label
var time_label: Label
var victory_label: Label
var audio_player: AudioStreamPlayer
var bgm_player: AudioStreamPlayer
var sfx = {}
var fireball_count = 0
var game_over = false
var paused = false
var title_active = false

var fade_rect: ColorRect
const FADE_DURATION = 0.25

var stomp_combo = 0
var stomp_combo_timer = 0.0
const STOMP_SCORES = [100, 200, 400, 800, 1000, 2000, 4000, 8000]

var current_level = ""

const LEVEL_WIDTH = 160

var level_map = []

func build_level_1_1():
	for i in range(16):
		level_map.append(" ".repeat(LEVEL_WIDTH))

	# 基础地面（row 13 草皮，row 14-15 土壤）
	for c in range(LEVEL_WIDTH):
		set_map(13, c, "G")
		set_map(14, c, "D")
		set_map(15, c, "D")

	# 开场砖块区 row8
	set_map(8, 10, "B")
	set_map(8, 11, "B")
	set_map(8, 12, "R")
	set_map(8, 14, "Q")
	set_map(8, 16, "B")
	set_map(8, 17, "B")
	set_map(8, 18, "B")
	set_map(8, 20, "Q")
	set_map(8, 21, "B")
	set_map(8, 22, "B")
	set_map(8, 23, "B")
	set_map(8, 24, "B")
	set_map(8, 25, "B")

	# 第一个敌人
	set_map(10, 28, "E")

	# 水管1（通往1-2的传送水管）
	build_pipe(36, 3)
	set_map(11, 36, "W")

	# 金币
	set_map(8, 48, "C")
	set_map(8, 49, "C")
	set_map(8, 50, "C")
	set_map(10, 55, "C")
	set_map(10, 56, "C")

	# 敌人
	set_map(10, 62, "E")

	# 水管2
	build_pipe(70, 3)

	# 敌人
	set_map(10, 82, "E")

	# 坑洞1
	for c in range(90, 97):
		set_map(13, c, " ")
		set_map(14, c, " ")
		set_map(15, c, " ")

	# 多层平台
	set_map(8, 105, "B")
	set_map(8, 106, "R")
	set_map(8, 107, "B")
	set_map(8, 108, "B")
	set_map(8, 109, "B")
	set_map(8, 110, "Q")
	set_map(8, 111, "B")
	set_map(8, 112, "B")
	set_map(8, 113, "B")
	set_map(8, 114, "B")

	# 敌人
	set_map(10, 100, "E")
	set_map(10, 116, "E")

	# 水管3
	build_pipe(125, 3)

	# 乌龟（移到水管2和金币区之间，更容易看到）
	set_map(10, 72, "K")

	# 坑洞2
	for c in range(128, 133):
		set_map(13, c, " ")
		set_map(14, c, " ")
		set_map(15, c, " ")

	# 台阶（6级，更高）
	set_map(13, 138, "B")
	set_map(12, 139, "B"); set_map(13, 139, "B")
	set_map(11, 140, "B"); set_map(12, 140, "B"); set_map(13, 140, "B")
	set_map(10, 141, "B"); set_map(11, 141, "B"); set_map(12, 141, "B"); set_map(13, 141, "B")
	set_map(9, 142, "B"); set_map(10, 142, "B"); set_map(11, 142, "B"); set_map(12, 142, "B"); set_map(13, 142, "B")
	set_map(8, 143, "B"); set_map(9, 143, "B"); set_map(10, 143, "B"); set_map(11, 143, "B"); set_map(12, 143, "B"); set_map(13, 143, "B")

	# 旗杆
	set_map(8, 148, "F")

	# 城堡
	set_map(11, 152, "A")

func build_level_1_2():
	for i in range(16):
		level_map.append(" ".repeat(LEVEL_WIDTH))

	# 底部天台地面（120列）
	for c in range(120):
		set_map(13, c, "T")
		set_map(14, c, "T")
		set_map(15, c, "T")

	# === Area 1: 起点（cols 0-12）===
	set_map(12, 2, "A")
	set_map(12, 6, "A")
	set_map(12, 10, "R")
	set_map(10, 8, "M")

	# === Area 2: 教学平台（cols 15-28）===
	for c in [16, 18, 20]:
		set_map(11, c, "T")
	set_map(10, 18, "w")
	for c in [24, 26, 28]:
		set_map(10, c, "T")
	set_map(9, 26, "I")
	set_map(10, 30, "t")

	# === Area 3: 初次跳跃（cols 32-48）===
	for c in [33, 35, 37]:
		set_map(9, c, "T")
	set_map(8, 35, "M")
	for c in [42, 44, 46, 48]:
		set_map(11, c, "T")
	set_map(10, 45, "t")
	set_map(12, 40, "R")
	set_map(12, 48, "R")

	# === Area 4: 高空平台（cols 52-74）===
	for c in [52, 54, 56]:
		set_map(8, c, "T")
	set_map(7, 54, "w")
	for c in [60, 62, 64, 66]:
		set_map(10, c, "T")
	set_map(9, 63, "t")
	set_map(9, 66, "t")
	for c in [70, 72, 74]:
		set_map(7, c, "T")
	set_map(6, 72, "I")
	set_map(12, 58, "A")
	set_map(12, 68, "A")

	# === Area 5: 天台跑道（cols 76-92）===
	for c in [78, 82, 86, 90]:
		set_map(12, c, "R")
	set_map(10, 80, "t")
	set_map(10, 88, "t")
	set_map(12, 85, "w")
	set_map(12, 89, "M")
	for c in [76, 79, 82]:
		set_map(11, c, "T")
	for c in [84, 87, 90]:
		set_map(9, c, "T")

	# === Area 6: 终点攀爬（cols 94-108）===
	for c in [94, 96]:
		set_map(11, c, "T")
	for c in [98, 100]:
		set_map(9, c, "T")
	for c in [102, 104, 106]:
		set_map(7, c, "T")
	set_map(6, 104, "I")
	set_map(10, 97, "t")

	# === Area 7: 出口（cols 110-115）===
	for c in [110, 111, 112, 113]:
		set_map(12, c, "T")
		set_map(13, c, "T")
	set_map(13, 112, "W")
	for c in [110, 111, 113]:
		set_map(12, c, "R")

func set_map(row: int, col: int, ch: String):
	if row < 0 or row >= level_map.size() or col < 0 or col >= LEVEL_WIDTH:
		return
	var line = level_map[row]
	level_map[row] = line.substr(0, col) + ch + line.substr(col + 1)

func build_pipe(start_col: int, height: int):
	for r in range(14 - height, 14):
		set_map(r, start_col, "P")

func _ready():
	# ===== 分数显示 =====
	var canvas = CanvasLayer.new()
	score_label = Label.new()
	score_label.position = Vector2(20, 20)
	score_label.text = "金币: 0"
	score_label.add_theme_font_size_override("font_size", 20)
	canvas.add_child(score_label)

	lives_label = Label.new()
	lives_label.position = Vector2(20, 50)
	lives_label.text = "生命: 3"
	lives_label.add_theme_font_size_override("font_size", 20)
	canvas.add_child(lives_label)

	time_label = Label.new()
	time_label.position = Vector2(160, 20)
	time_label.text = "时间: 400"
	time_label.add_theme_font_size_override("font_size", 20)
	canvas.add_child(time_label)

	points_label = Label.new()
	points_label.position = Vector2(300, 20)
	points_label.text = "分数: 0"
	points_label.add_theme_font_size_override("font_size", 20)
	canvas.add_child(points_label)

	victory_label = Label.new()
	victory_label.position = Vector2(450, 300)
	victory_label.text = "通关！"
	victory_label.visible = false
	victory_label.add_theme_font_size_override("font_size", 32)
	canvas.add_child(victory_label)

	# Fade overlay
	fade_rect = ColorRect.new()
	fade_rect.color = Color(0, 0, 0, 0)
	fade_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	fade_rect.z_index = 100
	canvas.add_child(fade_rect)

	add_child(canvas)

	# ===== 音效 =====
	audio_player = AudioStreamPlayer.new()
	add_child(audio_player)
	sfx["jump"] = load("res://jump.wav")
	sfx["coin"] = load("res://coin.wav")
	sfx["stomp"] = load("res://stomp.wav")
	sfx["hurt"] = load("res://hurt.wav")
	sfx["win"] = load("res://win.wav")
	sfx["pipe"] = load("res://pipe.wav")

	bgm_player = AudioStreamPlayer.new()
	add_child(bgm_player)

	# ===== 创建玩家 =====
	var player_body = CharacterBody2D.new()
	player_body.name = "Player"
	player_body.position = Vector2(100, 300)

	var player_col = CollisionShape2D.new()
	player_col.name = "CollisionShape2D"
	var player_shape = RectangleShape2D.new()
	player_shape.size = Vector2(40, 60)
	player_col.shape = player_shape
	player_body.add_child(player_col)

	var player_visual = Sprite2D.new()
	player_visual.name = "Sprite2D"
	player_visual.texture = load("res://player.png")
	player_body.add_child(player_visual)

	var camera = Camera2D.new()
	camera.position = Vector2(0, -50)
	camera.limit_bottom = 700
	camera.limit_top = -100
	camera.limit_left = 0
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 10.0
	player_body.add_child(camera)

	player_body.set_script(load("res://player.gd"))
	add_child(player_body)

	show_title_screen()

func show_title_screen():
	title_active = true
	RenderingServer.set_default_clear_color(Color(0.08, 0.06, 0.1))
	if has_node("Player"):
		$Player.visible = false

	var title = Label.new()
	title.name = "TitleLabel"
	title.text = "流浪的夏天"
	title.position = Vector2(280, 200)
	title.modulate.a = 0.0
	title.add_theme_font_size_override("font_size", 56)
	add_child(title)

	var sub = Label.new()
	sub.name = "SubLabel"
	sub.text = "Wandering Summer"
	sub.position = Vector2(310, 270)
	sub.modulate.a = 0.0
	sub.add_theme_font_size_override("font_size", 22)
	add_child(sub)

	var hint = Label.new()
	hint.name = "HintLabel"
	hint.text = "按任意键开始"
	hint.position = Vector2(340, 350)
	hint.modulate.a = 0.0
	hint.add_theme_font_size_override("font_size", 18)
	add_child(hint)

	var tw = create_tween()
	tw.tween_property(title, "modulate:a", 1.0, 1.0)
	tw.parallel().tween_property(sub, "modulate:a", 1.0, 1.0)
	tw.tween_property(hint, "modulate:a", 1.0, 0.5)

	var blink = hint.create_tween()
	blink.set_loops()
	blink.tween_property(hint, "modulate:a", 0.3, 0.6)
	blink.tween_property(hint, "modulate:a", 1.0, 0.6)

func start_game():
	title_active = false
	for n in ["TitleLabel", "SubLabel", "HintLabel"]:
		if has_node(n):
			get_node(n).queue_free()
	load_level("1-1")

func show_tutorial_hint(pos: Vector2, text: String):
	var hint = Label.new()
	hint.text = text
	hint.position = pos
	hint.modulate.a = 0.0
	hint.add_theme_font_size_override("font_size", 16)
	add_child(hint)
	var tw = create_tween()
	tw.tween_property(hint, "modulate:a", 1.0, 0.5)
	tw.tween_interval(2.5)
	tw.tween_property(hint, "modulate:a", 0.0, 0.5)
	tw.tween_callback(hint.queue_free)

func play_sfx(name: String):
	audio_player.stream = sfx[name]
	audio_player.play()

func _unhandled_input(event: InputEvent) -> void:
	if title_active:
		if event is InputEventKey or event is InputEventJoypadButton:
			if event.pressed and not event.is_echo():
				start_game()
		return
	if event.is_action_pressed("ui_cancel"):
		paused = not paused
		get_tree().paused = paused

func _process(delta: float) -> void:
	if game_over:
		return
	if has_node("Player"):
		var player = $Player
		if player.is_finishing or player.is_dying or player.is_entering_pipe:
			time_label.text = "时间: " + str(int(time_left))
			return
	time_left -= delta
	if time_left <= 0:
		time_left = 0
		lose_life()
		time_left = 400.0
	time_label.text = "时间: " + str(int(time_left))

	# 连击计时器
	if stomp_combo_timer > 0:
		stomp_combo_timer -= delta
		if stomp_combo_timer <= 0:
			stomp_combo = 0

func show_victory():
	bgm_player.stop()
	victory_label.visible = true
	await get_tree().create_timer(3.0).timeout
	get_tree().reload_current_scene()

func lose_life():
	lives -= 1
	lives_label.text = "生命: " + str(lives)
	if lives <= 0:
		game_over = true
		victory_label.text = "游戏结束"
		victory_label.visible = true
		await get_tree().create_timer(2.0).timeout
		get_tree().reload_current_scene()

func refresh_score_label():
	if current_level == "1-2":
		score_label.text = "收集: " + str(score)
	else:
		score_label.text = "金币: " + str(score)

func add_score(amount = 1):
	score += amount
	refresh_score_label()
	if score >= 100:
		score -= 100
		refresh_score_label()
		add_life()
		play_sfx("coin")

func add_life():
	lives += 1
	lives_label.text = "生命: " + str(lives)

func add_points(amount: int):
	points += amount
	points_label.text = "分数: " + str(points)

func create_landing_dust(pos: Vector2):
	var particles = CPUParticles2D.new()
	particles.position = pos + Vector2(0, 28)
	particles.emitting = true
	particles.one_shot = true
	particles.amount = 5
	particles.lifetime = 0.25
	particles.direction = Vector2(0, -1)
	particles.spread = 70.0
	particles.gravity = Vector2(0, 150)
	particles.initial_velocity_min = 20.0
	particles.initial_velocity_max = 60.0
	particles.scale_amount_min = 1.0
	particles.scale_amount_max = 2.5
	particles.color = Color(0.75, 0.75, 0.78, 0.35)
	add_child(particles)
	var timer = get_tree().create_timer(0.4)
	timer.timeout.connect(func(): particles.queue_free())

func create_run_dust(pos: Vector2, facing_left: bool):
	var particles = CPUParticles2D.new()
	particles.position = pos + Vector2(12 if facing_left else -12, 28)
	particles.emitting = true
	particles.one_shot = true
	particles.amount = 2
	particles.lifetime = 0.18
	particles.direction = Vector2(0, -1)
	particles.spread = 40.0
	particles.gravity = Vector2(0, 100)
	particles.initial_velocity_min = 10.0
	particles.initial_velocity_max = 30.0
	particles.scale_amount_min = 0.5
	particles.scale_amount_max = 1.5
	particles.color = Color(0.7, 0.7, 0.73, 0.25)
	add_child(particles)
	var timer = get_tree().create_timer(0.25)
	timer.timeout.connect(func(): particles.queue_free())

func shake_camera(intensity: float, duration: float):
	if has_node("Player/Camera2D"):
		var cam = $Player/Camera2D
		var tween = create_tween()
		var original = cam.offset
		var shakes = int(duration * 12)
		for i in range(shakes):
			var offset = Vector2(randf() * intensity * 2 - intensity, randf() * intensity * 2 - intensity)
			tween.tween_property(cam, "offset", original + offset, 0.04)
		tween.tween_property(cam, "offset", original, 0.04)

func flash_damage():
	fade_rect.color = Color(0.9, 0.15, 0.15, 0.25)
	var tween = create_tween()
	tween.tween_property(fade_rect, "color:a", 0.0, 0.25)

func show_level_title(text: String):
	var label = Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", 36)
	label.position = Vector2(380, 260)
	label.modulate.a = 0.0
	add_child(label)
	var tween = create_tween()
	tween.tween_property(label, "modulate:a", 1.0, 0.5)
	tween.tween_interval(1.8)
	tween.tween_property(label, "modulate:a", 0.0, 0.5)
	tween.tween_callback(label.queue_free)

func create_floating_text(pos: Vector2, text: String):
	var label = Label.new()
	label.text = text
	label.position = pos
	label.add_theme_font_size_override("font_size", 16)
	add_child(label)
	var tween = create_tween()
	tween.tween_property(label, "position:y", pos.y - 50, 0.6)
	tween.parallel().tween_property(label, "modulate:a", 0.0, 0.6)
	tween.tween_callback(label.queue_free)

func add_stomp_score(pos: Vector2):
	stomp_combo += 1
	stomp_combo_timer = 1.5
	var amount = STOMP_SCORES[min(stomp_combo - 1, 7)]
	add_points(amount)
	if stomp_combo >= 9:
		create_floating_text(pos, "1UP")
		add_life()
	else:
		create_floating_text(pos, "+" + str(amount))

func add_time_bonus():
	var bonus = int(time_left) * 50
	add_points(bonus)
	time_left = 0

func create_tile(pos: Vector2, texture_path: String, tile_name: String = "", script_path: String = ""):
	var body = StaticBody2D.new()
	body.position = pos
	if tile_name != "":
		body.name = tile_name
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(CELL_SIZE, CELL_SIZE)
	col.shape = shape
	body.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load(texture_path)
	body.add_child(visual)
	if script_path != "":
		body.set_script(load(script_path))
		body.add_to_group("hittable")
	add_child(body)
	return body

func create_enemy(pos: Vector2, patrol_width: float):
	var enemy = CharacterBody2D.new()
	enemy.name = "Enemy"
	enemy.position = pos
	enemy.add_to_group("enemy")
	var col = CollisionShape2D.new()
	col.name = "CollisionShape2D"
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	enemy.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://enemy.png")
	enemy.add_child(visual)
	enemy.set_meta("patrol_width", patrol_width)
	enemy.set_script(load("res://enemy.gd"))
	add_child(enemy)

func create_coin(pos: Vector2, bouncing: bool = false):
	var coin = Area2D.new()
	coin.position = pos
	var col = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = 10
	col.shape = shape
	coin.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://coin.png")
	coin.add_child(visual)
	coin.set_meta("bouncing", bouncing)
	coin.set_script(load("res://coin.gd"))
	add_child(coin)

func create_mushroom(pos: Vector2, is_1up: bool = false):
	var mush = CharacterBody2D.new()
	mush.position = pos
	mush.add_to_group("mushroom")
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	mush.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	if is_1up:
		visual.texture = load("res://1up.png")
	else:
		visual.texture = load("res://mushroom.png")
	mush.add_child(visual)
	mush.set_meta("is_1up", is_1up)
	mush.set_script(load("res://mushroom.gd"))
	add_child(mush)

func create_flower(pos: Vector2):
	var flower = Area2D.new()
	flower.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	flower.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://flower.png")
	flower.add_child(visual)
	flower.set_script(load("res://flower.gd"))
	add_child(flower)

func create_fireball(pos: Vector2, dir: int):
	if fireball_count >= 2:
		return
	fireball_count += 1
	var ball = CharacterBody2D.new()
	ball.position = pos
	var col = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = 8
	col.shape = shape
	ball.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://fireball.png")
	ball.add_child(visual)
	ball.set_meta("direction", dir)
	ball.set_script(load("res://fireball.gd"))
	add_child(ball)

func create_piranha(pos: Vector2):
	var p = Area2D.new()
	p.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 50)
	col.shape = shape
	p.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://piranha.png")
	p.add_child(visual)
	p.set_script(load("res://piranha.gd"))
	add_child(p)

func create_goal(pos: Vector2):
	var goal = Area2D.new()
	goal.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(60, 360)
	col.shape = shape
	goal.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://goal.png")
	goal.add_child(visual)
	goal.set_script(load("res://goal.gd"))
	add_child(goal)

	var flag = Sprite2D.new()
	flag.name = "Flag"
	flag.texture = load("res://flag.png")
	flag.position = Vector2(pos.x + 14, pos.y - 140)
	flag.z_index = 1
	add_child(flag)
	goal.set_meta("flag_node", flag)

	# 物理阻挡墙（薄墙位于旗杆上方，防止跳过但不阻挡地面通行）
	var wall = StaticBody2D.new()
	wall.position = Vector2(pos.x, pos.y - 280)
	var wall_col = CollisionShape2D.new()
	var wall_shape = RectangleShape2D.new()
	wall_shape.size = Vector2(20, 400)
	wall_col.shape = wall_shape
	wall.add_child(wall_col)
	add_child(wall)

func create_koopa(pos: Vector2):
	var koopa = CharacterBody2D.new()
	koopa.name = "Koopa"
	koopa.position = pos
	koopa.add_to_group("enemy")
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 40)
	col.shape = shape
	koopa.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://koopa.png")
	koopa.add_child(visual)
	koopa.set_meta("start_dir", -1)
	koopa.set_script(load("res://koopa.gd"))
	add_child(koopa)

func create_star(pos: Vector2):
	var star = CharacterBody2D.new()
	star.position = pos
	var col = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = 6
	col.shape = shape
	star.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://star.png")
	star.add_child(visual)
	star.add_to_group("star")
	star.set_script(load("res://star.gd"))
	add_child(star)

func create_castle(pos: Vector2):
	var castle = StaticBody2D.new()
	castle.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(120, 120)
	col.shape = shape
	castle.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://castle.png")
	castle.add_child(visual)
	add_child(castle)

func create_cat(pos: Vector2):
	var cat = CharacterBody2D.new()
	cat.name = "Cat"
	cat.position = pos
	cat.add_to_group("enemy")
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	cat.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	visual.texture = load("res://cat.png")
	cat.add_child(visual)
	var detect = Area2D.new()
	detect.name = "DetectionArea"
	var detect_col = CollisionShape2D.new()
	var detect_shape = CircleShape2D.new()
	detect_shape.radius = 150
	detect_col.shape = detect_shape
	detect.add_child(detect_col)
	cat.add_child(detect)
	cat.set_meta("patrol_width", 80.0)
	cat.set_script(load("res://cat.gd"))
	add_child(cat)

func create_collectible(pos: Vector2, type: String):
	var item = Area2D.new()
	item.position = pos
	item.add_to_group("collectible")
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	if type == "watermelon":
		shape.size = Vector2(25, 25)
	elif type == "ice_cream":
		shape.size = Vector2(15, 35)
	else:
		shape.size = Vector2(25, 15)
	col.shape = shape
	item.add_child(col)
	var visual = Sprite2D.new()
	visual.name = "Sprite2D"
	match type:
		"watermelon": visual.texture = load("res://watermelon.png")
		"ice_cream": visual.texture = load("res://ice_cream.png")
		"tape": visual.texture = load("res://tape.png")
	item.add_child(visual)
	item.set_meta("collectible_type", type)
	item.set_script(load("res://collectible.gd"))
	add_child(item)

func create_decoration(pos: Vector2, type: String):
	var dec = Sprite2D.new()
	dec.position = pos
	dec.z_index = -1
	match type:
		"ac": dec.texture = load("res://ac_unit.png")
		"railing": dec.texture = load("res://railing.png")
	add_child(dec)

func create_clothesline(pos: Vector2):
	var body = StaticBody2D.new()
	body.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(100, 6)
	col.shape = shape
	col.one_way_collision = true
	body.add_child(col)
	var visual = Sprite2D.new()
	visual.texture = load("res://clothesline.png")
	body.add_child(visual)
	add_child(body)

func create_antenna(pos: Vector2):
	var body = StaticBody2D.new()
	body.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(8, 70)
	col.shape = shape
	body.add_child(col)
	var visual = Sprite2D.new()
	visual.texture = load("res://antenna.png")
	body.add_child(visual)
	add_child(body)

func create_bird(pos: Vector2):
	var bird = Sprite2D.new()
	bird.texture = load("res://bird.png")
	bird.position = pos
	bird.z_index = -1
	bird.modulate = Color(0.35, 0.32, 0.4)
	add_child(bird)
	var tween = bird.create_tween()
	var duration = 10.0 + randf() * 5.0
	var drift = (randf() - 0.5) * 80
	tween.tween_property(bird, "position:x", pos.x - 900, duration)
	tween.parallel().tween_property(bird, "position:y", pos.y + drift, duration)
	tween.tween_callback(bird.queue_free)

func create_moving_platform(pos: Vector2, distance: float, speed: float = 35.0):
	var body = AnimatableBody2D.new()
	body.position = pos
	body.sync_to_physics = true
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(80, 10)
	col.shape = shape
	body.add_child(col)
	var visual = Sprite2D.new()
	visual.texture = load("res://rooftop_tile.png")
	body.add_child(visual)
	var tween = body.create_tween()
	tween.set_loops()
	tween.tween_property(body, "position:x", pos.x + distance, distance / speed)
	tween.tween_property(body, "position:x", pos.x, distance / speed)
	add_child(body)

func create_sunset_particles():
	var particles = CPUParticles2D.new()
	particles.position = Vector2(2400, 600)
	particles.amount = 40
	particles.lifetime = 5.0
	particles.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	particles.emission_rect_extents = Vector2(3000, 200)
	particles.direction = Vector2(0, -1)
	particles.spread = 30.0
	particles.gravity = Vector2(0, -5)
	particles.initial_velocity_min = 5.0
	particles.initial_velocity_max = 20.0
	particles.scale_amount_min = 1.0
	particles.scale_amount_max = 3.0
	particles.color = Color(1.0, 0.55, 0.15, 0.35)
	add_child(particles)

func create_checkpoint(pos: Vector2):
	var cp = Area2D.new()
	cp.name = "Checkpoint"
	cp.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 40)
	col.shape = shape
	cp.add_child(col)
	var visual = Sprite2D.new()
	visual.texture = load("res://checkpoint.png")
	cp.add_child(visual)
	cp.body_entered.connect(func(body):
		if body.name == "Player" and body.start_pos != pos:
			body.start_pos = pos
			play_sfx("coin")
			create_floating_text(pos + Vector2(0, -30), "已存档!")
			var tw = visual.create_tween()
			tw.tween_property(visual, "modulate", Color(2, 2, 2), 0.1)
			tw.tween_property(visual, "modulate", Color(1, 1, 1), 0.2)
	)
	add_child(cp)

func create_watertower(pos: Vector2):
	var tower = Area2D.new()
	tower.name = "WaterTower"
	tower.position = pos
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(50, 80)
	col.shape = shape
	tower.add_child(col)
	var visual = Sprite2D.new()
	visual.texture = load("res://watertower.png")
	tower.add_child(visual)
	tower.body_entered.connect(_on_watertower_entered)
	add_child(tower)

func _on_watertower_entered(body: Node2D):
	if body.name != "Player" or body.is_finishing:
		return
	body.is_finishing = true
	body.velocity = Vector2.ZERO
	_play_ending_sequence(body)

func _play_ending_sequence(player):
	bgm_player.stop()
	play_sfx("win")
	# Auto-walk to the right edge
	var walk_tween = create_tween()
	walk_tween.tween_property(player, "position:x", player.position.x + 120, 2.5)
	await walk_tween.finished
	# Ending text
	var label = Label.new()
	label.text = "明天见"
	label.position = player.position + Vector2(-50, -120)
	label.modulate.a = 0.0
	label.add_theme_font_size_override("font_size", 48)
	add_child(label)
	var lt = label.create_tween()
	lt.tween_property(label, "modulate:a", 1.0, 0.5)
	lt.parallel().tween_property(label, "position:y", label.position.y - 20, 2.0)
	# Celebration fireworks
	for i in range(3):
		create_firework(player.position + Vector2(randf() * 100 - 50, -80 - randf() * 40))
		await get_tree().create_timer(0.5).timeout
	lt.tween_property(label, "modulate:a", 0.0, 0.5)
	lt.tween_callback(label.queue_free)
	await get_tree().create_timer(0.8).timeout
	# Fade out and return to 1-1
	var tw = fade_out()
	await tw.finished
	load_level("1-1")
	fade_in()

func create_firework(pos: Vector2):
	var colors = [Color(1, 0.2, 0.2), Color(0.2, 1, 0.2), Color(0.2, 0.4, 1), Color(1, 1, 0.2), Color(1, 0.5, 0.2)]
	var color = colors[randi() % colors.size()]
	for i in range(12):
		var p = Sprite2D.new()
		p.texture = load("res://fireball.png")
		p.modulate = color
		p.position = pos
		add_child(p)
		var angle = i * PI / 6
		var dist = 60 + randi() % 40
		var target = pos + Vector2(cos(angle), sin(angle)) * dist
		var tween = p.create_tween()
		tween.tween_property(p, "position", target, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tween.parallel().tween_property(p, "modulate:a", 0.0, 0.6)
		tween.tween_callback(p.queue_free)
	play_sfx("coin")

func fade_out() -> Tween:
	var tween = create_tween()
	tween.tween_property(fade_rect, "color:a", 1.0, FADE_DURATION)
	return tween

func fade_in():
	var tween = create_tween()
	tween.tween_property(fade_rect, "color:a", 0.0, FADE_DURATION)

func clear_level():
	for child in get_children():
		if child.name == "Player" or child is CanvasLayer or child is AudioStreamPlayer:
			continue
		child.queue_free()

func load_level(level_name: String):
	current_level = level_name
	clear_level()
	level_map.clear()

	if level_name == "1-1":
		build_level_1_1()
		RenderingServer.set_default_clear_color(Color(0.35, 0.55, 0.95))
		bgm_player.stream = load("res://bgm.wav")
		bgm_player.stream.loop_mode = 1
	elif level_name == "1-2":
		build_level_1_2()
		RenderingServer.set_default_clear_color(Color(0.15, 0.12, 0.18))
		bgm_player.stream = load("res://summer_bgm.wav")
		bgm_player.stream.loop_mode = 1
	bgm_player.play()

	if has_node("Player"):
		var player = $Player
		player.is_entering_pipe = false
		player.pipe_timer = 0
		player.velocity = Vector2.ZERO
		player.is_dying = false
		player.is_finishing = false
		player.invincible = false
		player.visible = true
		if level_name == "1-1":
			player.position = Vector2(100, 300)
			player.start_pos = Vector2(100, 300)
		elif level_name == "1-2":
			player.reset_size()
			player.position = Vector2(3 * CELL_SIZE + CELL_SIZE / 2, 9 * CELL_SIZE + CELL_SIZE / 2)
			player.start_pos = Vector2(3 * CELL_SIZE + CELL_SIZE / 2, 9 * CELL_SIZE + CELL_SIZE / 2)
		if has_node("Player/Camera2D"):
			var cam = $Player/Camera2D
			if level_name == "1-1":
				cam.position = Vector2(0, -50)
				cam.limit_right = 160 * CELL_SIZE
			else:
				cam.position = Vector2(0, -80)
				cam.limit_right = 120 * CELL_SIZE

	spawn_level()

	if level_name == "1-2":
		show_level_title("1-2  流浪的夏天")
		get_tree().create_timer(1.5).timeout.connect(func(): show_tutorial_hint(Vector2(5 * CELL_SIZE + CELL_SIZE / 2, 8 * CELL_SIZE), "↑跳跃  ← →移动"))

func spawn_level():
	for row in range(level_map.size()):
		for col in range(level_map[row].length()):
			var ch = level_map[row][col]
			var x = col * CELL_SIZE + CELL_SIZE / 2
			var y = row * CELL_SIZE + CELL_SIZE / 2
			match ch:
				'G': create_tile(Vector2(x, y), "res://ground.png")
				'D': create_tile(Vector2(x, y), "res://ground_inner.png")
				'B': create_tile(Vector2(x, y), "res://brick.png", "Brick", "res://brick.gd")
				'Q':
					var q = create_tile(Vector2(x, y), "res://question.png", "QuestionBlock", "res://question_block.gd")
					if current_level == "1-1":
						if col == 14:
							q.content = "mushroom"
						elif col == 20:
							q.content = "flower"
						elif col == 110:
							q.content = "star"
						elif col == 111:
							q.content = "1up"
						else:
							q.content = "coin"
					else:
						q.content = "coin"
				'R':
					if current_level == "1-2":
						create_decoration(Vector2(x, y), "railing")
					else:
						var r = create_tile(Vector2(x, y), "res://brick.png", "MultiBrick", "res://question_block.gd")
						r.content = "coin"
						r.coin_count = 10
				'P':
					var p = create_tile(Vector2(x, y), "res://pipe.png")
					p.add_to_group("pipe")
				'W':
					var w = create_tile(Vector2(x, y), "res://pipe.png")
					w.add_to_group("pipe")
					w.add_to_group("warp_pipe")
					if current_level == "1-1" and col == 36:
						w.set_meta("destination", "1-2")
					elif current_level == "1-2" and col == 112:
						w.set_meta("destination", "1-1")
					else:
						w.set_meta("destination", "bonus")
				'w': create_collectible(Vector2(x, y), "watermelon")
				'E': create_enemy(Vector2(x, y - 15), 80.0)
				'K': create_koopa(Vector2(x, y - 15))
				'C': create_coin(Vector2(x, y))
				'F': create_goal(Vector2(x, y))
				'A':
					if current_level == "1-2":
						create_decoration(Vector2(x, y), "ac")
					else:
						create_castle(Vector2(x, y))
				'T': create_tile(Vector2(x, y), "res://rooftop_tile.png")
				't': create_cat(Vector2(x, y - 15))
				'I': create_collectible(Vector2(x, y), "ice_cream")
				'M': create_collectible(Vector2(x, y), "tape")

	if current_level == "1-1":
		create_piranha(Vector2(36 * CELL_SIZE + CELL_SIZE / 2, 11 * CELL_SIZE + CELL_SIZE / 2 - 40))
		var cloud_positions = [
			Vector2(300, 60), Vector2(900, 100), Vector2(1600, 50),
			Vector2(2400, 90), Vector2(3200, 55), Vector2(4000, 110),
			Vector2(4800, 70), Vector2(5600, 95)
		]
		for cp in cloud_positions:
			var cloud = Sprite2D.new()
			cloud.texture = load("res://cloud.png")
			cloud.position = cp
			cloud.z_index = -1
			add_child(cloud)
	elif current_level == "1-2":
		var building_positions = [
			Vector2(120, 420), Vector2(380, 400), Vector2(650, 430),
			Vector2(920, 390), Vector2(1180, 410), Vector2(1450, 380),
			Vector2(1720, 420), Vector2(1980, 400), Vector2(2250, 430),
			Vector2(2520, 390), Vector2(2780, 410), Vector2(3050, 420),
			Vector2(3350, 400), Vector2(3650, 430), Vector2(3950, 390),
			Vector2(4250, 410), Vector2(4550, 420), Vector2(4750, 400)
		]
		for bp in building_positions:
			var b = Sprite2D.new()
			b.texture = load("res://building.png")
			b.position = bp
			b.z_index = -2
			var s = 0.8 + (int(bp.x) % 7) * 0.1
			b.scale = Vector2(s, s)
			add_child(b)

		# Moving platform
		create_moving_platform(Vector2(50 * CELL_SIZE + CELL_SIZE / 2, 10 * CELL_SIZE + CELL_SIZE / 2), 100.0, 30.0)

		# Clotheslines (thin platforms)
		create_clothesline(Vector2(55 * CELL_SIZE, 9 * CELL_SIZE))
		create_clothesline(Vector2(82 * CELL_SIZE, 8 * CELL_SIZE))
		create_clothesline(Vector2(105 * CELL_SIZE, 6 * CELL_SIZE))

		# Antenna poles (obstacles)
		create_antenna(Vector2(40 * CELL_SIZE, 11 * CELL_SIZE))
		create_antenna(Vector2(68 * CELL_SIZE, 10 * CELL_SIZE))
		create_antenna(Vector2(95 * CELL_SIZE, 9 * CELL_SIZE))

		# Birds
		create_bird(Vector2(600, 120))
		create_bird(Vector2(1400, 90))
		create_bird(Vector2(2200, 140))
		create_bird(Vector2(3000, 110))
		create_bird(Vector2(3800, 160))

		# Sunset particles
		create_sunset_particles()

		# Checkpoint (mid-level respawn point)
		create_checkpoint(Vector2(55 * CELL_SIZE + CELL_SIZE / 2, 12 * CELL_SIZE + CELL_SIZE / 2))

		# Water tower (finish trigger)
		create_watertower(Vector2(117 * CELL_SIZE + CELL_SIZE / 2, 11.75 * CELL_SIZE))

func on_pipe_entered(destination: String):
	var tw = fade_out()
	tw.tween_callback(func():
		if destination == "1-2":
			load_level("1-2")
		elif destination == "1-1":
			load_level("1-1")
		fade_in()
	)
