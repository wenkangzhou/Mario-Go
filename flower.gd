extends Area2D

func _ready():
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 30)
	col.shape = shape
	add_child(col)
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	for body in get_overlapping_bodies():
		if body.name == "Player":
			body.get_fire()
			get_parent().add_points(1000)
			queue_free()
			return

func _on_body_entered(body: Node2D) -> void:
	if body.name == "Player":
		body.get_fire()
		get_parent().add_points(1000)
		queue_free()
