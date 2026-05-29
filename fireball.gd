extends CharacterBody2D

const SPEED = 400.0
const LIFETIME = 2.5
var direction = 1
var lifetime = 0.0

func _ready():
	add_to_group("fireball")
	direction = get_meta("direction", 1)
	velocity.x = direction * SPEED

	var area = Area2D.new()
	var col = CollisionShape2D.new()
	var shape = CircleShape2D.new()
	shape.radius = 8
	col.shape = shape
	area.add_child(col)
	area.area_entered.connect(_on_area_entered)
	add_child(area)

func _notification(what):
	if what == NOTIFICATION_PREDELETE:
		if get_parent():
			get_parent().fireball_count -= 1

func _on_area_entered(area: Area2D) -> void:
	if area.is_in_group("piranha"):
		area.queue_free()
		queue_free()

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y += 1200 * delta
	else:
		velocity.y = -300
	velocity.x = direction * SPEED
	move_and_slide()

	for i in get_slide_collision_count():
		var collider = get_slide_collision(i).get_collider()
		if collider and collider.is_in_group("enemy"):
			collider.die()
			queue_free()
			return
		if collider and (collider.is_in_group("star") or collider.is_in_group("mushroom")):
			queue_free()
			return
		if collider and collider.is_in_group("hittable"):
			if collider.name == "Brick":
				collider.hit()
			queue_free()
			return

	lifetime += delta
	if lifetime >= LIFETIME or position.y > 700 or position.x < -100 or position.x > 7000:
		queue_free()
