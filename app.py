from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response

app = FastAPI(title="EBII Background Removal API")


@app.get("/")
def root():
    return {"success": True, "message": "Background removal service is running"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()

        if not input_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        # Lazy import: servis açıldıktan sonra çağrı geldiğinde yüklenir
        from rembg import remove

        output_bytes = remove(input_bytes)

        return Response(
            content=output_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": "inline; filename=removed-bg.png"
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))