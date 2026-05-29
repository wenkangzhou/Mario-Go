extends Area2D

var is_triggered = false
var flag_node = null

func _ready():
	body_entered.connect(_on_body_entered)
	if has_meta("flag_node"):
		flag_node = get_meta("flag_node")

func _on_body_entered(body: Node2D) -> void:
	if body.name == "Player" and not is_triggered:
		is_triggered = true
		body.is_finishing = true
		body.velocity = Vector2.ZERO

		var target_x = position.x + 8
		body.position.x = target_x
		body.get_node("Sprite2D").flip_h = true

		get_parent().play_sfx("win")

		var slide = create_tween()
		slide.tween_property(body, "position:y", position.y + 150, 1.5)
		if flag_node:
			slide.parallel().tween_property(flag_node, "position:y", position.y + 130, 1.5)
		await slide.finished

		body.get_node("Sprite2D").flip_h = false
		var walk = create_tween()
		walk.tween_property(body, "position:x", body.position.x + 120, 1.5)
		await walk.finished

		get_parent().add_time_bonus()
		for i in range(6):
			await get_tree().create_timer(0.4).timeout
			get_parent().create_firework(Vector2(6200 + randi() % 300, 150 + randi() % 150))
		get_parent().show_victory()
