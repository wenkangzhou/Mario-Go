extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -620.0
const GRAVITY = 800.0
const START_POS = Vector2(100, 300)

var is_crouching = false
var normal_height = 60.0
var crouch_height = 30.0

var size_state = "small"  # small, big, fire
var invincible = false
var can_shoot = false
var shoot_pressed = false
var is_entering_pipe = false
var is_finishing = false
var pipe_timer = 0.0
var star_power = false
var star_timer = 0.0
var star_tween: Tween = null
var is_dying = false
var shoot_cooldown = 0.0

func _ready():
	var feet_area = Area2D.new()
	feet_area.name = "FeetArea"
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 10)
	col.shape = shape
	feet_area.add_child(col)
	feet_area.position = Vector2(0, 35)
	add_child(feet_area)

func _physics_process(delta: float) -> void:
	if get_parent().game_over:
		return
	if is_dying:
		velocity.y += GRAVITY * delta
		move_and_slide()
		return

	shoot_cooldown -= delta
	if shoot_cooldown < 0:
		shoot_cooldown = 0
	if is_finishing:
		return
	if is_entering_pipe:
		pipe_timer += delta
		position.y += 80 * delta
		if pipe_timer >= 0.5:
			is_entering_pipe = false
			pipe_timer = 0
			get_parent().add_life()
			reset_size()
			position = START_POS
			velocity = Vector2.ZERO
		return

	# 加速跑（B键或Shift）
	var is_running = Input.is_key_pressed(KEY_B) or Input.is_key_pressed(KEY_SHIFT)
	var current_speed = SPEED * 1.6 if is_running else SPEED
	var current_jump = JUMP_VELOCITY * 1.15 if is_running else JUMP_VELOCITY
	var current_accel = 1400.0 if is_running else 1200.0
	var current_friction = 1000.0 if is_running else 800.0

	# 蹲下处理
	if Input.is_action_pressed("ui_down") and is_on_floor():
		if not is_crouching:
			is_crouching = true
			$CollisionShape2D.shape.size.y = crouch_height
			$CollisionShape2D.position.y = 15
			$Sprite2D.scale.y = 0.6 if size_state == "small" else 0.45
			$Sprite2D.position.y = 12 if size_state == "small" else 22
	else:
		if is_crouching:
			var stand_height = 60 if size_state == "small" else 80
			var test_dist = -(stand_height - crouch_height)
			if not test_move(transform, Vector2(0, test_dist)):
				is_crouching = false
				$CollisionShape2D.shape.size.y = stand_height
				$CollisionShape2D.position.y = 0 if size_state == "small" else -10
				$Sprite2D.scale.y = 1.0
				$Sprite2D.position.y = 0

	if not is_on_floor():
		velocity.y += GRAVITY * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor() and not is_crouching:
		velocity.y = current_jump
		get_parent().play_sfx("jump")

	# 发射火球（Z键）
	if Input.is_key_pressed(KEY_Z):
		if not shoot_pressed and can_shoot and not is_crouching and shoot_cooldown <= 0:
			shoot_pressed = true
			shoot()
	else:
		shoot_pressed = false

	var direction := Input.get_axis("ui_left", "ui_right")
	if direction < 0:
		$Sprite2D.flip_h = true
	elif direction > 0:
		$Sprite2D.flip_h = false

	if not is_crouching:
		if direction:
			velocity.x = move_toward(velocity.x, direction * current_speed, current_accel * delta)
		else:
			velocity.x = move_toward(velocity.x, 0, current_friction * delta)
	else:
		if direction:
			velocity.x = move_toward(velocity.x, direction * current_speed * 0.3, 400.0 * delta)
		else:
			velocity.x = move_toward(velocity.x, 0, 250.0 * delta)

	move_and_slide()

	# 碰到敌人
	for i in get_slide_collision_count():
		var collision = get_slide_collision(i)
		var collider = collision.get_collider()
		if collider and collider.is_in_group("enemy"):
			if star_power:
				collider.die()
				velocity.y = -250
				get_parent().add_stomp_score(position)
			elif collider.has_method("become_shell"):
				if collision.get_normal().y < -0.5:
					if not collider.is_shell:
						collider.become_shell()
					else:
						if collider.is_sliding:
							collider.is_sliding = false
							collider.velocity.x = 0
						else:
							collider.is_sliding = true
							collider.dir = 1 if position.x < collider.position.x else -1
					velocity.y = -250
					get_parent().add_stomp_score(position)
				else:
					if collider.is_shell and not collider.is_sliding:
						collider.is_sliding = true
						collider.dir = 1 if position.x < collider.position.x else -1
						get_parent().play_sfx("stomp")
					else:
						take_damage()
			elif collision.get_normal().y < -0.5:
				collider.die()
				velocity.y = -250
				get_parent().add_stomp_score(position)
			else:
				take_damage()
			break

	# 碰到星星
	for i in get_slide_collision_count():
		var collider = get_slide_collision(i).get_collider()
		if collider and collider.is_in_group("star"):
			get_star()
			get_parent().add_points(1000)
			collider.queue_free()
			break

	# 碰到蘑菇
	for i in get_slide_collision_count():
		var collider = get_slide_collision(i).get_collider()
		if collider and collider.is_in_group("mushroom"):
			if collider.get_meta("is_1up", false):
				get_parent().add_life()
			else:
				grow()
			get_parent().add_points(1000)
			collider.queue_free()
			break

	# 顶砖块/问号砖
	for i in get_slide_collision_count():
		var collision = get_slide_collision(i)
		var collider = collision.get_collider()
		if collider and collider.is_in_group("hittable"):
			if collision.get_normal().y > 0.3:
				collider.hit()
				velocity.y = 0
				break

	# 传送水管检测
	if is_on_floor() and is_crouching:
		var on_warp = false
		for body in $FeetArea.get_overlapping_bodies():
			if body.is_in_group("warp_pipe"):
				on_warp = true
				break
		if on_warp:
			pipe_timer += delta
			if pipe_timer >= 0.8:
				pipe_timer = 0
				is_entering_pipe = true
				get_parent().play_sfx("pipe")
		else:
			pipe_timer = 0
	else:
		pipe_timer = 0

	# 掉出世界底部，死亡动画
	if position.y > 650 and not is_dying:
		is_dying = true
		velocity.y = -250
		get_parent().bgm_player.stop()
		if has_node("CollisionShape2D"):
			$CollisionShape2D.set_deferred("disabled", true)
		await get_tree().create_timer(1.2).timeout
		get_parent().lose_life()
		get_parent().play_sfx("hurt")
		reset_size()
		is_dying = false
		star_power = false
		if star_tween:
			star_tween.kill()
		if has_node("CollisionShape2D"):
			$CollisionShape2D.set_deferred("disabled", false)
		position = START_POS
		velocity = Vector2.ZERO
		if get_parent().lives > 0:
			get_parent().bgm_player.play()

	# 无敌星倒计时
	if star_power:
		star_timer -= delta
		if star_timer <= 0:
			star_power = false
			$Sprite2D.modulate = Color(1, 1, 1)
			if star_tween:
				star_tween.kill()

