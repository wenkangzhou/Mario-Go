extends StaticBody2D

var is_bumping = false

func hit():
	if is_bumping:
		return
	is_bumping = true
	get_parent().play_sfx("stomp")

	var original_y = position.y
	var tween = create_tween()
	tween.tween_property(self, "position:y", original_y - 8, 0.08)
	tween.tween_property(self, "position:y", original_y, 0.08)
	await tween.finished

	for i in range(12):
		var piece = Sprite2D.new()
		piece.texture = $Sprite2D.texture
		piece.region_enabled = true
		piece.region_rect = Rect2(randi() % 20, randi() % 20, 8 + randi() % 12, 8 + randi() % 12)
		piece.position = position + Vector2(randi() % 20 - 10, randi() % 20 - 10)
		piece.rotation = randf() * PI
		get_parent().add_child(piece)

		var ptween = piece.create_tween()
		var vx = (randf() - 0.5) * 400
		var vy = -200 - randf() * 180
		var mid = piece.position + Vector2(vx * 0.25, vy * 0.3)
		var end = piece.position + Vector2(vx * 0.7, 120)
		ptween.tween_property(piece, "position", mid, 0.15).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		ptween.tween_property(piece, "position", end, 0.4).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		ptween.parallel().tween_property(piece, "modulate:a", 0.0, 0.55)
		ptween.parallel().tween_property(piece, "rotation", piece.rotation + (randf() - 0.5) * 6, 0.55)
		ptween.tween_callback(piece.queue_free)
	queue_free()
