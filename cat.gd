extends CharacterBody2D

enum State { PATROL, DETECT, CHASE, ATTACK, HURT }
var state = State.PATROL
var direction = -1
var patrol_start: float
const PATROL_SPEED = 60.0
const CHASE_SPEED = 120.0
var detect_timer = 0.0
var chase_timer = 0.0
var attack_timer = 0.0
var player_ref = null

func _ready():
	patrol_start = position.x
	$Sprite2D.flip_h = direction < 0
	$DetectionArea.body_entered.connect(_on_detection_enter)
	$DetectionArea.body_exited.connect(_on_detection_exit)

func _physics_process(delta: float) -> void:
	if state == State.HURT:
		return

	if not is_on_floor():
		velocity.y += 800 * delta

	# 边缘检测（防止掉下平台）
	if is_on_floor() and velocity.x != 0:
		var check_dir = 1 if velocity.x > 0 else -1
		if not test_move(transform, Vector2(check_dir * 20, 10)):
			if state == State.PATROL:
				direction *= -1
				$Sprite2D.flip_h = direction < 0
				velocity.x = direction * PATROL_SPEED
			elif state == State.CHASE:
				velocity.x = 0

	match state:
		State.PATROL:
			velocity.x = direction * PATROL_SPEED
			move_and_slide()

			var patrol = get_meta("patrol_width", 80.0)
			if position.x > patrol_start + patrol:
				direction = -1
				$Sprite2D.flip_h = true
			elif position.x < patrol_start - patrol:
				direction = 1
				$Sprite2D.flip_h = false

		State.DETECT:
			velocity.x = move_toward(velocity.x, 0, 400 * delta)
			move_and_slide()
			if player_ref and is_instance_valid(player_ref):
				$Sprite2D.flip_h = player_ref.position.x < position.x
			detect_timer -= delta
			if detect_timer <= 0:
				state = State.CHASE
				chase_timer = 3.0

		State.CHASE:
			if player_ref and is_instance_valid(player_ref):
				var target_dir = 1 if player_ref.position.x > position.x else -1
				$Sprite2D.flip_h = target_dir < 0
				velocity.x = target_dir * CHASE_SPEED

				var dist = position.distance_to(player_ref.position)
				if dist < 40:
					state = State.ATTACK
					attack_timer = 0.5
			else:
				velocity.x = move_toward(velocity.x, 0, 400 * delta)

			move_and_slide()
			chase_timer -= delta
			if chase_timer <= 0:
				state = State.PATROL
				player_ref = null

		State.ATTACK:
			velocity.x = move_toward(velocity.x, 0, 600 * delta)
			move_and_slide()
			attack_timer -= delta
			# Pounce tween: lunge forward then retract
			if attack_timer > 0.45 and $Sprite2D.position.x == 0:
				var lunge_dir = 1 if not $Sprite2D.flip_h else -1
				var t = create_tween()
				t.tween_property($Sprite2D, "position:x", lunge_dir * 12, 0.08)
				t.tween_property($Sprite2D, "position:x", 0, 0.12)
			if attack_timer <= 0:
				$Sprite2D.position.x = 0
				if player_ref and is_instance_valid(player_ref) and position.distance_to(player_ref.position) < 60:
					state = State.CHASE
					chase_timer = 2.0
				else:
					state = State.PATROL
					player_ref = null

	if position.y > 700:
		queue_free()

func _on_detection_enter(body: Node2D):
	if body.name == "Player" and state != State.HURT:
		player_ref = body
		if state == State.PATROL:
			state = State.DETECT
			detect_timer = 0.5

func _on_detection_exit(body: Node2D):
	if body.name == "Player":
		player_ref = null

func die():
	if state == State.HURT:
		return
	state = State.HURT
	get_parent().play_sfx("stomp")
	set_physics_process(false)
	if has_node("CollisionShape2D"):
		$CollisionShape2D.set_deferred("disabled", true)
	$Sprite2D.flip_v = true
	# Hurt flash + spin
	$Sprite2D.modulate = Color(2.0, 0.5, 0.5)
	var tween = create_tween()
	tween.tween_property(self, "position:y", position.y - 60, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.parallel().tween_property($Sprite2D, "rotation", PI * 0.5, 0.3)
	tween.tween_property(self, "position:y", position.y + 200, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tween.parallel().tween_property($Sprite2D, "modulate:a", 0.0, 0.5)
	tween.parallel().tween_property($Sprite2D, "rotation", PI, 0.5)
	tween.tween_callback(queue_free)
