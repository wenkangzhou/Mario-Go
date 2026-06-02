extends Area2D

var collected = false

func _ready():
	body_entered.connect(_on_body_entered)
	# Gentle floating idle animation
	var tween = create_tween()
	tween.set_loops()
	tween.tween_property(self, "position:y", position.y - 3, 0.7).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "position:y", position.y + 3, 0.7).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

func _on_body_entered(body: Node2D) -> void:
	if body.name == "Player" and not collected:
		collected = true
		var type = get_meta("collectible_type", "tape")
		var points = 200
		var label_text = ""
		match type:
			"watermelon":
				points = 300
				label_text = "西瓜!"
			"ice_cream":
				points = 500
				label_text = "冰棍!"
			"tape":
				points = 200
				label_text = "磁带!"
		get_parent().add_points(points)
		get_parent().play_sfx("coin")
		get_parent().create_floating_text(position, label_text + " +" + str(points))
		var tween = create_tween()
		tween.tween_property(self, "position:y", position.y - 30, 0.2)
		tween.parallel().tween_property(self, "modulate:a", 0.0, 0.2)
		tween.tween_callback(queue_free)
