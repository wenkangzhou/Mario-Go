extends StaticBody2D

var was_hit = false
var content = "coin"
var is_bumping = false
var coin_count = 1

func hit():
	if is_bumping:
		return
	is_bumping = true

	var original_y = position.y
	var tween = create_tween()
	tween.tween_property(self, "position:y", original_y - 8, 0.08)
	tween.tween_property(self, "position:y", original_y, 0.08)
	await tween.finished

	if coin_count > 0:
		coin_count -= 1
		match content:
			"coin":
				get_parent().create_coin(position + Vector2(0, -50), true)
			"mushroom":
				get_parent().create_mushroom(position + Vector2(0, -40))
			"1up":
				get_parent().create_mushroom(position + Vector2(0, -40), true)
			"flower":
				get_parent().create_flower(position + Vector2(0, -40))
			"star":
				get_parent().create_star(position + Vector2(0, -40))
		get_parent().play_sfx("coin")
		if coin_count == 0:
			was_hit = true
			$Sprite2D.texture = load("res://used_block.png")

	is_bumping = false
