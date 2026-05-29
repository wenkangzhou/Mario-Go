extends CharacterBody2D

const SPEED = 80.0
const BOUNCE = -400.0
var dir = 1
var spawn_timer = 0.0
const SPAWN_TIME = 0.4
var pickup_area: Area2D

func _ready():
	pickup_area = Area2D.new()
	var area_col = CollisionShape2D.new()
	var area_shape = CircleShape2D.new()
	area_shape.radius = 20
	area_col.shape = area_shape
	pickup_area.add_child(area_col)
	add_child(pickup_area)
	pickup_area.body_entered.connect(_on_body_entered)
	collision_layer = 0
	collision_mask = 0

func _on_body_entered(body: Node2D) -> void:
	if spawn_timer < SPAWN_TIME:
		return
	if body.name == "Player":
		body.get_star()
		queue_free()

func _physics_process(delta: float) -> void:
	if spawn_timer < SPAWN_TIME:
		spawn_timer += delta
		position.y -= 80 * delta
		if spawn_timer >= SPAWN_TIME:
			collision_layer = 1
			collision_mask = 1
			velocity.y = BOUNCE
			check_pickup()
		return

	if not is_on_floor():
		velocity.y += 800 * delta
	else:
		velocity.y = BOUNCE

	velocity.x = dir * SPEED
	check_pickup()
	move_and_slide()
	if is_on_wall():
		dir *= -1

func check_pickup():
	for body in pickup_area.get_overlapping_bodies():
		if body.name == "Player":
			body.get_star()
			queue_free()
			return
