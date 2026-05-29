extends CharacterBody2D

const SPEED = 80.0
var direction = 1
var start_x: float

func _ready():
	start_x = position.x
	$Sprite2D.flip_h = direction < 0

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += 800 * delta

	velocity.x = direction * SPEED
	move_and_slide()

	var patrol = get_meta("patrol_width", 100.0)
	if position.x > start_x + patrol:
		direction = -1
		$Sprite2D.flip_h = true
	elif position.x < start_x - patrol:
		direction = 1
		$Sprite2D.flip_h = false

	if is_on_floor():
		if not test_move(transform, Vector2(direction * 20, 10)):
			direction *= -1
			$Sprite2D.flip_h = direction < 0

	# 前方敌人检测（在物理碰撞前转向）
	for body in get_parent().get_children():
		if body != self and body.is_in_group("enemy"):
			var dx = body.position.x - position.x
			var dy = body.position.y - position.y
			if abs(dy) < 30 and ((direction > 0 and dx > 0 and dx < 35) or (direction < 0 and dx < 0 and dx > -35)):
				direction *= -1
				$Sprite2D.flip_h = direction < 0
				break

	for i in get_slide_collision_count():
		var collider = get_slide_collision(i).get_collider()
		if collider and collider.has_method("become_shell") and collider.is_sliding:
			die()
			return
		if collider and collider.is_in_group("enemy") and collider.name != "Player":
			if position.x < collider.position.x:
				direction *= -1
				$Sprite2D.flip_h = direction < 0
			break

	if position.y > 700:
		queue_free()

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