func shoot():
	shoot_cooldown = 0.25
	var dir = -1 if $Sprite2D.flip_h else 1
	get_parent().create_fireball(position + Vector2(dir * 30, -10), dir)

func grow():
	if size_state == "small":
		size_state = "big"
		$CollisionShape2D.shape.size.y = 80
		$CollisionShape2D.position.y = -10
		get_parent().play_sfx("coin")
		var tween = create_tween()
		for i in range(3):
			tween.tween_callback(func(): $Sprite2D.texture = load("res://big_player.png"))
			tween.tween_interval(0.06)
			tween.tween_callback(func(): $Sprite2D.texture = load("res://player.png"))
			tween.tween_interval(0.06)
		tween.tween_callback(func(): $Sprite2D.texture = load("res://big_player.png"))
	else:
		# 已变大/火焰，吃蘑菇只加分
		get_parent().add_score()
		get_parent().play_sfx("coin")

func get_fire():
	if size_state == "small":
		grow()
	size_state = "fire"
	can_shoot = true
	$Sprite2D.texture = load("res://fire_player.png")
	get_parent().play_sfx("coin")
	var tween = create_tween()
	tween.set_loops(4)
	tween.tween_property($Sprite2D, "modulate", Color(2, 2, 2), 0.08)
	tween.tween_property($Sprite2D, "modulate", Color(1, 1, 1), 0.08)

func get_star():
	star_power = true
	star_timer = 10.0
	get_parent().play_sfx("coin")
	if star_tween:
		star_tween.kill()
	star_tween = create_tween()
	star_tween.set_loops()
	star_tween.tween_property($Sprite2D, "modulate", Color(2, 2, 0.5), 0.15)
	star_tween.tween_property($Sprite2D, "modulate", Color(1.5, 1.5, 0.3), 0.15)

func take_damage():
	if star_power or invincible:
		return
	if size_state == "fire":
		size_state = "big"
		can_shoot = false
		$Sprite2D.texture = load("res://big_player.png")
	elif size_state == "big":
		reset_size()
	else:
		get_parent().bgm_player.stop()
		get_parent().lose_life()
		get_parent().play_sfx("hurt")
		position = START_POS
		velocity = Vector2.ZERO
		star_power = false
		if star_tween:
			star_tween.kill()
		$Sprite2D.modulate = Color(1, 1, 1, 1)
		if get_parent().lives > 0:
			get_parent().bgm_player.play()
		return
	# 无敌闪烁
	invincible = true
	var tween = create_tween()
	tween.set_loops(6)
	tween.tween_property($Sprite2D, "modulate:a", 0.3, 0.1)
	tween.tween_property($Sprite2D, "modulate:a", 1.0, 0.1)
	tween.tween_callback(func(): invincible = false)

func reset_size():
	size_state = "small"
	can_shoot = false
	$CollisionShape2D.shape.size.y = 60
	$CollisionShape2D.position.y = 0
	$Sprite2D.texture = load("res://player.png")
	$Sprite2D.scale.y = 1.0
	$Sprite2D.position.y = 0
	$Sprite2D.modulate = Color(1, 1, 1, 1)
