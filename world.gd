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

var stomp_combo = 0
var stomp_combo_timer = 0.0
const STOMP_SCORES = [100, 200, 400, 800, 1000, 2000, 4000, 8000]

const LEVEL_WIDTH = 160

var level_map = []

func build_level_map():
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

	# 水管1
	build_pipe(36, 3)

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

func set_map(row: int, col: int, ch: String):
	if row < 0 or row >= level_map.size() or col < 0 or col >= LEVEL_WIDTH:
		return
	var line = level_map[row]
	level_map[row] = line.substr(0, col) + ch + line.substr(col + 1)

func build_pipe(start_col: int, height: int):
	for r in range(14 - height, 14):
		set_map(r, start_col, "P")

func _ready():
	build_level_map()

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
	var bgm_stream = load("res://bgm.wav")
	bgm_stream.loop_mode = 1
	bgm_player.stream = bgm_stream
	add_child(bgm_player)
	bgm_player.play()

	# 天空背景色
	RenderingServer.set_default_clear_color(Color(0.35, 0.55, 0.95))

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
	camera.limit_right = LEVEL_WIDTH * CELL_SIZE
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 10.0
	player_body.add_child(camera)

	player_body.set_script(load("res://player.gd"))
	add_child(player_body)

	# ===== 生成关卡瓦片 =====
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
				'R':
					var r = create_tile(Vector2(x, y), "res://brick.png", "MultiBrick", "res://question_block.gd")
					r.content = "coin"
					r.coin_count = 10
				'P':
					var p = create_tile(Vector2(x, y), "res://pipe.png")
					p.add_to_group("pipe")
					if col == 36:
						p.add_to_group("warp_pipe")
				'E': create_enemy(Vector2(x, y - 15), 80.0)
				'K': create_koopa(Vector2(x, y - 15))
				'C': create_coin(Vector2(x, y))
				'F': create_goal(Vector2(x, y))
				'A': create_castle(Vector2(x, y))

	# 食人花（只在第一根水管上方）
	create_piranha(Vector2(36 * CELL_SIZE + CELL_SIZE / 2, 11 * CELL_SIZE + CELL_SIZE / 2 - 40))

	# 背景云朵
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

func play_sfx(name: String):
	audio_player.stream = sfx[name]
	audio_player.play()

func _unhandled_input(event: InputEvent) -> void:
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

func add_score(amount = 1):
	score += amount
	score_label.text = "金币: " + str(score)
	if score >= 100:
		score -= 100
		score_label.text = "金币: " + str(score)
		add_life()
		play_sfx("coin")

func add_life():
	lives += 1
	lives_label.text = "生命: " + str(lives)

func add_points(amount: int):
	points += amount
	points_label.text = "分数: " + str(points)

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
