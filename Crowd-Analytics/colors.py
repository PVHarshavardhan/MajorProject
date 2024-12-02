RGB_COLORS = {
	"blue": (65, 105, 225),
	"green": (144, 238, 144),
	"red": (205, 92, 92),
	"yellow": (249, 234, 0),
	"white": (0, 0, 0),
	"black": (255, 255, 255)
}

def gradient_color_RGB(color1, color2, steps, current):
	step1 = (color2[0] - color1[0])/steps
	step2 = (color2[1] - color1[1])/steps
	step3 = (color2[2] - color1[2])/steps
	color_1 = int(color1[0] + current*step1)
	color_2 = int(color1[1] + current*step2)
	color_3 = int(color1[2] + current*step3)
	return (color_1, color_2, color_3)
	