extends CharacterBody2D

const SPEED = 80.0
var dir = 1
var spawn_timer = 0.0
const SPAWN_TIME = 0.4
var pickup_area: Area2D

func _ready():
	var player = get_parent().get_node_or_null("Player")
	if player:
		dir = 1 if player.global_position.x < global_position.x else -1

	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	add_child(col)
	collision_layer = 0
	collision_mask = 0

	pickup_area = Area2D.new()
	var area_col = CollisionShape2D.new()
	var area_shape = RectangleShape2D.new()
	area_shape.size = Vector2(30, 30)
	area_col.shape = area_shape
	pickup_area.add_child(area_col)
	add_child(pickup_area)
	pickup_area.body_entered.connect(_on_body_entered)

	if get_meta("is_1up", false):
		$Sprite2D.texture = load("res://1up.png")

func _on_body_entered(body: Node2D) -> void:
	if spawn_timer < SPAWN_TIME:
		return
	if body.name == "Player":
		if get_meta("is_1up", false):
			body.get_parent().add_life()
		else:
			body.grow()
		get_parent().add_points(1000)
		queue_free()
		return
	if body.is_in_group("fireball"):
		get_parent().add_score()
		queue_free()
		return

func _physics_process(delta: float) -> void:
	if spawn_timer < SPAWN_TIME:
		spawn_timer += delta
		position.y -= 80 * delta
		if spawn_timer >= SPAWN_TIME:
			collision_layer = 1
			collision_mask = 1
			check_pickup()
		return

	if not is_on_floor():
		velocity.y += 800 * delta
	velocity.x = dir * SPEED
	move_and_slide()
	if is_on_wall():
		dir *= -1

	check_pickup()

func check_pickup():
	# 方法1: Area2D 重叠检测
	for body in pickup_area.get_overlapping_bodies():
		if body.name == "Player":
			if get_meta("is_1up", false):
				body.get_parent().add_life()
			else:
				body.grow()
			get_parent().add_points(1000)
			queue_free()
			return
		if body.is_in_group("fireball"):
			get_parent().add_score()
			queue_free()
			return

	# 方法2: 距离检测（备用，防止物理信号漏掉）
	var player = get_parent().get_node_or_null("Player")
	if player and global_position.distance_to(player.global_position) < 40:
		if get_meta("is_1up", false):
			player.get_parent().add_life()
		else:
			player.grow()
		get_parent().add_points(1000)
		queue_free()
		return
	for child in get_parent().get_children():
		if child.is_in_group("fireball"):
			if global_position.distance_to(child.global_position) < 30:
				get_parent().add_score()
				queue_free()
				return
