extends Area2D

var start_y: float
var timer = 0.0
const CYCLE = 4.0
const EXTEND = 2.0

func _ready():
	add_to_group("piranha")
	start_y = position.y
	body_entered.connect(_on_body_entered)
	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(30, 50)
	col.shape = shape
	add_child(col)
	# 初始隐藏在水管内
	position.y = start_y + 100
	$Sprite2D.visible = false

func _process(delta: float) -> void:
	var player = get_parent().get_node_or_null("Player")
	var player_near = false
	if player and abs(player.global_position.x - global_position.x) < 30 and player.global_position.y < global_position.y + 20:
		player_near = true

	timer += delta
	var t = fmod(timer, CYCLE)
	if player_near:
		position.y = move_toward(position.y, start_y + 100, 80 * delta)
		$Sprite2D.visible = false
	else:
		if t < EXTEND:
			position.y = move_toward(position.y, start_y, 80 * delta)
		else:
			position.y = move_toward(position.y, start_y + 100, 80 * delta)
		# 只有大部分升出 pipe 才可见
		$Sprite2D.visible = position.y < start_y + 30

func _on_body_entered(body: Node2D) -> void:
	if body.name == "Player":
		body.take_damage()
