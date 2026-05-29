extends CharacterBody2D

const SPEED = 60.0
const SHELL_SPEED = 300.0
var dir = 1
var is_shell = false
var is_sliding = false

func _ready():
	dir = get_meta("start_dir", 1)
	var col = CollisionShape2D.new()
	col.name = "CollisionShape2D"
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 40)
	col.shape = shape
	add_child(col)
	$Sprite2D.flip_h = dir < 0

func _physics_process(delta: float) -> void:
	if not is_shell:
		if not is_on_floor():
			velocity.y += 800 * delta
		velocity.x = dir * SPEED
		move_and_slide()
		if is_on_wall():
			dir *= -1
			$Sprite2D.flip_h = dir < 0
		if is_on_floor() and not test_move(transform, Vector2(dir * 20, 10)):
			dir *= -1
			$Sprite2D.flip_h = dir < 0

		# 前方敌人检测（在物理碰撞前转向）
		for body in get_parent().get_children():
			if body != self and body.is_in_group("enemy"):
				var dx = body.position.x - position.x
				var dy = body.position.y - position.y
				if abs(dy) < 30 and ((dir > 0 and dx > 0 and dx < 35) or (dir < 0 and dx < 0 and dx > -35)):
					dir *= -1
					$Sprite2D.flip_h = dir < 0
					break
	else:
		if not is_on_floor():
			velocity.y += 800 * delta
		if is_sliding:
			velocity.x = dir * SHELL_SPEED
		else:
			velocity.x = move_toward(velocity.x, 0, 400 * delta)
		move_and_slide()
		if is_sliding and is_on_wall():
			dir *= -1

	if position.y > 700:
		queue_free()

	for i in get_slide_collision_count():
		var collider = get_slide_collision(i).get_collider()
		if collider and collider.is_in_group("enemy"):
			if is_sliding:
				collider.die()
				return
			else:
				if position.x < collider.position.x:
					dir *= -1
					$Sprite2D.flip_h = dir < 0
				break
		if collider and collider.is_in_group("hittable") and is_sliding:
			collider.hit()
			return

func become_shell():
	is_shell = true
	is_sliding = false
	$Sprite2D.texture = load("res://shell.png")
	$CollisionShape2D.shape.size = Vector2(30, 30)
	$CollisionShape2D.position.y = 5
	velocity.x = 0
	get_parent().play_sfx("stomp")

func die():
	get_parent().play_sfx("stomp")
	set_physics_process(false)
	if has_node("CollisionShape2D"):
		$CollisionShape2D.set_deferred("disabled", true)
	$Sprite2D.flip_v = true
	var tween = create_tween()
	tween.tween_property(self, "position:y", position.y - 60, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "position:y", position.y + 200, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tween.parallel().tween_property($Sprite2D, "modulate:a", 0.0, 0.5)
	tween.tween_callback(queue_free)
