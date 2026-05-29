extends Area2D

var collected = false

func _ready():
	body_entered.connect(_on_body_entered)
	if get_meta("bouncing", false):
		bounce_auto()

func bounce_auto():
	var original_y = position.y
	var tween = create_tween()
	tween.tween_property(self, "position:y", original_y - 60, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "position:y", original_y + 20, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tween.parallel().tween_property(self, "modulate:a", 0.0, 0.3)
	tween.tween_callback(func():
		if not collected:
			get_parent().add_score()
			get_parent().add_points(200)
			get_parent().play_sfx("coin")
		queue_free()
	)

func _on_body_entered(body: Node2D) -> void:
	if body.name == "Player" and not collected:
		collected = true
		get_parent().add_score()
		get_parent().add_points(200)
		get_parent().play_sfx("coin")
		var tween = create_tween()
		tween.tween_property(self, "position:y", position.y - 30, 0.2)
		tween.parallel().tween_property(self, "modulate:a", 0.0, 0.2)
		tween.tween_callback(queue_free)
