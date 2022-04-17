image = "sablablab"
format = ["png", "jpg", "jpeg", "webp", "gif"]

if any(s in image for s in format):
    print(f"![{image}]({image})")
else:
    print(image)
