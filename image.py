@app.post("/image")
async def generate_image(data: dict):
    prompt = data["prompt"]

    result = subprocess.run(
        ["python", "sd_generate.py", prompt],
        capture_output=True,
        text=True
    )

    return {"image": result.stdout.strip()}
